# 🧠 AI NPC Memory System

> Give your NPCs a brain. Let them remember, learn, and speak like real characters — entirely offline.

A **Unity (C#) + Python Flask** system that gives game NPCs persistent, context-aware memory powered by a **local LLM via Ollama** and **semantic vector search via ChromaDB**. No cloud API required. Your NPCs remember what the player said, retrieve relevant memories using vector similarity, and generate natural responses — all running on your own machine.

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [📁 Project Structure](#-project-structure)
- [⚙️ Requirements](#️-requirements)
- [🚀 Installation & Setup](#-installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install and Start Ollama](#2-install-and-start-ollama)
  - [3. Set Up the Python Backend](#3-set-up-the-python-backend)
  - [4. Open the Unity Project](#4-open-the-unity-project)
- [▶️ Running the System](#️-running-the-system)
- [🔄 How an NPC Interaction Works](#-how-an-npc-interaction-works)
- [🧠 Memory System](#-memory-system)
- [📊 Performance Benchmarking](#-performance-benchmarking)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [👥 Sharing the Project](#-sharing-the-project)
- [🚀 Future Improvements](#-future-improvements)
- [📜 License](#-license)

---

## ✨ Features

- 🤖 **AI-powered NPC dialogue** — dynamic, context-aware responses instead of scripted lines
- 🧠 **Persistent semantic memory** — NPCs remember past interactions using ChromaDB
- 🔎 **Vector similarity search** — memories are retrieved by meaning, not just keywords, using Sentence Transformers
- 🦙 **Local LLM inference** — runs entirely via Ollama; no internet or cloud API needed
- 🎮 **Unity-based NPC interaction** — full dialogue UI built in the Unity game engine (C#)
- 🐍 **Python Flask backend** — connects Unity to the AI pipeline over HTTP
- 📊 **Benchmarking & CSV logging** — records performance metrics for comparison across machines
- 🔒 **Fully local** — the core system requires no cloud LLM API key

---

## 🏗️ System Architecture

```
                Unity (C#)
                    │
                    │  HTTP POST /npc
                    ▼
             Flask Backend (Python)
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
      ChromaDB       Sentence Transformer
    (Vector Store)     (Embedding Model)
          │                   │
          │      Semantic      │
          │      Search        │
          └─────────┬─────────┘
                    │
             Relevant Memories
                    │
                    ▼
             Prompt Builder
                    │
                    ▼
                 Ollama
                    │
                    ▼
              Local LLM
                    │
                    ▼
             Generated Reply
                    │
                    ▼
                 Unity
             (Dialogue UI)
```

---

## 📁 Project Structure

```
AI_NPC_MEMORY/
│
├── Assets/                  # Unity assets, scenes, scripts, and UI
├── Packages/                # Unity package configuration
├── ProjectSettings/         # Unity project settings
│
├── AI_Server/               # Python Flask backend
│   ├── server.py            # Main Flask API entry point
│   ├── requirements.txt     # Python dependencies
│   └── ...
│
├── benchmark_results.csv    # Recorded performance measurements
├── requirements.txt         # Python dependencies (root-level, if used)
├── README.md                # This file
└── .gitignore
```

> ⚠️ Do **not** commit Unity's generated folders: `Library/`, `Temp/`, `Logs/`, `UserSettings/`. These are regenerated automatically by Unity and should be in your `.gitignore`.

---

## ⚙️ Requirements

Before running this project, install the following tools on your machine.

### 🖥️ System Requirements

| Requirement | Version / Details |
|---|---|
| Operating System | Windows 10/11, macOS 12+, or Ubuntu 20.04+ |
| Python | **3.12** recommended |
| Unity | **6000.3.10f1** (use the same version to avoid compatibility issues) |
| RAM | 8 GB minimum — 16 GB recommended for local LLM inference |
| Storage | 5–10 GB free (for Ollama models) |
| Internet | Only needed for the initial setup (cloning, installing packages, pulling Ollama model) |

---

### 🐍 Python Dependencies

These are installed from `requirements.txt`. Key packages include:

| Package | Purpose |
|---|---|
| `flask` | Web server framework for the backend API |
| `chromadb` | Vector database for persistent NPC memory |
| `sentence-transformers` | Generates semantic embeddings from text |
| `ollama` | Python client for local LLM inference |
| `torch` | Required by Sentence Transformers |

All exact versions are pinned in `AI_Server/requirements.txt`.

---

### 🎮 Unity Requirements

| Requirement | Details |
|---|---|
| Unity Version | **Unity 6000.3.10f1** |
| Unity Hub | Required to open and manage the project |
| Packages | `TextMeshPro` (dialogue UI), `UnityWebRequest` (built-in HTTP client) |

Install Unity Hub from: [https://unity.com/download](https://unity.com/download)

---

### 🦙 Ollama

Ollama runs the local LLM. No cloud API key is needed.

Install Ollama from: [https://ollama.com/](https://ollama.com/)

After installation, verify it works:

```bash
ollama --version
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/HimeshKrishna/AI_NPC_Memory.git
cd AI_NPC_Memory
```

---

### 2. Install and Start Ollama

#### a) Start Ollama

Make sure the Ollama application or service is running in the background. The local Ollama API will be available at:

```
http://127.0.0.1:11434
```

#### b) Pull the required model

Check `AI_Server/server.py` to confirm which model name is configured. Then pull it:

```bash
# Example — if the server is configured for Llama 3:
ollama pull llama3
```

Verify the model is downloaded:

```bash
ollama list
```

> ⚠️ Use the **exact model name** that appears in `server.py`. If the names don't match, Ollama will return an error.

---

### 3. Set Up the Python Backend

#### a) Create a virtual environment

From the root of the cloned repository:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

After activation, your terminal prompt will show:

```
(.venv) C:\...\AI_NPC_Memory>
```

#### b) Install dependencies

Navigate to the backend folder and install:

```bash
cd AI_Server
pip install -r requirements.txt
```

If a `requirements.txt` also exists at the root level, install that too:

```bash
cd ..
pip install -r requirements.txt
```

#### c) Start the Flask server

Make sure Ollama is already running, then:

```bash
cd AI_Server
python server.py
```

The Flask API will start on:

```
http://127.0.0.1:5000
```

Unity communicates with the backend through:

```
POST http://127.0.0.1:5000/npc
```

Leave this terminal open while using Unity.

---

### 4. Open the Unity Project

1. Open **Unity Hub**
2. Click **Add** → **Add project from disk**
3. Navigate to the root of the cloned repository (`AI_NPC_Memory/`) and select it
4. Open the project using **Unity 6000.3.10f1**
5. Wait for Unity to import assets and regenerate the `Library/` folder (this may take a few minutes on first open)
6. In the **Project** panel, open your scene from the `Assets/` folder
7. Press ▶️ **Play**

---

## ▶️ Running the System

Always start the services in this order:

```
1. Start Ollama       →   ollama serve  (or open the Ollama app)
2. Start Flask        →   python server.py  (inside AI_Server/)
3. Press Play         →   in Unity
```

Then walk your player up to an NPC and interact. The NPC will:
- Receive your message via Unity
- Retrieve semantically relevant past memories from ChromaDB
- Build a context-aware prompt with those memories
- Generate a response via Ollama
- Display the response in the Unity dialogue UI
- Store the new interaction as a memory for future conversations

---

## 🔄 How an NPC Interaction Works

```
Player types a message
        │
        ▼
Unity sends  POST /npc  to Flask
        │
        ▼
Flask generates a text embedding  (Sentence Transformer)
        │
        ▼
ChromaDB is searched for similar past memories
        │
        ▼
Relevant memories are retrieved
        │
        ▼
Prompt is built:  [NPC personality] + [retrieved memories] + [player message]
        │
        ▼
Prompt is sent to Ollama (local LLM)
        │
        ▼
LLM generates a natural response
        │
        ▼
Response is returned to Unity
        │
        ▼
NPC speaks the response in the dialogue UI
        │
        ▼
The interaction is saved as a new memory in ChromaDB
```

---

## 🧠 Memory System

The memory system uses **semantic vector retrieval** rather than keyword matching, so NPCs can recall memories by meaning even when the exact words differ.

**How memories are stored:**

When a player interacts with an NPC, the interaction is converted into a vector embedding using a Sentence Transformer model and stored in ChromaDB.

**How memories are retrieved:**

```
New Player Message
        ↓
Generate Embedding  (Sentence Transformer)
        ↓
Search ChromaDB for Similar Vectors
        ↓
Retrieve Most Relevant Memories
        ↓
Inject Memories into LLM Prompt
        ↓
Generate Context-Aware Response
```

This means if a player told an NPC "I defeated the dragon" in a previous session, and later asks "Do you have a quest for me?", the NPC can surface that memory and respond accordingly — without any hardcoded logic.

---

## 📊 Performance Benchmarking

The project includes **CSV-based performance benchmarking** to evaluate how the system performs across different hardware (e.g. a personal laptop vs a college HPC server).

Benchmark results are written to:

```
benchmark_results.csv
```

### 📈 Metrics Recorded

| Metric | Description |
|---|---|
| Total response latency | End-to-end time from player input to NPC response |
| Model load time | Time for Ollama to load the model |
| Prompt processing time | Time to build and embed the prompt |
| Generation time | Time for the LLM to generate the response |
| Prompt token count | Number of tokens in the input prompt |
| Generated token count | Number of tokens in the response |
| Tokens per second | Inference speed |
| Memory retrieval info | Number of memories retrieved and their similarity scores |

### 🧪 Recommended Benchmark Procedure

For a fair comparison across machines:

- ✅ Use the **same model**
- ✅ Use the **same model configuration**
- ✅ Use the **same NPC**
- ✅ Use the **same test prompts**
- ✅ Use the **same number of interactions**
- ✅ Record **multiple runs** and average the results

Example comparison table:

| Environment | Avg Latency | Avg Tokens/sec |
|---|---|---|
| Laptop | X.XX s | XX.XX |
| HPC Server | X.XX s | XX.XX |

---

## 🛠️ Troubleshooting

**Flask cannot connect to Ollama**

Make sure Ollama is running before starting Flask. Check:

```bash
ollama list
```

If the required model is missing:

```bash
ollama pull <model-name>
```

The Ollama API should be available at `http://127.0.0.1:11434`. If Flask cannot reach it, check that Ollama is not blocked by a firewall.

---

**Unity shows "Server Error" or no NPC response**

Check that all three services are running in order:

```
Ollama  →  Flask  →  Unity (Play mode)
```

Flask must be running at `http://127.0.0.1:5000`. Check the Flask terminal for Python errors, and check the Unity Console for HTTP response codes.

---

**ChromaDB or embedding errors**

Make sure the virtual environment is activated:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

**Unity project opens with missing scripts or pink materials**

Make sure these folders are present in the repository after cloning:

```
Assets/
Packages/
ProjectSettings/
```

Do **not** copy the `Library/` folder from another machine. Unity will regenerate it automatically on first open.

---

**`python` command not found**

On some systems, Python 3 is invoked as `py` or `python3`:

```bash
py --version
python3 --version
```

Use whichever works on your system consistently throughout setup.

---

## 👥 Sharing the Project

The repository is public. Another developer can get the full system running by following these steps:

```
1.  git clone https://github.com/HimeshKrishna/AI_NPC_Memory.git
2.  Install Unity 6000.3.10f1 via Unity Hub
3.  Install Python 3.12
4.  Install Ollama  →  https://ollama.com/
5.  Pull the required model  →  ollama pull <model-name>
6.  Create virtual environment  →  python -m venv .venv
7.  Activate it
8.  Install dependencies  →  pip install -r requirements.txt
9.  Start Ollama
10. Start Flask  →  python server.py
11. Open the Unity project and press Play
12. Interact with an NPC
```

> 🔐 **Important:** Never commit `.env` files, API keys, passwords, or private credentials. Also avoid committing `Library/`, `Temp/`, and `Logs/` — these are Unity-generated and machine-specific.

---

## 🚀 Future Improvements

Planned and possible future directions for this project:

- 🧬 Memory importance scoring and decay mechanisms
- 🧬 Better long-term memory management and pruning strategies
- 🎭 Multiple distinct NPC personalities with separate memory namespaces
- 🌐 Multi-NPC shared memory (NPCs that know what other NPCs remember)
- 🔍 Improved memory filtering and relevance ranking
- 📊 Quantitative retrieval-quality evaluation
- ⚡ GPU and HPC acceleration experiments
- 🤖 Comparison of different local LLMs (Llama 3, Mistral, Phi, etc.)
- 🎯 Autonomous NPC decision-making based on accumulated memory
- 💬 Emotional state modeling and dialogue tone variation

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for full details.

---

<div align="center">

👨‍💻 Built by <a href="https://github.com/HimeshKrishna">Himesh Krishna</a>
<br/>
B.Tech — Artificial Intelligence & Machine Learning
<br/><br/>
⭐ If this project helped you, consider leaving a star on the <a href="https://github.com/HimeshKrishna/AI_NPC_Memory">repository</a>!

</div>
