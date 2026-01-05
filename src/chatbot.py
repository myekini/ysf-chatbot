"""Chatbot interface for the YSJ Student Chatbot."""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from .rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

class YSJChatbot:
    """Main chatbot class for interacting with the RAG pipeline."""
    
    def __init__(self, data_dir: str = "data/processed"):
        """Initialize the chatbot with a RAG pipeline."""
        self.rag_pipeline = RAGPipeline(data_dir=data_dir)
        self.chat_history: List[Dict[str, str]] = []
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Create a prompt template
        self.prompt_template = PromptTemplate(
            template="""You are a helpful assistant for York St John University students. 
            Use the following context to answer the question. If you don't know the answer, 
            say that you don't have enough information and suggest contacting the university directly.
            
            Context: {context}
            
            Question: {question}
            
            Helpful Answer:""",
            input_variables=["context", "question"]
        )
    
    def add_documents(self, file_paths: List[str]) -> None:
        """Add documents to the chatbot's knowledge base."""
        if not file_paths:
            return "No files provided."
            
        # Check if files exist
        missing_files = [f for f in file_paths if not Path(f).exists()]
        if missing_files:
            return f"Error: The following files were not found: {', '.join(missing_files)}"
            
        try:
            self.rag_pipeline.process_documents(file_paths)
            return f"Successfully processed {len(file_paths)} documents."
        except Exception as e:
            return f"Error processing documents: {str(e)}"
    
    def chat(self, message: str) -> str:
        """Process a user message and return a response."""
        if not message.strip():
            return "Please enter a valid message."
            
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": message})
        
        try:
            # Get relevant documents from RAG pipeline
            context_docs = self.rag_pipeline.query(message, top_k=3)
            
            # Format context
            context = "\n\n".join([doc["text"] for doc in context_docs])
            
            # Generate response using LLM
            if context.strip():
                # Use RAG approach if we have context
                prompt = self.prompt_template.format(
                    context=context,
                    question=message
                )
                response = self.llm.invoke(prompt)
                response_text = response.content
            else:
                # Fallback to direct LLM query if no context
                response = self.llm.invoke(
                    f"As a York St John University assistant, please answer: {message}"
                )
                response_text = response.content
            
            # Add assistant response to chat history
            self.chat_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the chat history."""
        return self.chat_history
    
    def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []

# Example usage
if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = YSJChatbot()
    
    # Example conversation
    print("YSJ Student Chatbot initialized. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        response = chatbot.chat(user_input)
        print(f"\nChatbot: {response}")
