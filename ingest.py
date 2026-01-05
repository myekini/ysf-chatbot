"""
Ingestion script to process all documents in data/raw and populate the vector store.
"""

import os
import shutil
from pathlib import Path
from src.rag_pipeline import RAGPipeline
from tqdm import tqdm

def ingest_data():
    """Process all documents in data/raw."""
    
    # Paths
    ROOT_DIR = Path(__file__).parent
    RAW_DIR = ROOT_DIR / "data" / "raw"
    PROCESSED_DIR = ROOT_DIR / "data" / "processed" # For moving processed files if needed, or just keeping track
    
    print(f"🚀 Starting ingestion from: {RAW_DIR}")
    
    if not RAW_DIR.exists():
        print(f"❌ Error: {RAW_DIR} does not exist.")
        return

    # Find all supported files
    supported_extensions = {'.pdf', '.docx', '.txt', '.md'}
    files_to_process = []
    
    for ext in supported_extensions:
        files_to_process.extend(list(RAW_DIR.glob(f"*{ext}")))
    
    if not files_to_process:
        print("⚠️ No supported documents found in data/raw.")
        print(f"Supported formats: {supported_extensions}")
        return

    print(f"found {len(files_to_process)} documents.")
    
    # Initialize RAG Pipeline
    print("Initializing RAG pipeline...")
    rag = RAGPipeline()
    
    # Process
    success_count = 0
    errors = []
    
    for file_path in tqdm(files_to_process, desc="Processing documents"):
        try:
            rag.process_documents([str(file_path)])
            success_count += 1
        except Exception as e:
            errors.append((file_path.name, str(e)))
    
    # Summary
    print("\n" + "="*50)
    print(f"✅ Ingestion Complete!")
    print(f"Successfully processed: {success_count}/{len(files_to_process)}")
    
    if errors:
        print("\n❌ Errors encountered:")
        for name, err in errors:
            print(f"- {name}: {err}")
    
    print("="*50)

if __name__ == "__main__":
    ingest_data()
