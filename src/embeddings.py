"""Embedding utilities for the YSJ Student Chatbot."""

from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """Handles text embedding generation using pre-trained models."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for multiple document chunks."""
        texts = [doc["text"] for doc in documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add embeddings to documents
        for doc, embedding in zip(documents, embeddings):
            doc["embedding"] = embedding.tolist()
            
        return documents
