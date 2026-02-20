
import os
import time

from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from pathlib import Path
import shutil

from dotenv import load_dotenv
load_dotenv()

os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

# Step 1: Create Embedding Model
try:
    embeddings = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv('COHERE_API_KEY')
    )

    print("✅Embedding model created successfully")
    time.sleep(1.5)

except Exception as e:
    print(f"❌Error initializinf embedding {e}")

# Step 2: Create Document Dataset
document = [
    # Programming & Development
    "Python is a high-level programming language widely used for web development, data science, and automation",
    "JavaScript is the primary language for frontend web development and runs in web browsers",
    "React is a JavaScript library for building interactive user interfaces with reusable components",

    # AI & Machine Learning
    "Machine learning trains algorithms to learn patterns from data and make predictions without explicit programming",
    "Deep learning uses neural networks with multiple layers to process complex patterns in large datasets",
    "LangChain is a framework for developing applications powered by large language models",
    "Vector databases like ChromaDB and FAISS store embeddings for efficient semantic similarity search",

    # DevOps & Infrastructure
    "Docker containers package applications with dependencies for consistent deployment across environments",
    "Kubernetes orchestrates containerized applications, managing scaling and deployment automatically",
    "CI/CD pipelines automate testing and deployment for faster software releases",

    # Databases
    "SQL databases use structured schemas and ACID properties for reliable transaction processing",
    "NoSQL databases like MongoDB offer flexible schemas for unstructured data with horizontal scaling",
    "Redis is an in-memory data store used for caching and real-time applications"
]

print(f"Dataset created with {len(document)} documents")
print("Categories: Programming, AI/ML, DevOps, Docker")

# Step 3: Cleaning old Database and creating a new one

# Clean up old database for fresh start
db_path = "./chroma_db"
if Path(db_path).exists():
    shutil.rmtree(db_path)
    print("🗑 Existing Database Cleaned")

# Creating a new Vector Database(Chroma)
vectorstore = Chroma.from_texts(
    texts=document,
    embedding=embeddings,
    persist_directory=db_path
)

print(f"{len(document)} Documents indexed and stored")

# Step 4: Demonstrating Semantic Search
test_queries = [
    "What tools help build AI applications?",
    "How do I deploy and scale my application?",
    "What programming language is best for data science?",
    "Which database should I use for caching?"
]

for query_num, query in enumerate(test_queries, 1):
    print(f"{query_num} - {query}")

    result = vectorstore.similarity_search_with_score(query, k=3)


    for rank, (doc, score) in enumerate(result, 1):
        similarity_percent = max(0, min(100, 100 - (score * 20)))

        print("Fetching results...")
        time.sleep(1.0)

        print(f" Rank: {rank}, (Similarity: {similarity_percent:,.1f}% | Distance: {score:,.4f})")
        print(f" └ {doc.page_content}")
