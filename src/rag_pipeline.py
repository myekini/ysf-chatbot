"""RAG (Retrieval-Augmented Generation) pipeline implementation."""

from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from .document_processor import DocumentProcessor
from .embeddings import EmbeddingModel
from .vector_store import VectorStore

class RAGPipeline:
    """End-to-end RAG pipeline for document retrieval and generation."""
    
    def __init__(self, data_dir: str = "data/processed"):
        """Initialize the RAG pipeline."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.doc_processor = DocumentProcessor()
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(dimension=384)  # Default for all-MiniLM-L6-v2
        
        # Check for existing vector store
        self.vector_store_path = self.data_dir / "vector_store"
        if self.vector_store_path.with_suffix('.index').exists():
            self.vector_store = VectorStore.load(str(self.vector_store_path))
    
    def process_documents(self, file_paths: List[str]) -> None:
        """Process and index multiple documents."""
        all_chunks = []
        
        for file_path in file_paths:
            # Process document
            chunks = self.doc_processor.process_document(file_path)
            
            # Generate embeddings
            chunks_with_embeddings = self.embedding_model.embed_documents(chunks)
            all_chunks.extend(chunks_with_embeddings)
        
        # Add to vector store
        self.vector_store.add_documents(all_chunks)
        
        # Save the updated vector store
        self.vector_store.save(str(self.vector_store_path))
    
    def query(self, question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Query the RAG system with a question."""
        # Generate query embedding
        query_embedding = self.embedding_model.embed_text(question)
        
        # Retrieve relevant documents
        results = self.vector_store.search(query_embedding, k=top_k)
        
        return results
    
    def generate_response(self, question: str, context: List[Dict[str, Any]]) -> str:
        """Generate a response using the retrieved context."""
        # Format the context
        context_text = "\n\n".join([doc["text"] for doc in context])
        
        # In a real implementation, you would use a language model here
        # For now, we'll return a simple response
        return (
            f"Question: {question}\n\n"
            f"Here's some relevant information from the documents:\n\n"
            f"{context_text}"
        )
    
    def process_query(self, question: str) -> str:
        """Process a query and return a response."""
        # Retrieve relevant documents
        context = self.query(question)
        
        # Generate response
        response = self.generate_response(question, context)
        
        return response
