from flask import Flask, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import time
import csv
import os
import uuid
from datetime import datetime


app = Flask(__name__)


# ============================================================
# 1. EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ============================================================
# 2. CHROMADB MEMORY
# ============================================================

chroma_client = chromadb.EphemeralClient()

collection = chroma_client.get_or_create_collection(
    "npc_memory"
)


# ============================================================
# 3. OLLAMA
# ============================================================

client = ollama.Client(
    host="http://127.0.0.1:11434"
)

MODEL_NAME = "llama3:latest"


# ============================================================
# 4. BENCHMARK FILE
# ============================================================

BENCHMARK_FILE = "benchmark_results.csv"


if not os.path.exists(BENCHMARK_FILE):

    with open(
        BENCHMARK_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "npc",
            "total_latency_sec",
            "model_load_sec",
            "prompt_eval_sec",
            "generation_sec",
            "prompt_tokens",
            "generated_tokens",
            "tokens_per_sec"
        ])


# ============================================================
# 5. NPC ENDPOINT
# ============================================================

@app.route("/npc", methods=["POST"])
def npc_chat():

    # --------------------------------------------------------
    # Start total timer
    # --------------------------------------------------------

    total_start = time.perf_counter()


    # --------------------------------------------------------
    # Get data from Unity
    # --------------------------------------------------------

    data = request.json

    npc_name = data["npc"]
    player_message = data["message"]


    # --------------------------------------------------------
    # Create embedding
    # --------------------------------------------------------

    embedding_start = time.perf_counter()

    embedding = model.encode(
        player_message
    ).tolist()

    embedding_time = (
        time.perf_counter() - embedding_start
    )


    # --------------------------------------------------------
    # Search memory
    # --------------------------------------------------------

    memory_start = time.perf_counter()

    memories = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    memory_time = (
        time.perf_counter() - memory_start
    )


    # --------------------------------------------------------
    # Combine previous memories
    # --------------------------------------------------------

    memory_text = ""

    if (
        memories["documents"]
        and len(memories["documents"][0]) > 0
    ):

        memory_text = " ".join(
            memories["documents"][0]
        )


    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
NPC: {npc_name}

Previous Memory:
{memory_text}

Player: {player_message}

Respond naturally like the NPC character.
"""


    # --------------------------------------------------------
    # LLM INFERENCE
    # --------------------------------------------------------

    llm_start = time.perf_counter()

    response = client.chat(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    llm_wall_time = (
        time.perf_counter() - llm_start
    )


    # --------------------------------------------------------
    # Extract response
    # --------------------------------------------------------

    reply = response["message"]["content"]


    # ========================================================
    # OLLAMA PERFORMANCE METRICS
    # ========================================================

    load_duration = response.get(
        "load_duration",
        0
    )

    prompt_eval_duration = response.get(
        "prompt_eval_duration",
        0
    )

    eval_duration = response.get(
        "eval_duration",
        0
    )

    prompt_eval_count = response.get(
        "prompt_eval_count",
        0
    )

    eval_count = response.get(
        "eval_count",
        0
    )


    # Ollama reports durations in nanoseconds
    model_load_sec = load_duration / 1_000_000_000

    prompt_eval_sec = (
        prompt_eval_duration / 1_000_000_000
    )

    generation_sec = (
        eval_duration / 1_000_000_000
    )


    # --------------------------------------------------------
    # Tokens per second
    # --------------------------------------------------------

    if generation_sec > 0:

        tokens_per_sec = (
            eval_count / generation_sec
        )

    else:

        tokens_per_sec = 0


    # --------------------------------------------------------
    # Total request time
    # --------------------------------------------------------

    total_latency = (
        time.perf_counter() - total_start
    )


    # ========================================================
    # SAVE BENCHMARK RESULT
    # ========================================================

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )


    with open(
        BENCHMARK_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            npc_name,
            round(total_latency, 4),
            round(model_load_sec, 4),
            round(prompt_eval_sec, 4),
            round(generation_sec, 4),
            prompt_eval_count,
            eval_count,
            round(tokens_per_sec, 2)
        ])


    # ========================================================
    # STORE MEMORY
    # ========================================================

    collection.add(

        documents=[player_message],

        embeddings=[embedding],

        ids=[str(uuid.uuid4())]
    )


    # ========================================================
    # SEND RESPONSE TO UNITY
    # ========================================================

    return jsonify({

        "reply": reply,

        "benchmark": {

            "total_latency_sec":
                round(total_latency, 3),

            "model_load_sec":
                round(model_load_sec, 3),

            "prompt_eval_sec":
                round(prompt_eval_sec, 3),

            "generation_sec":
                round(generation_sec, 3),

            "prompt_tokens":
                prompt_eval_count,

            "generated_tokens":
                eval_count,

            "tokens_per_sec":
                round(tokens_per_sec, 2),

            "embedding_sec":
                round(embedding_time, 3),

            "memory_search_sec":
                round(memory_time, 3),

            "llm_wall_time_sec":
                round(llm_wall_time, 3)
        }

    })


# ============================================================
# 6. START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )