# Task 13: AI Proxy Bridge (Spring Boot + LangGraph)

## 🚀 Overview
A cross-language AI implementation demonstrating the **Proxy Design Pattern**.  
This project bridges a Java-based enterprise gateway with a Python-based intelligent reasoning engine.

## 🏗️ Architecture

### Java (Spring Boot)
Acts as the **REST Proxy**.  
Handles incoming user requests and communicates with the AI backend using `RestTemplate`.

### Python (FastAPI + LangGraph)
Acts as the **Inference Engine**.  
Uses a **ReAct Agent pattern** to perform arithmetic operations via the **Llama-3.3-70b** model.

## 🛠️ Tech Stack

- **Backend:** Java 17, Spring Boot  
- **AI Framework:** LangGraph, LangChain  
- **LLM:** Groq (Llama-3.3-70b-versatile)  
- **Communication:** REST (JSON over HTTP)

## 🚦 How to Run

### 1. Start Python Service
```bash
python main.py
Starts FastAPI on port 8000.

### 2. Start Java Gateway
```bash
mvn spring-boot:run
Starts Gateway on port 8080.

### 3. Test the System
Send a POST request to:
http://localhost:8080/ai-query
Include a math question in the request body.
