# 🦉 WiseOwl - AI Tutor Chatbot

An intelligent AI-powered tutoring chatbot built with LangChain and Groq AI. 
WiseOwl remembers your conversation context to provide personalized, continuous 
learning support.

## Features

- **Conversation Memory**: Remembers previous messages for contextual responses
- **Multiple Model Support**: Choose between different LLaMA models
- **Clean UI**: Built with Streamlit
- **LangChain Integration**: Uses LCEL (LangChain Expression Language)
- **Fast Inference**: Powered by Groq's optimized infrastructure

## Why Groq AI?

This project uses **Groq AI** instead of OpenAI because:

- **Free Access**: Groq provides free API access to powerful open-source models
- **Speed**: Exceptionally fast inference times
- **Learning-Friendly**: Perfect for internship projects without API costs

## Tech Stack

- Python 3.12+
- LangChain (chain composition and prompt management)
- Groq API (LLM inference)
- Streamlit (web UI)
- python-dotenv (environment variables)

## Installation

### 1. Navigate to the task directory
```bash
cd Flexisaf-AI-Internship/task-3
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your Groq API Key

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Create a new API key

### 5. Set up environment variables

1. Create a `.env` file:
```bash
cp .env.example .env
```

2. Add your API key to `.env`:
```env
GROQ_API_KEY=your-actual-api-key-here
```

**Security Note**: The `.env` file is in `.gitignore` - never commit it to version 
control.

## Usage

### Running the Application
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### How to Use

1. Select a model (llama-3.3-70b-versatile recommended)
2. Type your question and press Enter
3. Continue the conversation - WiseOwl remembers context

## Sample Test Queries

Here are 5 sample queries to test WiseOwl:

1. **Query:** "What is photosynthesis?"

2. **Query:** "Can you explain that in simpler terms?"

3. **Query:** "How do I solve the equation 2x + 5 = 15?"

4. **Query:** "What if the equation was 3x + 5 = 15 instead?"

5. **Query:** "Explain the difference between DNA and RNA"

## Configuration

**Temperature:** 0.7 (balanced for educational content)

**Available Models:**
- `llama-3.3-70b-versatile` - Best quality
- `llama-3.1-8b-instant` - Fastest

## Troubleshooting

**API key error:** Ensure `.env` file exists with `GROQ_API_KEY=your-key`

**Model not found:** Try `llama-3.1-70b-versatile` as alternative

**Slow responses:** Switch to `llama-3.1-8b-instant` model

**Import errors:** Run `pip install -r requirements.txt --force-reinstall`

## Assignment Requirements

**Completed:**
- Simple chatbot using LangChain chains
- Accepts user questions and returns answers
- Tested with 5+ sample queries
- Setup notes included (API key usage, env vars)

**Additional Features:**
- Conversation memory
- Multiple model selection
- Professional UI

## Future Enhancements

- Display conversation history in UI
- Clear conversation button
- Export chat history

---

**Built by Felix Samuel**  

*AI Engineering Intern @ Flexisaf (EdTech)*

