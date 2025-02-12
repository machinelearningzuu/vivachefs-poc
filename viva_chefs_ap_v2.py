import os, sys, pickle
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader

# Setup environment and paths
load_dotenv()

class DocumentParser:
    def __init__(self):
        self.parser = LlamaParse(
            api_key=os.environ["LLAMA_PARSER_API_KEY"],
            result_type="markdown"
        )
        self.write_path = "processed/parsed_documents.md"

    def load_documents(self):
        with open(self.write_path, 'r', encoding='utf-8') as f:
            return f.read()


class RAGChat:
    def __init__(self, documents_path: str):
        """
        Initialize RAG chat with documents from the specified path
        """
        self.system_prompt = """You are a helpful assistant for Viva Chefs. 

        For greetings and basic interactions (like "hi", "hello", "how are you", etc.), respond naturally and warmly.
        
        For all other questions, 
        
        1. if you don't find relevant information in the provided context to answer accurately but still relevant to the https://www.vivachefs.com website, 
        respond with:
        
        "Kindly note that our operations team has limited availability after 6:00 PM PST. Therefore, messages received after this time may not be addressed until the following morning. We appreciate your understanding and patience."
        
        2. if you don't find relevant information in the provided context to answer accurately and not related to the https://www.vivachefs.com website, 
        respond with:

        "I apologize, but I can only assist with questions related to Viva Chefs' personal chef services, meal plans, and policies. For other topics, please visit www.vivachefs.com or contact our support team at support@vivachefs.com for personalized assistance. We're here to help you with all your personal chef and meal planning needs!"
        """
        
        # Initialize OpenAI with GPT-4 and embedding models
        self.llm = OpenAI(
                        model="gpt-4o",
                        temperature=0.7,
                        api_key=os.environ["OPENAI_API_KEY"],
                        system_prompt=self.system_prompt
                        )
        self.embed_model = OpenAIEmbedding(
                                        model="text-embedding-3-small",
                                        api_key=os.environ["OPENAI_API_KEY"]
                                        )
        
        # Configure global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 1024
        Settings.chunk_overlap = 128
        
        # Load and index documents
        index_path = "processed/index.pkl"
        if os.path.exists(index_path):
            with open(index_path, 'rb') as f:
                self.index = pickle.load(f)
        else:
            self.documents = SimpleDirectoryReader(documents_path).load_data()
            self.index = VectorStoreIndex.from_documents(self.documents)
            with open(index_path, 'wb') as f:
                pickle.dump(self.index, f)
        
        # Create query engine with response synthesis
        self.query_engine = self.index.as_query_engine(
                                                    response_mode="compact",
                                                    system_prompt=self.system_prompt,
                                                    streaming=True
                                                    )
        
    def chat(self, query: str) -> str:
        """
        Query the RAG system with a question
        """
        # try:
        response = self.query_engine.query(query)
        # if not response or getattr(response, 'confidence', 0) < 0.5:
        #     return ("Kindly note that our operations team has limited availability after 6:00 PM PST. "
        #            "Therefore, messages received after this time may not be addressed until the following morning. "
        #            "We appreciate your understanding and patience.")
        return str(response).replace(" For other topics, please visit www.vivachefs.com or contact our support team at support@vivachefs.com for personalized assistance. We're here to help you with all your personal chef and meal planning needs!")
        
        # except Exception as e:
        #     return ("Kindly note that our operations team has limited availability after 6:00 PM PST. "
        #            "Therefore, messages received after this time may not be addressed until the following morning. "
        #            "We appreciate your understanding and patience.")


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
    rag_chat = RAGChat("processed")
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