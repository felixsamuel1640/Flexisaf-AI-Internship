import os
import shutil
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma

from dotenv import load_dotenv

load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# ===========================================================================
# SYSTEM 1: INDEXING PHASE
# ===========================================================================

# Step 1: Load documents from directory
print("**** SYSTEM 1: Indexing Phase ****\n")
loader = DirectoryLoader(
    'langchain_samples',
    glob='**/*.txt',
    loader_cls=TextLoader
)

document = loader.load()
print(f"✅Successfully loaded {len(document)} documents\n")

# Show loaded documents
print("** Documents loaded **")
for i, doc in enumerate(document, 1):
    print(f"{i}. {doc.metadata['source']}")

# Step 2: Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True
)

chunks = text_splitter.split_documents(document)
print(f"\n✅Created {len(chunks)} chunks from {len(document)} documents")

# Add chunk ID for tracking
for i, chunk in enumerate(chunks, 1):
    chunk.metadata['chunk_id'] = i

# Show sample chunks
print("\n*** Sample chunks (first 3) ***")
for i, chunk in enumerate(chunks[:3], 1):
    print(f"\n    Chunk {i}")
    print(f"    Source: {chunk.metadata['source']}")
    print(f"    Length: {len(chunk.page_content)} characters")
    print(f"    Preview:{chunk.page_content[:100]}")

# Step 3: Create embeddings and vectore store
try:
    embeddings = CohereEmbeddings(
        model='embed-english-v3.0',
        cohere_api_key=os.getenv('COHERE_API_KEY')
    )
    print("✅Embedding created")
except Exception as e:
    print(f"❌Failed to create embedding - {e}")
    exit(1)

# Check if the database already exists
db_path = './rag_db'

if Path(db_path).exists():
    print("**** Loading existing database ****")
    vectorstore = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    print(f"Loaded existing vectorstore with {len(chunks)} chunks")
else:
    print("**** Creating new vector store ****")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print(f"✅Vector database created and saved {db_path}")

# ===========================================================================
# SYSTEM 2: RETRIEVAL PHASE
# ===========================================================================

print("\nSYSTEM 2: Retrieval Configuration")

# Creating retriever that returns top-3 most relevant chunks
retrieval = vectorstore.as_retriever(
    search_kwargs={'k': 3}  # Returns top-3 chunks
)
print("✅Retriever configured")


# ===========================================================================
# SYSTEM 3:  GENERATION PHASE
# ===========================================================================

# Create RAG prompt template
rag_prompt = ChatPromptTemplate.from_template("""
You are a strict based-document assistant.

Answer the question based ONLY on the following context.

Context:
{context}

Question:
{question}

Answer: Provide a clear answer based on the context above.
If the context doesn't contain the answer,
simply say 'I don't have that information in the document'. 

""")

# Initializing LLM
groq_llm = ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=0
)
parser = StrOutputParser()

# Build RAG chain
def format_docs(docs):
    """Format retrieved documents into context string"""
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retrieval | format_docs,
        "question": RunnablePassthrough()
    }
    | rag_prompt | groq_llm | parser
)
print("✅RAG chain assembled")

print("\n**** RAG System Ready ****")

# ===========================================================================
# INTERACTIVE Q&A LOOP
# ===========================================================================
while True:
    print("(type 'exit' or 'quit' to end session)")
    user_input = input("enter prompt: ").strip()

    if not user_input:
        print("Enter a prompt")
        continue

    if user_input.lower() in ['exit', 'quit']:
        print("Session Ended. Thank you for using RAG Q&A system")
        break

    try:
        print("🔍Searching document...")

        print("\n💡Answer")

        response = ""

        for chunk in rag_chain.stream(user_input):
            print(chunk, end="", flush=True)
            response += chunk

        print()

        # Get retrieved documents seperately
        retrieved_docs = retrieval.invoke(user_input)
        if "I don't have" not in response:
            print("\n**** Retrieved Chunks ****")
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"{i}. Source: {doc.metadata['source']}")

    except Exception as e:
        print(f"❌ERROR...Failed to process question")
        print("Please try again")








