import os, time

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from tools import convert_currency, search_knowledge_base, web_search

load_dotenv()

# llm setup
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3)


# tools
tools = [convert_currency, search_knowledge_base, web_search]

system_prompt = """You are a helpful Nigerian financial assistant.
You have access to these tools and must use them correctly,

- convert_currency: USE THIS when user asks about exchange rates, converting naira to dollars,
pounds or any other currency.

- search_knowledge_base: USE THIS when user asks about Opay, Kuda, Palmpay, failed transfers,
bank charges, BVN or comparing fintech apps.

- web_search: USE THIS for latest nigerian news, current black market rates or 
anything not covered by the other tools.

Always respond in clear simple ENGLISH anyone can understand.
Always be honest, helpful and concise.

Never guess - always use the right tool to get the correct answer.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=InMemorySaver()
)

thread_id = "chat-1"
def main():
    while True:
        print("🇳🇬AjoBot — Smart Nigerian Finance Agent")
        print("Powered by Groq + LangChain 1.2.10\n")
        user_input = input("ask agent (enter 'quit' or 'exit' to quit): ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("Closing session")
            break

        if not user_input.lower():
            continue

        response = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )
        print("Fetching response..please wait!")
        time.sleep(1)
        print(f"Assistant: {response['messages'][-1].content}\n")

if __name__ == "__main__":
    main()

