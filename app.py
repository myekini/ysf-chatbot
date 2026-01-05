"""Flask API server for the YSJ Student Chatbot."""

import os
from flask import Flask, send_from_directory, request, jsonify
from pathlib import Path
from dotenv import load_dotenv
from src.chatbot import YSJChatbot

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='frontend/build')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-for-ysj-chatbot')

# Initialize the chatbot
chatbot = YSJChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Get response from chatbot
    response = chatbot.chat(message)
    
    return jsonify({
        'response': response,
        'history': chatbot.get_chat_history()
    })

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Handle document uploads."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file temporarily
    upload_dir = Path('data/raw')
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename
    file.save(file_path)
    
    # Process the document
    result = chatbot.add_documents([str(file_path)])
    
    return jsonify({
        'message': result,
        'filename': file.filename
    })

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear the chat history."""
    chatbot.clear_chat_history()
    return jsonify({'status': 'success'})

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        return jsonify({"message": "YSJ Chatbot API is running. Frontend build not found."})

if __name__ == '__main__':
    # Create necessary directories
    for dir_path in ['data/raw', 'data/processed', 'data/sample']:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=5000)
