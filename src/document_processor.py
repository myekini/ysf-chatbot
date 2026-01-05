"""Document processing utilities for the YSJ Student Chatbot."""

from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
from docx import Document

class DocumentProcessor:
    """Handles loading and processing of various document formats."""
    
    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""

    @staticmethod
    def load_docx(file_path: str) -> str:
        """Extract text from a Word document."""
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return ""

    @staticmethod
    def load_txt(file_path: str) -> str:
        """Extract text from a plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks."""
        if not text:
            return []
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({
                "text": chunk,
                "start": start,
                "end": end,
                "overlap": overlap if start > 0 else 0
            })
            start = end - overlap
            
        return chunks
    
    @classmethod
    def process_document(cls, file_path: str) -> List[Dict[str, Any]]:
        """Process a document based on its extension and return chunks."""
        file_path = str(file_path) # Ensure string
        extension = Path(file_path).suffix.lower()
        
        text = ""
        if extension == '.pdf':
            text = cls.load_pdf(file_path)
        elif extension == '.docx':
            text = cls.load_docx(file_path)
        elif extension == '.txt' or extension == '.md':
            text = cls.load_txt(file_path)
        else:
            print(f"Unsupported file format: {extension}")
            return []
            
        if not text.strip():
            print(f"Warning: No text extracted from {file_path}")
            return []
            
        return cls.chunk_text(text)
