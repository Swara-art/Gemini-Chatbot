import streamlit as st
import requests
import uuid

# Page configuration
st.set_page_config(
    page_title="Gemini Intelligence Chat",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state for user_id and chat history
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    st.info(f"**Session ID:** {st.session_state.user_id}")
    if st.button("New Chat"):
        st.session_state.user_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

# Main UI
st.title("🚀 Gemini AI Chatbot")
st.markdown("---")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is on your mind?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call FastAPI backend
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "http://localhost:8000/chat/",
                json={
                    "user_id": st.session_state.user_id,
                    "message": prompt
                },
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json().get("response", "No response received.")
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(answer)
                
                # Add assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")

# Add a footer
st.markdown("---")
st.caption("Powered by Google Gemini 1.5/2.x Flash with Real-time Search Capabilities")
