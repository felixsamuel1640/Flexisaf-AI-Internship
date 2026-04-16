from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition


# 1. SETTINGS & LLM SETUP
class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="", case_sensitive=False
    )
    groq_api_key: SecretStr


settings = Config()
llm = ChatGroq(
    groq_api_key=settings.groq_api_key.get_secret_value(),
    model="llama-3.3-70b-versatile",
    temperature=0.2
)


# 2. TOOLS
def multiply(a: int, b: int) -> float:
    """Multiply a and b"""
    return a * b


def add(a: int, b: int) -> float:
    """Add a and b"""
    return a + b


def divide(a: int, b: int) -> float:
    """Divide a by b"""
    return a / b


tools = [multiply, add, divide]
llm_with_tools = llm.bind_tools(tools)

# 3. THE GRAPH (THE BRAIN)
sys_message = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic.")


async def assistant(state: MessagesState):
    # This is the function that actually calls the LLM
    response = await llm_with_tools.ainvoke([sys_message] + state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
react_graph = builder.compile(checkpointer=memory)

# 4. THE REST API (THE BODY)
app = FastAPI()


class ChatInput(BaseModel):
    question: str


@app.post("/ask")
async def ask_agent(input_data: ChatInput):

    config = {"configurable": {"thread_id": "chat-1"}}
    # This wraps your chatbot logic into a JSON response
    messages = [HumanMessage(content=input_data.question)]
    result = await react_graph.ainvoke({"messages": messages}, config=config)
    final_answer = result['messages'][-1].content

    return {
        "status": "success",
        "agent_response": final_answer
    }
