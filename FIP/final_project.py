import os
import asyncio

from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Data Loading and Handling
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Retrieval (The Hybrid Part)
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# AI & Vector Database
from langchain.messages import SystemMessage, HumanMessage
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_cohere import CohereEmbeddings

# Agents & Tools
from langchain.agents import create_agent
from langchain_core.tools import tool

# Memory
import sqlite3
from langgraph.checkpoint.memory import InMemorySaver



# 1. --------------------------- CONFIGURATION ---------------------------
class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False
    )

    groq_api_key: SecretStr
    cohere_api_key: SecretStr

try:
    settings = Config()
    llm = ChatGroq(groq_api_key=settings.groq_api_key.get_secret_value(), model="llama-3.3-70b-versatile", temperature=0.0)
except Exception as e:
    print(f"Failed to load API: {str(e)}")

# 2. RAG SETUP (The Knowledge Base)
def prepare_retriever():
    loader = DirectoryLoader("untitled_folder", glob="**/*.pdf", loader_cls=PyMuPDFLoader, show_progress=True)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_chunk = text_splitter.split_documents(docs)

    try:
        vector_embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=settings.cohere_api_key.get_secret_value())
        print("✅Embeddings Initialized Successfully")
    except Exception as e:
        print(f"❌Failed to load embeddings: {str(e)}")

    db_path = "./final_project"
    if Path(db_path).exists():
        vectorstore = Chroma(
            persist_directory=db_path,
            embedding_function=vector_embeddings
        )
        print(f"Loaded existing database from {db_path}")
    else:
        vectorstore = Chroma.from_documents(
            documents=split_chunk,
            embedding=vector_embeddings,
            persist_directory=db_path
        )
        print(f"Vectorstore database created and stored in: {db_path}.")
    # Hybrid Set Up
    bm25 = BM25Retriever.from_documents(split_chunk)
    bm25.k = 2
    vectorstore_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # This combines them mathematically using Reciprocal Rank Fusion (RRF)
    ensemble = EnsembleRetriever(retrievers=[bm25, vectorstore_retriever], weights=[0.5, 0.5])

    return ensemble

ensemble_retriever = prepare_retriever()

@tool
def query_school_knowledge(query: str) -> str:
    """Consult this tool for ANY questions about Flexisaf Academy policies,
        fees, admissions, calendar or rules."""
    docs = ensemble_retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

SYSTEM_PROMPT = """
You are the official FlexiSaf Academy AI Assistant.

## ROLE
Provide helpful, accurate, and context-aware responses.

## RULES
1. Always use the 'query_school_knowledge' tool if the user asks about school details.
2. If the info isn't in the tool, simply say you don't know

## MEMORY BEHAVIOUR
1. Maintain conversational context across all turns.
2. Remember and re-use user provided information (like names, or prebious questions)
3. When asked, provide a clear summary of prior conversation.
4. Ensure continuity in dialogue

## RESPONSE RULES
1. Do not fabricate or hallucinate information
2. Be concise but informative
"""

# 4. Create the stateful Agent
memory = InMemorySaver()

agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=[query_school_knowledge],
    checkpointer=memory
)

# 5. RUN THE LOOP
async def main():
    config= {"configurable": {"thread_id": "chat-1"}}
    print("\nFlexisaf Academy 'Super Agent' Online (With Memory & RAG)\n")

    while True:
        user_input = input("Enter prompt: ")

        if user_input.lower() in ["quit", "exit"]: break

        if not user_input: continue

        print("Assistant: ", end="", flush=True)

        async for chunk in agent.astream(
                {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            if hasattr(chunk[0], 'content') and chunk[0].content:
                print(chunk[0].content, end="", flush=True)

            #if chunk[0].content:
            #    print(chunk[0].content, end="", flush=True)
        print()

if __name__ == "__main__":
    asyncio.run(main())