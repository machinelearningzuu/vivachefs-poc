import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from llama_parse import LlamaParse

# Setup environment and paths
load_dotenv()

project_root = str(Path.cwd())
if project_root not in sys.path:
    sys.path.append(project_root)

class DocumentParser:
    def __init__(self):
        self.parser = LlamaParse(
            api_key=os.getenv("LLAMA_PARSER_API_KEY"),
            result_type="markdown"
        )
        self.write_path = f"{project_root}/processed/parsed_documents.md"
        
    def parse_documents(
                        self, 
                        directory_path: str
                        ) -> list:
        """
        Parse all documents in the specified directory using LlamaParse
        """
        if not os.path.exists(self.write_path):
            parsed_documents = []
            directory = f"{project_root}/{directory_path}"
            
            # Supported file extensions
            supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
            
            print(f"Scanning directory: {directory}")
            for file_path in directory.glob('*'):
                if file_path.suffix.lower() in supported_extensions:
                    try:
                        documents = self.parser.load_data(str(file_path))
                        parsed_documents.extend(documents)
                        print(f"Successfully parsed: {file_path.name}")
                    except Exception as e:
                        print(f"Error parsing {file_path.name}: {str(e)}")
            
            self.write_to_file(parsed_documents)
    
    def write_to_file(self, documents: list):
        with open(self.write_path, 'w', encoding='utf-8') as f:
            for doc in documents:
                f.write(f"{doc.text}\n\n")
                f.write("---\n\n")  # Add separator between documents

    def load_documents(self):
        with open(self.write_path, 'r', encoding='utf-8') as f:
            return f.read()


