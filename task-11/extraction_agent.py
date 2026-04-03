from typing import TypedDict, Optional
from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from langchain_groq import ChatGroq
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import SystemMessage, HumanMessage


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", 
extra="ignore")

    groq_api_key: SecretStr

try:
    settings = Config()
    llm = ChatGroq(
        groq_api_key=settings.groq_api_key.get_secret_value(),
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )
except Exception as e:
    print(f"❌ERROR: Failed to load API: {str(e)}")

# 1. This is the "Target" - What we want the AI to find
class StudentInsight(BaseModel):
    student_name: str = Field(description="The student's name")
    gpa: float = Field(description="student's grade point average")
    subjects: list = Field(description="The list of subjects mentioned")

# 2. This is the brain of the graph - It holds the data as it moves
class ExtractionState(TypedDict):
    raw_text: str          # The text from the PDF
    extracted_data: Optional[StudentInsight] # The AI's result
    manually_verified: bool

def pdf_loader(state: ExtractionState):
    text = state.get("raw_text", "")
    return {"raw_text": text}

def human_feedback(state: ExtractionState):
    pass

structured_llm = llm.with_structured_output(StudentInsight)

def ai_parser(state: ExtractionState):

    # 1. Get the text from the state
    text_to_analyze = state["raw_text"]

    # 2. Ask the AI to find the data
    # We pass the text to our structured LLM
    messages = [
        SystemMessage(content="You are a precise data extractor for FLEXISAF. Extract only valid 
student data."),
        HumanMessage(content=text_to_analyze)
    ]
    result = structured_llm.invoke(messages)

    # 3. Return the result to update the 'extracted_data' key
    return {"extracted_data": result}

# Create the graph
workflow = StateGraph(ExtractionState)

# Add your nodes
workflow.add_node("pdf_loader", pdf_loader)
workflow.add_node("ai_parser", ai_parser)
workflow.add_node("human_feedback", human_feedback)

workflow.add_edge(START, "pdf_loader")
workflow.add_edge("pdf_loader", "human_feedback")
workflow.add_edge("human_feedback", "ai_parser")
workflow.add_edge("ai_parser", END)

# Compile
#memory = MemorySaver()
app = workflow.compile(interrupt_before=["human_feedback"])

# Start the graph

#test_text = """
#Student Progress Report - FlexiSaf International

#After a long deliberation by the board, we are pleased to announce that Bamidele Olusegun has 
completed his junior year. While his attendance was only 85%, his academic results were stellar.

#Bamidele sat for examinations in Further Mathematics, Data Processing, and Technical Drawing. 
Despite a challenging semester in sports, he managed to secure a cumulative grade point average 
of 3.95. He is recommended for a scholarship.
#"""

#thread = {"configurable": {"thread_id": "flexisaf-chat-1"}}

#initial_input = {"raw_text": test_text}

# First run
#for event in app.stream(initial_input, thread, stream_mode="updates"):
#    pass
    #print(f"Node Completed: {list(event.keys())[0]}")

#state = app.get_state(thread)
#print("*** TEXT IN STATE ***")
#print(state.values.get("raw_text"))

#user_confirm = input("\nDoes this text look correct? (y/n): ")

#if user_confirm.lower() in ["no", "n"]:
#    new_text = input("Please paste the correct text: ")

#    app.update_state(thread, {"raw_text": new_text}, as_node="human_feedback")
#    print("✅ State updated with your manual step")

#print("****** Sending to AI for Structured Insights ******")
#for event in app.stream(None, thread):
#    if 'ai_parser' in event:
#        data = event["ai_parser"]["extracted_data"]
#        print("\n--- FINAL STRUCTURED INSIGHTS ---")
#        print(f"Name: {data.student_name}")
#        print(f"GPA: {data.gpa}")
#        print(f"Subjects: {', '.join(data.subjects)}")
