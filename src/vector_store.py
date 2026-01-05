"""Vector store implementation for document retrieval."""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import faiss

class VectorStore:
    """A simple FAISS-based vector store for document retrieval."""
    
    def __init__(self, dimension: int = 384):  # Default dimension for all-MiniLM-L6-v2
        """Initialize the vector store with a given embedding dimension."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[Dict[str, Any]] = []
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents with embeddings to the vector store."""
        if not documents:
            return
            
        # Extract embeddings
        embeddings = np.array([doc["embedding"] for doc in documents], dtype=np.float32)
        
        # Add to FAISS index
        if len(self.documents) == 0:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        
        # Add vectors to index
        self.index.add(embeddings)
        
        # Store document metadata
        self.documents.extend(documents)
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if len(self.documents) == 0:
            return []
            
        # Reshape query embedding if needed
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # Search the index
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)
        
        # Return matching documents with scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0:  # Skip invalid indices
                continue
                
            doc = self.documents[idx].copy()
            doc["score"] = float(distances[0][i])
            results.append(doc)
            
        return results
    
    def save(self, filepath: str) -> None:
        """Save the vector store to disk."""
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.index")
        
        # Save document metadata
        with open(f"{filepath}_meta.json", 'w', encoding='utf-8') as f:
            json.dump({
                'dimension': self.dimension,
                'documents': self.documents
            }, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'VectorStore':
        """Load a vector store from disk."""
        # Load FAISS index
        index = faiss.read_index(f"{filepath}.index")
        
        # Load document metadata
        with open(f"{filepath}_meta.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
               
        # Create vector store instance
        store = cls(dimension=data['dimension'])
        store.index = index
        store.documents = data['documents']
        
        return store
