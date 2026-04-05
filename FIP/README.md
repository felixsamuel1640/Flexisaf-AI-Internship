# FlexiSaf Academy 'Super Agent' Assistant

---

## Project Overview

The FlexiSaf Academy AI Assistant is a state-of-the-art, autonomous support system designed to 
handle complex school-related inquiries. Built using a modern Agentic Framework, this assistant 
goes beyond simple chatbots by dynamically reasoning through school policies, fee structures, 
and admission guidelines to provide accurate, context-aware responses.

---

## Key Features & Technical Innovation

- **Agentic Reasoning (LangGraph)** — The agent autonomously decides whether to answer from its 
own internal logic or invoke the `query_school_knowledge` tool to browse school documents.
- **Hybrid Retrieval (RAG)** — Combines Semantic Search (Cohere v3 Embeddings + ChromaDB) with 
Keyword Search (BM25) using Reciprocal Rank Fusion (RRF) for maximum accuracy.
- **Stateful Conversational Memory** — Uses `InMemorySaver` with unique `thread_id` tracking to 
maintain context, remember user names, and summarize prior conversation turns.
- **Asynchronous Streaming** — Built with `asyncio` to provide a real-time, "live typing" user 
experience in the terminal.

---

## Technical Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B (via Groq Cloud) |
| Orchestration | LangGraph & LangChain |
| Embeddings | Cohere English v3.0 |
| Vector Store | ChromaDB |
| Data Processing | PyMuPDF |
| Runtime | Python 3.11+ |

---

## Project Structure

| File / Folder | Description |
|---|---|
| `FINAL_PROJECT.py` | Main asynchronous production script |
| `Final_Project_Notebook.ipynb` | Interactive notebook showing data exploration and RAG 
pipeline steps |
| `screenshots/` | Visual proof of the agent's performance, tool-calling, and memory |
| `untitled_folder/` | Directory containing source PDF documents (Knowledge Base) |

---

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/felixsamuel1640/Flexisaf-AI-Internship.git
cd Flexisaf-AI-Internship/task-12
```

**2. Install dependencies**

```bash
pip install langchain-groq langchain-cohere langchain-chroma pymupdf pydantic-settings langgraph 
nest_asyncio
```

**3. Configure environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
COHERE_API_KEY=your_api_key_here
```

---

## How to Run the Project

### Command Line Interface (CLI)

For the full asynchronous streaming experience with real-time terminal output:

```bash
python final_project.py
```

### Interactive Jupyter Notebook

To see the step-by-step logic and model usage:

1. Open `final_project_notebook.ipynb`.
2. Run all cells sequentially to view the pre-saved outputs and the interactive chat loop at the 
bottom.
---

## Capability Testing Suite

Use these prompts to verify the agent's sophisticated behavior:

| Category | Test Prompt | Expected Behavior |
|---|---|---|
| Accuracy | "What are the tuition fees for Grade 3 for the 2026 session?" | Agent triggers 
`query_school_knowledge` and extracts PDF data. |
| Memory | "My name is Mr. Samuel and my daughter is Aisha." then "What was my name?" | Agent 
recalls user-provided details across multiple turns. |
| Reasoning | "Who are you and what can you do?" | Agent responds via System Prompt without 
using the RAG tool. |
| Guardrails | "How do I bake a cake?" | Agent politely stays within its role as a school 
assistant. |

---

*Developed as the Final Project for the FlexiSaf AI Engineering Internship.*
