from typing import TypedDict
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek
from langchain.messages import SystemMessage, HumanMessage

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    groq_api_key: SecretStr

try:
    settings = Config()
except Exception as e:
    print(f"FAILED TO LOAD API: {e}")
    settings = None

class DocumentState(TypedDict):
    raw_documents: str
    summary: str
    analysis: str
    is_valid: bool # Track if the document is worth processing

llm = ChatGroq(
    groq_api_key=settings.groq_api_key.get_secret_value(),
    model="openai/gpt-oss-120b",
    #model="llama-3.3-70b-versatile",
    temperature=0.7
)


def check_document_node(state: DocumentState):
    print("----- Step 1: Checking if document is valid")
    text = state.get("raw_documents", "")

    if len(text) < 10:
        return {"is_valid": False}
    return {"is_valid": True}

def summarize_node(state: DocumentState):
    print("----- Step 2: Summarizing")
    system_message = SystemMessage( content="You are a professional editor. Summarize the following text into 2 sentences")

    user_content = HumanMessage(content=state["raw_documents"])

    response = llm.invoke([system_message, user_content])
    return {"summary": response.content}

def analyze_node(state: DocumentState):
    print("----- Step 3: Analyzing for risks -----")

    system_prompt = SystemMessage(
        content="""You are a risk auditor. 
        Analyze the summary for any legal for any legal, financial or urgent risks.
        Format your response as:
        RISK LEVEL: [High/Low]
        REASON: [Your explanation]
        """)

    user_content = HumanMessage(content=state["summary"])
    response = llm.invoke([system_prompt, user_content])
    return {"analysis": response.content}

def route_after_check(state: DocumentState):
    if state["is_valid"]:
        return "summarize_node"
    return "end"

building = StateGraph(DocumentState)

building.add_node("check_doc", check_document_node)
building.add_node("summarize_node", summarize_node)
building.add_node("analyze_node", analyze_node)

building.add_edge(START, "check_doc")

building.add_conditional_edges(
    "check_doc",
    route_after_check,
    {
        "summarize_node": "summarize_node",
        "end": END
    }
)

building.add_edge("summarize_node", "analyze_node")
building.add_edge("analyze_node", END)

doc_assistant = building.compile()

good_input = {"raw_documents": "Urgent: We need to transfer one Million dollars to the Berlin office."}
final_state = doc_assistant.invoke(good_input)
print(final_state.get("summary"))
print()
print(final_state.get("analysis"))

# This generates the "blueprint" of your graph
print("\n--- COPY THE CODE BELOW FOR YOUR DIAGRAM ---")
print(doc_assistant.get_graph().draw_mermaid())


