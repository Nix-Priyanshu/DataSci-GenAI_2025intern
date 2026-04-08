import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retriever_chain import qa_chain, log_interaction
import streamlit as st


# Page config
st.set_page_config(page_title="SmartHR: HR Assistant Bot", page_icon="🤖")


with st.sidebar:
    st.title("📌 About")
    st.markdown("""
    **SmartHR: HR Assistant Bot 🤖**

    - Built using RAG Architecture  
    - AWS Bedrock Knowledge Base  
    - Amazon Nova LLM  
    - LangChain PromptTemplate  

    Ask questions about company policies!
    """)
    

# Title
st.title("🤖 SmartHR: HR Assistant Bot")
st.markdown("💬 Ask me anything about company HR policies.")
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

#Divider
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your question here...")
# Empty input check
if user_input is not None and not user_input.strip():
    st.warning("Please enter a valid question.")
elif user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                # 🧠 Build conversation history
                history = ""
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        history += f"User: {msg['content']}\n"
                    else:
                        history += f"Assistant: {msg['content']}\n"

                # Combine history with current question
                enhanced_query = history + f"\nUser: {user_input}"
                
                result = qa_chain(enhanced_query)

                response = result["answer"]
                sources = result["sources"]

                st.markdown(response)

                # 📄 Show sources
                if sources:
                    st.markdown("---")
                    st.markdown("**📄 Source:**")
                    for src in sources:
                        st.markdown(f"- {src}")
                        
                log_interaction(user_input, response)
            except Exception as e:
                response = f"Error: {e}"
                st.markdown(response)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": response})
