from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from functools import lru_cache, cached_property
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq

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

llm_model = ChatGroq(
    groq_api_key=settings.groq_api_key.get_secret_value(),
    model=settings.model_name,
    temperature=1.0
)

SYSTEM_PROMPT = """
You are a conventional AI assistant designed to demonstrate memory in a chatbot system.

## ROLE
Provide helpful, accurate, and context-aware responses.

## MEMORY BEHAVIOUR
- Maintain conversation context across all turns.
- Remember and reuse user-provided information (name, preferences, etc.).
- When asked, provide a clear summary of prior conversation.
- Ensure continuity in dialogue.

## RESPONSE RULES
- Be concise but informative.
- If unsure, say: "I don't know."
- Do not hallucinate or fabricate information.
- Ask relevant follow-up questions when appropriate.

## STYLE
- Friendly, natural, and professional
- Clear and structured when needed
"""

agent = create_agent(
    model=llm_model,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id": "chat-1"}}

while True:
    user_input = input("You: ")

    if not user_input:
        continue


    if user_input.lower() in ['exit', 'quit']:
        print("Ending session..")
        break

    print("Assistant: ", end="", flush=True)

    # ----- ADDED TRY/EXCEPT HERE -----
    try:

        for token, metadata in agent.stream(
                {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            if token.content:
                print(token.content, end="", flush=True)

        print() # New line after streaming

    except Exception as e:
        print(f"\n[SYSTEM ERROR]: I encountered a problem connecting to the brain. Details: {str(e)}")
        print("Please check your internet connection or API quota")
