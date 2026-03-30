from typing import Annotated, TypedDict, Literal
import sqlite3
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_groq import ChatGroq

# --- 1. CONFIGURATION ---
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    groq_api_key: SecretStr

try:
    settings = Config()
    llm = ChatGroq(
        groq_api_key=settings.groq_api_key.get_secret_value(),
        model="llama-3.3-70b-versatile",
        temperature=0.5
    )
except Exception as e:
    print(f"ERROR: Ensure .env file exists with groq_api_key. {e}")
    exit()

# --- 2. STATE DEFINITION ---
class AuraState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    category: str
    critical_flag: bool
    summary: str

# --- 3. NODES & LOGIC ---
def analyze_intent(state: AuraState):
    user_message = state["messages"][-1].content.lower()
    if any(word in user_message for word in ["pain", "hurt", "emergency", "fall"]):
        return {"category": "emergency", "critical_flag": True}
    elif any(word in user_message for word in ["pill", "med", "medication", "dose"]):
        return {"category": "meds", "critical_flag": False}
    else:
        return {"category": "chat", "critical_flag": False}

def chat_node(state: AuraState):
    sys_msg = SystemMessage(content=(
        "You are Aura, a loving and patient medical assistant for 'mum'. "
        "Use warm, empathic language like 'dear' or 'rest up'. "
        "Keep answers short and ask one simple follow-up question at a time."
    ))
    response = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

def meds_node(state: AuraState):
    med_list = "- Lisinopril (8 AM)\n- Vitamin D (12 PM)"
    sys_msg = SystemMessage(content=(
        f"You are Aura. Help Mum with her meds. Schedule:\n{med_list}. "
        "Always remind her to take them with water and be encouraging."
    ))
    response = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

def emergency_node(state: AuraState):
    content = (
        "Mum, I'm deeply concerned by what you just said. "
        "I've flagged this as an emergency and am alerting the care team now. "
        "Please sit down or lie comfortably. I am right here with you. Help is on the way."
    )
    return {"messages": [AIMessage(content=content)], "critical_flag": True}

def summary_node(state: AuraState):
    summary = state.get("summary", "")
    prompt = f"Extend the current summary: {summary}" if summary else "Summarize this conversation."
    messages = state["messages"] + [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    # We keep only the last 2 messages to prevent the context window from exploding
    return {"summary": response.content, "messages": state["messages"][-2:]}
# --- 4. ROUTERS ---
def router_intent(state: AuraState) -> Literal["emergency_node", "meds_node", "chat_node"]:
    return f"{state['category']}_node" if state['category'] in ["emergency", "meds"] else "chat_node"

def should_summarize(state: AuraState) -> Literal["summary_node", "__end__"]:
    if len(state["messages"]) > 6:
        return "summary_node"
    return END

# --- 5. GRAPH CONSTRUCTION ---
workflow = StateGraph(AuraState)

workflow.add_node("intent_node", analyze_intent)
workflow.add_node("chat_node", chat_node)
workflow.add_node("meds_node", meds_node)
workflow.add_node("emergency_node", emergency_node)
workflow.add_node("summary_node", summary_node)

workflow.add_edge(START, "intent_node")
workflow.add_conditional_edges("intent_node", router_intent)

# After chat or meds, check if we need to summarize
workflow.add_conditional_edges("chat_node", should_summarize)
workflow.add_conditional_edges("meds_node", should_summarize)

workflow.add_edge("emergency_node", END)
workflow.add_edge("summary_node", END)

# --- 6. PERSISTENCE & RUN ---
#conn = sqlite3.connect("aura-med_db", check_same_thread=False)
#memory = SqliteSaver(conn)
aura_bot = workflow.compile()

#if __name__ == "__main__":
#    config = {"configurable": {"thread_id": "1"}}
#    print("---- Aura-Med Active ----")
#    with conn:
#    while True:
#        user_input = input("\nMum: ")
#        if user_input.lower() in ['quit', 'exit']: break
#        response = aura_bot.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
#        print(f"Aura: {response['messages'][-1].content}")