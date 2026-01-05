"""Tests for the RAG pipeline and chatbot functionality."""

import pytest
import os
from pathlib import Path
from src.chatbot import YSJChatbot

# Create a test PDF file for testing
TEST_PDF_CONTENT = """
YSJ Student Information

Welcome to York St John University. This is a test document.
It contains information about student services, courses, and campus facilities.
"""

@pytest.fixture
def create_test_pdf(tmp_path):
    """Create a test PDF file for testing."""
    pdf_path = tmp_path / "test_document.pdf"
    
    # In a real test, you would create a proper PDF file
    # For simplicity, we'll just create a text file with .pdf extension
    with open(pdf_path, 'w', encoding='utf-8') as f:
        f.write(TEST_PDF_CONTENT)
    
    return str(pdf_path)

def test_chatbot_initialization():
    """Test that the chatbot initializes correctly."""
    chatbot = YSJChatbot()
    assert chatbot is not None

def test_add_documents(create_test_pdf):
    """Test adding documents to the chatbot."""
    chatbot = YSJChatbot()
    result = chatbot.add_documents([create_test_pdf])
    assert "successfully processed" in result.lower()

def test_chat_without_documents():
    """Test that the chatbot can handle queries without documents."""
    chatbot = YSJChatbot()
    response = chatbot.chat("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_chat_history():
    """Test that chat history is maintained correctly."""
    chatbot = YSJChatbot()
    test_messages = ["Hello", "How are you?", "What can you tell me about YSJ?"]
    
    for msg in test_messages:
        chatbot.chat(msg)
    
    history = chatbot.get_chat_history()
    assert len(history) == 2 * len(test_messages)  # Each message has a response

def test_clear_chat_history():
    """Test that chat history can be cleared."""
    chatbot = YSJChatbot()
    chatbot.chat("Test message")
    chatbot.clear_chat_history()
    assert len(chatbot.get_chat_history()) == 0
