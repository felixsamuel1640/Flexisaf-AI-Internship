# 🤖 Stateful AI Assistant: LangGraph & Pydantic-Driven Architecture

This project is a high-performance, **stateful chatbot** demonstration developed 
for an AI Engineering internship. It fulfills the core requirement of maintaining 
**session history** and **contextual awareness** across multiple conversational 
turns using modern industry standards.

---

## 🎯 Internship Project Goals

- **Stateful Persistence:** Maintain memory across infinite turns within a single 
thread.
- **Production Configuration:** Shift from "scripting" (dotenv) to "engineering" 
(Pydantic Settings).
- **Real-Time UX:** Implement token-based streaming for a responsive interface.
- **Security:** Ensure API keys are validated and masked using `SecretStr`.

---

## 🏗️ Technical Architecture

### 1. The State Machine (LangGraph)

Unlike standard LLM calls that "forget" the previous message, this assistant uses 
**LangGraph's `InMemorySaver`**.

- **Checkpointing:** Every message is saved to a "checkpoint" linked to a 
`thread_id`.
- **Context Retrieval:** When a new message arrives, the system automatically 
injects the relevant history before the LLM processes the prompt.
- **Thread Isolation:** Different `thread_id` values can represent different users 
or separate sessions, ensuring no data leakage.

### 2. Validated Configuration (Pydantic V2)

We have implemented a `BaseSettings` class to handle environment variables. This is 
a significant step up from `os.getenv` for three reasons:

1. **Fail-Fast Validation:** If `GROQ_API_KEY` is missing from the `.env` file, the 
app crashes instantly with a clear error rather than failing later during a call.
2. **Secret Masking:** Using `SecretStr` prevents the API key from appearing in 
plain text if the configuration is logged or printed.
3. **Automatic Parsing:** Pydantic handles type conversion (e.g., a string `"True"` 
in `.env` becomes a Python `True` boolean).

---

## 🚀 Installation & Setup

### 1. Prerequisites

Ensure you have **Python 3.10+** installed.

### 2. Install Dependencies

```bash
pip install langchain-groq pydantic-settings langgraph
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
# Required for LLM Inference
GROQ_API_KEY=gsk_your_actual_key_here

# App Settings
ENVIRONMENT=development
```

---

## 💻 Implementation Details

### The "Smart" Configuration Object

```python
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env_name: str = Field(default="dev")
    groq_api_key: SecretStr

    @property
    def model_name(self) -> str:
        """Automatically pick the model based on the environment."""
        if self.env_name == "prod":
            return "llama-3.3-70b-versatile"
        return "openai/gpt-oss-120b"

@lru_cache
def get_settings():
    print("Reading .env")
    return Config()

settings = get_settings()
```

The `@lru_cache` on `get_settings()` ensures the `.env` file is only read **once** 
per process, no matter how many times `get_settings()` is called. The `model_name` 
property also allows the model to be swapped automatically based on the `ENV_NAME` 
variable — no manual changes needed when deploying.

### The Stateful Agent

```python
agent = create_agent(
    model=llm_model,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()  # This provides the 'Memory'
)
```

---

## 🧪 Testing the Stateful Memory

To verify that the chatbot maintains context, follow this test script in the 
terminal:

```
You: Hi, I'm Sarah and I'm a Data Scientist.
Assistant: Hello Sarah! Nice to meet a Data Scientist. How can I help you today?

You: What was the first thing I told you?
Assistant: You introduced yourself as Sarah and mentioned that you're a Data 
Scientist.
```

---

## 🛠️ Operational Features

- **Streaming Output:** Tokens are flushed to the terminal as they are generated 
for a "live" feel.
- **Graceful Exit:** Supports `exit` and `quit` commands to close the session 
cleanly.
- **Error Handling:** `try/except` blocks around LLM invocations to prevent silent 
crashes.

---

## 📄 License & Disclaimer

This project is for educational/internship purposes. Ensure you rotate your API 
keys regularly and **never commit your `.env` file to version control**.

---

**Author:** [@felixsamuel1640](https://github.com/felixsamuel1640)
