# 🔍 RAG-Powered Q&A System

A Retrieval-Augmented Generation (RAG) system that answers domain-specific 
questions using content retrieved from local documents — without hallucinating 
answers outside its knowledge base.

This project includes two implementations: a documented Jupyter Notebook for 
step-by-step evaluation, and an interactive CLI app for real-time Q&A.

---

## 📌 What It Does

Instead of relying solely on an LLM's training data, this system:
1. Loads your own documents
2. Splits and embeds them into a vector database
3. Retrieves the most relevant chunks for any given question
4. Passes those chunks to an LLM to generate a grounded answer

If the answer isn't in the documents, it says so — no guessing.

---

## 🏗️ Architecture

```
Documents (.txt)
      ↓
Document Loading  (LangChain DirectoryLoader)
      ↓
Text Splitting    (RecursiveCharacterTextSplitter — 500 tokens, 50 overlap)
      ↓
Embeddings        (Cohere embed-english-v3.0)
      ↓
Vector Store      (Chroma — persisted locally)
      ↓
Retriever         (Top-3/5 semantic search)
      ↓
LLM Generation    (Groq — LLaMA 3.1 8B)
      ↓
Answer + Sources
```

---

## 📁 Project Structure

```
task-6/
│
├── rag_notebook.ipynb        # Jupyter Notebook — step-by-step documented 
pipeline
├── rag_system.py             # Interactive CLI app — real-time Q&A session
├── langchain_samples/        # Domain documents folder
│   ├── langchain_tips.txt
│   ├── python_guide.txt
│   └── sample_docs.txt
├── rag_db/                   # Chroma vector store (auto-generated)
├── .env                      # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/felixsamuel1640/task-6.git
cd task-6
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API keys
Create a `.env` file in the root directory:
```
COHERE_API_KEY=your_cohere_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free keys at [cohere.com](https://cohere.com) and 
[console.groq.com](https://console.groq.com)

### 4. Add your documents
Place your `.txt` files inside the `langchain_samples/` folder.

### 5. Run the notebook
```bash
jupyter notebook rag_notebook.ipynb
```

### 6. Or run the interactive app
```bash
python rag_system.py
```

---

## 🖥️ Interactive Q&A App (`rag_system.py`)

In addition to the notebook, this project includes a standalone interactive CLI 
application that lets you query your documents in real time.

### What to expect
```
**** SYSTEM 1: Indexing Phase ****
✅Successfully loaded 3 documents
✅Created 25 chunks from 3 documents
✅RAG chain assembled

**** RAG System Ready ****
(type 'exit' or 'quit' to end session)
enter prompt: What is the remote work policy?

🔍Searching document...

💡Answer
Employees may work remotely up to 3 days per week...

**** Retrieved Chunks ****
1. Source: langchain_samples/company_handbook.txt
```

### How it differs from the notebook

| | `rag_notebook.ipynb` | `rag_system.py` |
|---|---|---|
| Purpose | Step-by-step documented demo | Real-time interactive use |
| Input | Predefined test queries | Live user input |
| Output | Inline notebook cells | CLI streaming output |
| Best for | Presentation & evaluation | Practical usage |

---

## 📦 Requirements

```
langchain
langchain-community
langchain-cohere
langchain-groq
langchain-chroma
chromadb
python-dotenv
```

---

## 🧪 Evaluation & Test Results

The system was tested with 5 domain-specific queries and 1 out-of-scope query:

| # | Query | Result |
|---|-------|--------|
| 1 | What is the company policy on remote work? | ✅ Answered correctly |
| 2 | How do I set up a LangChain agent? | ✅ Answered correctly |
| 3 | What Python frameworks are used for data science? | ✅ Answered correctly |
| 4 | Summarize the vacation and remote work policies. | ✅ Multi-doc summarization 
worked |
| 5 | List the recommended steps for building a RAG system using LangChain. | ✅ 
Answered correctly |
| 6 | Out-of-scope question (unrelated topic) | ✅ Returned fallback message |

### Hallucination Prevention
When asked a question outside the document scope, the system responds:
> *"I don't have that information in the document."*

---

## 🔑 Key Design Decisions

- **Cohere Embeddings** — High quality semantic embeddings with a generous free 
tier
- **Groq LLM** — Fast inference with LLaMA 3.1, ideal for development and testing
- **Chroma with persistence** — Vector store is saved locally so embeddings aren't 
regenerated on every run
- **Chunk overlap (50 tokens)** — Ensures context isn't lost at chunk boundaries
- **Top-5 retrieval (notebook) / Top-3 (CLI)** — Tuned per use case

### `.stream()` over `.invoke()`
Both implementations initially used `.invoke()` which waits for the full response 
before printing. The final implementation opts for `.stream()` instead, which 
yields tokens progressively as they are generated — giving a typewriter-style 
output that feels more responsive. Response chunks are accumulated into a single 
string so downstream logic (such as the hallucination fallback check) still works 
as expected. Retrieval via the vector store still uses `.invoke()` since document 
fetching is not a streaming operation.

---

## 💡 How to Use With Your Own Documents

1. Replace the `.txt` files in `langchain_samples/` with your own documents
2. Delete the `rag_db/` folder to force re-embedding
3. Run the notebook or CLI app from the top
4. Update the test queries in the evaluation section to match your domain

---

## 🚧 Known Limitations

- Only supports `.txt` files currently (can be extended to PDF, CSV, etc.)
- No chat history / multi-turn conversation support
- Retrieval quality depends on document quality and chunk size tuning

---

## 👤 Author

**Your Name**
[GitHub](https://github.com/felixsamuel1640) ·

