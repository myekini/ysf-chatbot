"""Test script to verify environment variables are loaded correctly."""

from dotenv import load_dotenv
import os

def test_environment():
    """Load and verify environment variables."""
    print("Loading environment variables...")
    load_dotenv()  # Load environment variables from .env file
    
    # Get environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
    
    # Verify setup
    print("\n=== Environment Variables Verification ===")
    print(f"GROQ_API_KEY: {'✓ Loaded' if GROQ_API_KEY else '✗ Not found'}")
    print(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}")
    print(f"VECTOR_DB_PATH: {VECTOR_DB_PATH}")
    
    # Test Groq API connection
    if GROQ_API_KEY:
        print("\n=== Testing Groq API Connection ===")
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                groq_api_key=GROQ_API_KEY
            )
            
            # Simple test
            response = llm.invoke("Hello! Can you respond with 'API connection successful!'?")
            print(f"✓ Groq API Response: {response.content}")
            
        except Exception as e:
            print(f"✗ Error connecting to Groq API: {str(e)}")
    
    # Create vector DB directory if it doesn't exist
    if VECTOR_DB_PATH:
        print(f"\n=== Creating Vector DB Directory ===")
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        print(f"✓ Vector DB directory created/verified at: {VECTOR_DB_PATH}")
    
    print("\n=== Setup Complete ===")
    return True

if __name__ == "__main__":
    test_environment()
