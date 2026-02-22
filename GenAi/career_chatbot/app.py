import os
import streamlit as st
import time
import logging

from dotenv import load_dotenv
from backend.gemini_client import generate_response
from backend.prompts import build_system_prompt
from backend.config import validate_config
from backend.memory import get_recent_history

validate_config()

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


st.title("Career Guidance Chatbot")

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")

personality = st.sidebar.selectbox(
    "Choose Assistant Personality",
    ["Friendly", "Professional", "Fun"]
)

st.sidebar.markdown("### 📥 Export Chat")

# MEMORY (Initialize session state for messages if not exists)
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Download Chat"):
    chat_text = ""
    for msg in st.session_state.messages:
        role = msg["role"].capitalize()
        chat_text += f"{role}: {msg['content']}\n\n"

    st.sidebar.download_button(
        label="Click to Download",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- CHAT INTERFACE ---

# Chat History (Display chat history from session state)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# --- INPUT ---
user_input = st.chat_input("Ask about careers...")

if user_input:
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Career Clarity Check with 3 Questions
    if "don't know" in user_input.lower() or "confused" in user_input.lower():
        reply =  """No worries — let's figure it out together 😊
                        1️⃣ What subjects do you enjoy?\n
                        2️⃣ Do you prefer creative or technical work?
                        3️⃣ Do you like working with people, data, or technology?
                       """
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
        st.stop()


    #History Content Before API Call
    history_context = get_recent_history(st.session_state.messages)

    #System Prompt
    with st.spinner("Thinking... 🤔"):
        system_prompt = build_system_prompt(personality, user_input)
        reply = generate_response(system_prompt, history_context)


     # --- Typing indicator ---
    typing_placeholder = st.empty()
    typing_placeholder.markdown("_Bot is typing..._")
    time.sleep(0.4)  # small delay for realism
    typing_placeholder.empty()

    # --- TYPING EFFECT AND DISPLAY ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        typed_text = ""
        safe_reply = reply or "⚠️ Sorry, I couldn't generate a response."
        for char in safe_reply:
            typed_text += char
            placeholder.markdown(typed_text + "▌")
            time.sleep(0.015)
        placeholder.markdown(safe_reply)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👍", key="up"):
                st.toast("Glad you liked it!")
        with col2:
            if st.button("😐", key="neutral"):
                st.toast("Thanks for the feedback!")
        with col3:
            if st.button("👎", key="down"):
                st.toast("I'll try to improve!")


    # Store bot reply
    st.session_state.messages.append({"role": "assistant", "content": safe_reply})
    
    logging.info("User: %s", user_input)
    logging.info("Bot: %s", safe_reply)

    st.rerun() # Refresh to show feedback buttons properly
