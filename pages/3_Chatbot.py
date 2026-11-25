import logging
import os
import streamlit as st
from pydantic_ai import Agent

st.set_page_config(page_title="Business Chatbot", page_icon="💬")
st.title("International Business Chatbot 💬")
st.write("Ask for general tips for preparing for an international business conversation.")

try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    logging.exception("Gemini request failed")
    answer = "Sorry, something went wrong. Please try again."

agent = Agent(
    "google:gemini-3.8-flash",
    instructions=(
        "You are a friendly assistant for people preparing for international business conversations. "
        "Keep answers short, respectful, and practical. Give general advice about communication and meeting preparation. "
        "Do not use or invent country facts, time zones, currencies, or languages. "
        "If asked for exact country information, say you cannot look it up here and suggest the Country Guide page. "
        "Remember details the user shares during this conversation."
    ),
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hi! I can help you prepare for an international business conversation."}
    ]

if "message_history" not in st.session_state:
    st.session_state.message_history = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        result = agent.run_sync(
            prompt,
            message_history=st.session_state.message_history,
        )
        answer = result.output
        st.session_state.message_history = result.all_messages()
    except Exception:
        answer = "Sorry, something went wrong. Please try again."

    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
