# Aura-Med: Stateful AI Health Agent for Maternal & Elderly Care

Aura-Med is a stateful, multi-agent conversational assistant built using **LangGraph**, 
**Python**, and **Llama 3.3 (via Groq)**. It is designed to provide warm, empathic health 
support while maintaining a strict safety-first triage system for medical emergencies.

---

## Key Engineering Highlights

- **Stateful Persistence** — Integrated SQLite checkpointers to maintain user context (names, 
conditions, history) across multiple sessions.
- **Deterministic Safety Triage** — Implemented a non-LLM-based intent analyzer to catch 
emergency keywords (pain, falls, hurt), ensuring immediate, hard-coded safety instructions that 
bypass AI hallucinations.
- **Autonomous Memory Summarization** — Developed a background node that automatically 
compresses long conversation histories into summaries once a message threshold is reached, 
optimizing token usage and performance.
- **Modular Node Architecture** — Designed separate specialized nodes for General Chat, 
Medication Scheduling, and Emergency Response for high maintainability.

---

## Architecture

The agent follows a Directed Acyclic Graph (DAG) structure:

1. **Intent Node** — Analyzes the user's input.
2. **Router** — Directs the flow to either `emergency_node`, `meds_node`, or `chat_node`.
3. **Summarize Node** — *(Conditional)* Triggered when history exceeds 6 messages to prune the 
state while keeping the conversation context intact.

---

## Technical Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph / LangChain |
| Inference Engine | Groq (Llama-3.3-70b-versatile) |
| Database | SQLite |
| Configuration | Pydantic Settings (secure API management) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Groq API Key

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/aura-med.git
cd aura-med
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

**4. Run the terminal test**

```bash
python main.py
```

---

## 🧠 System in Action

| Emergency Triage | Medication Management | Stateful Memory |
| :---: | :---: | :---: |
| ![Emergency](aura_emergency_triage.png) | ![Meds](aura_meds_knowledge_injection.png) | 
![Memory](aura_stateful_conversation.png) |
| **Safety Guardrails** | **Structured Knowledge** | **Context Persistence** |

---

## Demo Output

```
Mum: Hi Aura, my name is Bisola and I am pregnant.
Aura: Dear Bisola, congratulations! To keep fit, I recommend short walks. Are you drinking 
enough water?

Mum: Do you remember my name?
Aura: Dear, your name is Bisola, and you're a lovely pregnant mum. How are you feeling today?
```

---

## Future Roadmap

- [ ] Integration with a real-time Medication API.
- [ ] Multi-user authentication.
- [ ] Voice-to-text integration for elderly accessibility.

---

*Developer: felixsamuel1640 — AI Engineering Intern*
