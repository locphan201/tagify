from flask import Flask, render_template, jsonify, request
from search import get_top_closest
from search.v2 import compare, get_keywords, load_data
from sentence_transformers import SentenceTransformer
import numpy as np
import time

app = Flask(__name__)

videos = load_data()
# Load SentenceTransformer model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_route():
    try:
        json_data = request.json
        prompt = json_data['prompt']
        
        keywords = get_keywords(prompt)
        
        t1 = time.time()
        compared = compare(videos, prompt)
        return_data = get_top_closest(compared)
        
        # Embedding and comparison section
        # Embed the prompt and the return data sentences
        prompt_embedding = model.encode([prompt])[0]  # Get embedding for prompt
        return_sentences = [data.split(' - ')[1] for data in return_data]  # Extract only the description sentences
        sentence_embeddings = model.encode(return_sentences)  # Get embeddings for the return sentences
        
        # Calculate cosine similarity between prompt and each sentence embedding
        similarities = np.dot(sentence_embeddings, prompt_embedding) / (
            np.linalg.norm(sentence_embeddings, axis=1) * np.linalg.norm(prompt_embedding)
        )
        
        # Sort based on similarity scores and get the top 5 closest sentences
        sorted_indices = np.argsort(similarities)[::-1][:5]
        top_5_closest = [return_data[i] for i in sorted_indices]
        t2 = time.time()
    
        print('Time:', t2 - t1)
        
        return jsonify({'keywords': keywords, 'result': top_5_closest}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Only .txt files are allowed'}), 400
    
    file_content = file.read().decode('utf-8')
    
    return jsonify({'content': file_content}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)