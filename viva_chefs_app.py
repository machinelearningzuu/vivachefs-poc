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

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    .stApp {
        background-color: #fafafa;
    }
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1a472a;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
    }
    .stMarkdown {
        color: #2C3E50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .chat-container {
        border-radius: 15px;
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        box-shadow: 5px 5px 10px #d9d9d9, -5px -5px 10px #ffffff;
        padding: 20px;
        margin: 20px 0;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #1a472a, #2c5338);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0;
        border-radius: 15px;
    }
    .footer {
        background: linear-gradient(135deg, #1a472a, #2c5338);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
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

# Header with enhanced styling
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.title("Viva Chefs Assistant")

# Welcome banner with image
st.markdown("""
<div class='welcome-banner'>
    <h2>Welcome to Viva Chefs!</h2>
    <p>Your personal culinary concierge is here to assist you with all your dining needs.</p>
</div>
""", unsafe_allow_html=True)

# Feature highlights with images
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?ixlib=rb-4.0.3", caption="Personal Chef Service")
with col2:
    st.image("https://images.unsplash.com/photo-1547592180-85f173990554?ixlib=rb-4.0.3", caption="Custom Meal Plans")
with col3:
    st.image("https://images.unsplash.com/photo-1507048331197-7d4ac70811cf?ixlib=rb-4.0.3", caption="Special Events")

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# Enhanced footer with contact information
st.markdown("""
<div class='footer'>
    <h3>Experience the Luxury of Personal Chef Services</h3>
    <p>Elevate your dining experience with Viva Chefs</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>📞 Contact us: (555) 123-4567</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2024 Viva Chefs. All rights reserved.</p>
</div>
""", unsafe_allow_html=True) 