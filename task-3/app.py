
import os
from dotenv import load_dotenv

import streamlit as st
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

st.title("🦉 WiseOwl")

if 'messages' not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input("Enter your question: ")

model_choice = st.selectbox(
    "🦉 Select Model",
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
)

llm = ChatGroq(model=model_choice, temperature=0.7)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are WiseOwl, a patient and helpful AI tutor. You remember 
previous conversations and help students learn effectively"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

chain = prompt_template | llm

if prompt:
    response = chain.invoke({
        "chat_history": st.session_state.messages,
        "input": prompt
    })

    st.session_state.messages.append(HumanMessage(content=prompt))
    st.session_state.messages.append(AIMessage(content=response.content))

    st.write(response.content)

else:
    st.warning("Please enter a prompt")
