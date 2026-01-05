# YSJ Student Chatbot

An intelligent Retrieval-Augmented Generation (RAG) chatbot designed to assist York St John University students by answering questions about policies, procedures, and services using institutional documents.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🚀 Key Features

*   **Intelligent Query Answering**: Uses Groq (Llama 3.3 70B) to understand and answer complex student queries.
*   **Knowledge Retrieval**: Searches through university PDFs, Word documents, and text files using FAISS vector search.
*   **Document Context**: Provides answers grounded in specific institutional documents (e.g., "Fitness to Study Policy").
*   **Modern Interface**: A responsive, user-friendly React web interface for students.
*   **Easy Ingestion**: Batch process hundreds of documents with a single command.

## 🛠️ Technology Stack

*   **Backend**: Flask (Python)
*   **Frontend**: React, TypeScript, Tailwind CSS
*   **LLM**: Llama 3.3 70B (via Groq API)
*   **Vector Database**: FAISS (Facebook AI Similarity Search)
*   **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
*   **Orchestration**: LangChain

## 📦 Installation

### Prerequisites

*   Python 3.10+
*   Node.js 16+
*   Groq API Key (Get one for free at [groq.com](https://groq.com))

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ysj_chatbot.git
cd ysf_chatbot
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key
```

## 🏃‍♂️ Running the Application

### 1. Ingest Documents

Place your university documents (PDF, DOCX, TXT) in the `data/raw` folder. Then run:

```bash
python ingest.py
```

This will process the documents and build the vector database in `data/processed`.

### 2. Start the Server

This command starts the Flask API backend.

```bash
python app.py
```

### 3. Start the Frontend (Development)

In a new terminal:

```bash
cd frontend
npm start
```

Access the chatbot at `http://localhost:3000`.

## 🧪 Testing

Run the comprehensive test suite to ensure everything is working:

```bash
pytest
```

## 📁 Project Structure

```
ysf_chatbot/
├── app.py                 # Main application entry point (Flask)
├── ingest.py              # Document ingestion script
├── src/                   # Backend source code
│   ├── chatbot.py         # Main chatbot logic
│   ├── rag_pipeline.py    # RAG implementation
│   ├── document_processor.py # File parsing (PDF, DOCX, etc.)
│   └── vector_store.py    # FAISS wrapper
├── frontend/              # React frontend application
├── data/                  # Data storage
│   ├── raw/               # Drop your documents here
│   └── processed/         # Vector store indices
├── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
