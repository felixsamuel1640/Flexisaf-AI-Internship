# Semantic Similarity Search with ChromaDB

**Module 5 Deliverable - Vector Databases**

## Overview

This project demonstrates semantic similarity search using ChromaDB vector database 
and Cohere embeddings. The system retrieves relevant documents based on meaning 
rather than exact keyword matching.

## Features

- Vector Database Storage: ChromaDB for efficient document indexing
- Semantic Embeddings: Cohere embed-english-v3.0 model
- 13-Document Dataset: Organized across 4 technical categories
- Top-3 Retrieval: Returns most similar documents with similarity scores
- Automatic Database Refresh: Cleans old data for consistent results
- Error Handling: Graceful failure management for API initialization

## Tech Stack

- Python 3.11
- LangChain Chroma: Vector database integration
- LangChain Cohere: Embedding model integration
- ChromaDB: Vector storage and retrieval
- Cohere API: Text-to-vector embeddings

## Installation
```bash
pip install langchain-chroma langchain-cohere python-dotenv
```

## Setup

1. Create a `.env` file in the project directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
```

2. Get your free Cohere API key from: https://cohere.com/

## Usage

Run the script:
```bash
python app.py
```

### Execution Flow

1. Initializes Cohere embeddings model
2. Creates a 13-document dataset across 4 categories
3. Cleans existing ChromaDB database (if any)
4. Stores documents as vector embeddings in ChromaDB
5. Executes 4 test queries demonstrating semantic search
6. Displays top-3 results with similarity percentages and distance scores

## Test Queries

The system runs these queries to demonstrate semantic understanding:

| Query # | Question | Expected Top Result |
|---------|----------|---------------------|
| 1 | "What tools help build AI applications?" | LangChain |
| 2 | "How do I deploy and scale my application?" | Kubernetes |
| 3 | "What programming language is best for data science?" | Python |
| 4 | "Which database should I use for caching?" | Redis |

## Sample Results
```
1 - What tools help build AI applications?
Fetching results...
 Rank: 1, (Similarity: 77.9% | Distance: 1.1035)
 └ LangChain is a framework for developing applications powered by large language 
models

2 - How do I deploy and scale my application?
Fetching results...
 Rank: 1, (Similarity: 79.5% | Distance: 1.0232)
 └ Kubernetes orchestrates containerized applications, managing scaling...

3 - What programming language is best for data science?
Fetching results...
 Rank: 1, (Similarity: 78.7% | Distance: 1.0655)
 └ Python is a high-level programming language widely used for...

4 - Which database should I use for caching?
Fetching results...
 Rank: 1, (Similarity: 76.0% | Distance: 1.1981)
 └ Redis is an in-memory data store used for caching and real-time applications
```

## How It Works

### 1. Document Embedding
Documents are converted to 1024-dimensional vectors using Cohere's embedding model. 
Similar documents have similar vector representations.

### 2. Vector Storage
Embeddings are stored in ChromaDB, which indexes them for fast similarity searches.

### 3. Query Processing
Search queries are also converted to vectors using the same embedding model.

### 4. Similarity Calculation
ChromaDB calculates distance scores between the query vector and all stored 
document vectors using cosine similarity.

### 5. Result Ranking
Documents are ranked by similarity (lower distance = higher similarity) and top-K 
results are returned.

## Document Categories

- **Programming & Development**: Python, JavaScript, React
- **AI & Machine Learning**: Machine Learning, Deep Learning, LangChain, Vector 
Databases
- **DevOps & Infrastructure**: Docker, Kubernetes, CI/CD
- **Databases**: SQL, NoSQL (MongoDB), Redis

## Understanding Scores

- **Similarity Percentage**: Higher percentage indicates more relevant results 
(converted from distance)
- **Distance**: Lower distance indicates higher similarity (ChromaDB L2 distance 
metric)
- **Typical Range**: 74-80% similarity indicates strong semantic match

## Key Concepts Demonstrated

- Text-to-vector conversion using embeddings
- Vector database storage and indexing
- Semantic similarity search (meaning-based retrieval)
- Top-K retrieval with ranking
- Distance-to-similarity conversion

## Project Structure
```
.
├── app.py                 # Main application script
├── .env                   # API keys (gitignored)
├── README.md             # Documentation
├── requirements.txt      # Python dependencies
└── chroma_db/            # ChromaDB storage (auto-generated)
```

## Why Semantic Search?

Traditional keyword search looks for exact matches:
- Query: "caching database" → Only finds documents with these exact words

Semantic search understands meaning:
- Query: "Which database should I use for caching?"
- Finds: "Redis is an in-memory data store used for caching..."
- No exact keyword match needed

## Future Enhancements

- Add interactive query input
- Implement persistent database (load vs recreate)
- Add document upload functionality
- Include similarity score visualization
- Add support for larger datasets
- Implement filtering by category

## Notes

- Database is recreated on each run for consistency
- Similarity scores of 75% and above indicate strong semantic relevance
- All test queries successfully retrieve contextually correct documents
- System demonstrates understanding without requiring exact keyword matches

## Learning Outcomes

This project demonstrates understanding of:
- Vector embeddings and their role in semantic search
- Vector database operations (store, index, retrieve)
- Similarity scoring and ranking mechanisms
- Production-ready code structure with error handling

---

**Author:** [Felix Samuel]  
**Date:** February 21, 2026  
**Module:** 5 - Vector Databases

