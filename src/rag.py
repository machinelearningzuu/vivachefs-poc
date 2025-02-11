import os, sys
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from src.parser import DocumentParser

# Setup environment
load_dotenv()

project_root = str(Path.cwd().parent)
if project_root not in sys.path:
    sys.path.append(project_root)

print(f"Project root: {project_root}")

class RAGChat:
    def __init__(self, documents_path: str):
        """
        Initialize RAG chat with documents from the specified path
        """
        # Initialize OpenAI with GPT-4 and embedding models
        self.llm = OpenAI(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configure global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 1024
        Settings.chunk_overlap = 128
        
        # Load and index documents
        self.documents = SimpleDirectoryReader(documents_path).load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        
        # Create query engine with response synthesis
        self.query_engine = self.index.as_query_engine(
            response_mode="compact",
            streaming=True
        )
        
    def chat(self, query: str) -> str:
        """
        Query the RAG system with a question
        """
        try:
            response = self.query_engine.query(query)
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"