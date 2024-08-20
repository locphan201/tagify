from flask import Flask, render_template, jsonify, request
from compare import compare, load_data

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
        compared = compare(videos, prompt)
        
        max = compared[0]["points"]
        return_data = [f'{video["video"]} - {video["desc"]}' for video in compared if video["points"] == max]
        
        # return_data = [f'{video["video"]} - {video["desc"]}' for video in compared[:10]]
    
        return jsonify({'result': return_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)