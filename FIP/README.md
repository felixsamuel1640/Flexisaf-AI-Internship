# FlexiSaf Academy 'Super Agent' Assistant

---

## Project Overview

The FlexiSaf Academy AI Assistant is a state-of-the-art, autonomous support system designed to 
handle complex school-related inquiries. Built using a modern Agentic Framework, this assistant 
goes beyond simple chatbots by dynamically reasoning through school policies, fee structures, 
and admission guidelines to provide accurate, context-aware responses.

---

## Key Features & Technical Innovation

### 1. Agentic Reasoning (Modern LangChain)

This project utilizes the latest LangGraph-driven Agent patterns:

- **Dynamic Decision Making** — The agent evaluates user intent and decides autonomously whether 
to chat directly or invoke the `query_school_knowledge` tool.
- **Autonomous Tool-Use** — Using the `create_agent` architecture, the LLM is equipped to browse 
internal school documents only when factual data is required.

### 2. Advanced Hybrid Retrieval (RAG)

To ensure the highest accuracy, the system implements a Hybrid RAG pipeline:

- **Semantic Search** — Uses Cohere v3 Embeddings and ChromaDB to understand the deep context of 
parent queries.
- **Keyword Search** — Utilizes BM25 for precise matching of specific terms (e.g., "JSS1", 
"Admission Form").
- **Reciprocal Rank Fusion (RRF)** — Results are mathematically merged using an 
`EnsembleRetriever` to prioritize the most relevant information from both search methods.

### 3. Non-Blocking Asynchronous Streaming

The core loop is built on `asyncio` using `astream`:

- **Real-time UX** — Tokens are streamed to the terminal as they are generated for a smooth 
"live typing" experience.
- **Attribute Safety** — Implements robust attribute-checking (`hasattr`) to safely handle the 
transition between the agent's internal reasoning and final responses.

### 4. Stateful Conversational Memory

Using `InMemorySaver` with unique `thread_id` tracking, the assistant maintains a Short-Term 
Memory, allowing it to recall names and context across a multi-turn dialogue.

---

## Technical Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B (via Groq Cloud) |
| Orchestration | LangGraph & LangChain (Agentic Pattern) |
| Embeddings | Cohere English v3.0 |
| Vector Store | ChromaDB |
| Data Processing | PyMuPDF (Directory Loading) |
| Runtime | Python 3.11+ (Asynchronous Programming) |

---

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/felixsamuel1640/Flexisaf-AI-Internship.git
cd Flexisaf-AI-Internship/FIP
```

**2. Install dependencies**

```bash
pip install langchain-groq langchain-cohere langchain-chroma pymupdf pydantic-settings langgraph
```

**3. Configure environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
COHERE_API_KEY=your_api_key_here
```

**4. Prepare your data**

Place school-related PDF documents in the `untitled_folder/` directory.

**5. Launch the assistant**

```bash
python final_project.py
```

---

## Admin Testing Suite

To verify the capabilities of the Super Agent, use the following prompts:

| Category | Test Prompt | Expected Behavior |
|---|---|---|
| Accuracy | "What are the tuition fees for Grade 3 for the 2026 session?" | Agent triggers 
`query_school_knowledge` and pulls data from PDFs. |
| Memory | "Hi, I am Mr. Musa. My daughter Zara is 5 years old." then "What class should Zara 
join?" | Agent remembers names and age to suggest the correct class. |
| Reasoning | "How are you today?" | Agent responds conversationally without using the RAG tool. 
|
| Guardrails | "How do I bake a cake?" | Agent politely declines, staying within its role as a 
school assistant. |
| Streaming | "Summarize the school's entire code of conduct." | Observe real-time token 
streaming for long responses. |

---

*Developed as part of the FlexiSaf AI Internship Program — Final Project.*
