from flask import Flask, render_template, jsonify, request
from convert.v1 import convert_sentence_to_json
from compare.v1 import load_data, compare

app = Flask(__name__)

videos = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_route():
    try:
        json_data = request.json
        prompt = json_data['prompt']
        
        json_input = convert_sentence_to_json(prompt)
        keywords = []
        [keywords.extend(s['k']) for s in json_input]
        compared = compare(videos, keywords)
        
        max = compared[0]["points"]
        return_data = [f'{video["video"]} - {video["desc"]}' for video in compared if video["points"] == max]
        
        return jsonify({'keywords': keywords, 'result': return_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)