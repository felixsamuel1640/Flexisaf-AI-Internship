# 🇳🇬 AjoBot — Smart Nigerian Finance Agent

> A conversational AI agent that helps everyday Nigerians make smarter financial 
decisions — from exchange rates to fintech app comparisons — in plain simple 
English.

---

## 💡 What is AjoBot?

AjoBot is an AI-powered financial assistant built specifically for Nigerians. It 
answers real financial questions that affect everyday life — whether you want to 
know the current dollar rate, what to do when your OPay transfer fails, or which 
fintech app is best for you.

Named after **Ajo** — the traditional Nigerian community savings system — AjoBot 
brings that same spirit of financial empowerment into the digital age.

---

## 🚨 The Problem

Nigerian fintech apps like OPay, Kuda, and PalmPay are great at moving money — but 
they don't help users **understand** their money. People still struggle with:

- Not knowing the real exchange rate vs the black market rate
- Not understanding why their transfer failed or when to expect a reversal
- Not knowing which fintech app is best for their needs
- Making financial decisions blindly without any guidance

**AjoBot solves this** by giving everyday Nigerians a conversational assistant that 
explains financial decisions in plain English.

---

## ✨ Features

- 💱 **Live Exchange Rates** — converts any currency to/from Naira in real time
- 🏦 **Nigerian Fintech Knowledge** — answers questions about OPay, Kuda, PalmPay, 
BVN, transfer limits and more
- 🌐 **Live Web Search** — fetches current Nigerian fintech news and black market 
rates
- 🧠 **Conversation Memory** — remembers what you said earlier in the same session
- 🇳🇬 **Built for Nigerians** — understands Nigerian financial context that 
generic assistants miss

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain 1.2.10 | Agent framework |
| Groq (llama-3.3-70b-versatile) | LLM — fast and free |
| ExchangeRate API | Live currency conversion |
| Tavily Search | Live web search |
| LangGraph InMemorySaver | Conversation memory |
| Python dotenv | Environment variable management |

---

## 📁 Project Structure

```
task-7/
├── main.py          # Agent setup and conversation loop
├── tools.py         # All 3 tools (exchange rate, knowledge base, web search)
├── knowledge.py     # Nigerian fintech knowledge base
├── .env             # API keys (not committed to GitHub)
└── README.md        # You are here
```

---

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/felixsamuel1640/task-7.git
cd task-7
```

**2. Install dependencies**
```bash
pip install langchain==1.2.10 langchain-groq langchain-tavily langchain-community 
requests python-dotenv langgraph
```

**3. Create your `.env` file**
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
EXCHANGE_API_KEY=your_exchangerate_api_key
```

**4. Get your free API keys**
- Groq — [console.groq.com](https://console.groq.com)
- Tavily — [tavily.com](https://tavily.com)
- ExchangeRate API — [exchangerate-api.com](https://exchangerate-api.com)

**5. Run AjoBot**
```bash
python main.py
```

---

## 💬 Example Conversations

```
You: How much is 50,000 naira in dollars?
AjoBot: 50,000 NGN = $34.20 USD (Rate: 1 USD = ₦1,462.00)

You: My OPay transfer failed, what do I do?
AjoBot: Common reasons your transfer failed: insufficient balance,
        wrong account number, network downtime, or daily limit exceeded.
        Your money reverses within 24 hours. If not reversed, contact
        support with your transaction reference number.

You: Should I use Kuda or OPay?
AjoBot: OPay is better for traders and business owners due to its POS
        network. Kuda is better for salary earners and students —
        no maintenance fees and 25 free transfers monthly.

You: What is the latest news about OPay?
AjoBot: [fetches live results] OPay was named Fintech Company of the
        Year 2025 for the second consecutive time at the Leadership
        Annual Conference in Abuja...
```

---

## 🧠 How It Works

AjoBot uses a **3-tool agent architecture**:

```
User Question
      ↓
   AjoBot Agent (Groq LLM)
      ↓
Decides which tool to use:
      ├── convert_currency     → Exchange Rate API (live data)
      ├── search_knowledge_base → Nigerian fintech knowledge (local)
      └── web_search           → Tavily (live internet)
      ↓
   Final Answer to User
```

The agent reads each tool's description and decides which one to use based on the 
user's question — no hardcoding, no if/else logic.

---

## 🚀 Future Improvements

- 🗣️ **Pidgin English mode** — switch to Nigerian Pidgin for more relatable 
responses
- 📊 **Exchange rate history** — show rate trends over time
- 💾 **Persistent memory** — remember users across sessions
- 📱 **WhatsApp integration** — reach Nigerians where they already are
- 🏪 **Market trader mode** — help traders calculate profit margins with live rates

---

## 👨‍💻 Author

**Felix Samuel**
GitHub: [@felixsamuel1640](https://github.com/felixsamuel1640)

---

## 📄 License

MIT License — free to use and build on.

---

*Built with 🇳🇬 for everyday Nigerians who deserve better financial tools.*

