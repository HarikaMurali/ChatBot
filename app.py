import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# ---------- Load API key ----------
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not API_KEY:
    st.error("PERPLEXITY_API_KEY not found in .env file.")
    st.stop()

# OpenAI-compatible client pointing to Perplexity [web:54][web:75][web:78]
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai",
)

SYSTEM_PROMPT = """
You are a helpful college course assistant chatbot.
You answer questions about courses, timetables, basic CS topics,
and give short, clear explanations. Keep answers concise.
"""

# ---------- Streamlit page config ----------
st.set_page_config(page_title="College Chatbot", page_icon="💬")
st.title("College Course Assistant Chatbot")
st.caption("Powered by Perplexity Sonar API + Streamlit")

# ---------- Initialize chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Show chat history (skip system prompt)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- User input ----------
user_input = st.chat_input("Ask about courses, schedules, or CS concepts...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ---------- Call Perplexity chat completions ----------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="sonar-reasoning",   # good default Perplexity model [web:72][web:78]
                    messages=st.session_state.messages,
                )
                assistant_reply = response.choices[0].message.content
            except Exception as e:
                assistant_reply = f"Error from API: {e}"

            st.markdown(assistant_reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# ---------- Clear conversation ----------
if st.button("Clear conversation"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.experimental_rerun()
