from flask import Flask, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

app = Flask(__name__)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB memory database
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection("npc_memory")

# FORCE Ollama local connection
client = ollama.Client(host='http://127.0.0.1:11434')

@app.route("/npc", methods=["POST"])
def npc_chat():

    # Get data from Unity
    data = request.json
    npc_name = data["npc"]
    player_message = data["message"]

    # Convert player message into embedding
    embedding = model.encode(player_message).tolist()

    # Search memory
    memories = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    # Combine previous memories
    memory_text = ""

    if memories["documents"] and len(memories["documents"][0]) > 0:
        memory_text = " ".join(memories["documents"][0])

    # Prompt for LLM
    prompt = f"""
NPC: {npc_name}

Previous Memory:
{memory_text}

Player: {player_message}

Respond naturally like the NPC character.
"""

    # Generate response using Ollama
    response = client.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract generated reply
    reply = response["message"]["content"]

    # Store current interaction in memory
    collection.add(
        documents=[player_message],
        embeddings=[embedding],
        ids=[str(hash(player_message + npc_name))]
    )

    # Send reply back to Unity
    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)