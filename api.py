from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag import RAGChat
from src.parser import DocumentParser
from pathlib import Path
import sys

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your Next.js domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup RAG Chat
project_root = str(Path.cwd().parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Initialize RAG Chat
parse = DocumentParser()
parse.parse_documents("markdown_results")
rag_chat = RAGChat(f"{project_root}/processed")

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = rag_chat.chat(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 