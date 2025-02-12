import streamlit as st
import sys
from pathlib import Path
from src.parser import DocumentParser
from src.rag import RAGChat

# Set page config
st.set_page_config(
    page_title="Viva Chefs Assistant",
    page_icon="👩‍🍳",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2C3E50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stMarkdown {
        color: #34495E;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Setup RAG Chat
project_root = str(Path.cwd())
if project_root not in sys.path:
    sys.path.append(project_root)

@st.cache_resource
def initialize_rag():
    parse = DocumentParser()
    parse.parse_documents("markdown_results")
    rag_chat = RAGChat(f"{project_root}/processed")
    return rag_chat

# Initialize RAG Chat
rag_chat = initialize_rag()

# Header with logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.title("Viva Chefs Assistant")

st.markdown("""
<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
Welcome! I'm here to help you learn more about Viva Chefs services. 
Ask me anything about our personal chef services, meal plans, or policies!
</div>
""", unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👩‍🍳" if message["role"] == "assistant" else None):
        st.markdown(f"<div class='chat-message'>{message['content']}</div>", unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("Ask me anything about Viva Chefs..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="👩‍🍳"):
        response = rag_chat.chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add footer with styling
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p>Powered by Viva Chefs AI Assistant</p>
    <p style='font-size: 0.8rem;'>© 2024 Viva Chefs. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)