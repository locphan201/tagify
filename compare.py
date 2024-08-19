import json
from tqdm import tqdm
from convert import convert_sentence_to_json

if __name__ == '__main__':
    with open('metadata.json', 'r') as f:
        videos = json.load(f)

    sentence = 'A goalkeeper playing soccer'
    result_json = convert_sentence_to_json(sentence)
    
    keywords = []
    for s in result_json:
        keywords.extend(s['keywords'])
    
    compared = []
    
    for video in videos:
        points = 0
        for desc in video:
            for key in desc['keywords']:
                if key in keywords:
                    points += 1
        
        compared.append({
            'desc': ' '.join([desc['prompt'] for desc in video]),
            'points': points
        })            

    sorted_compared = sorted(compared, key=lambda x: x['points'], reverse=True)

    print('\n', sentence)
    print(keywords, '\n')
    for i in range(5):
        print(f'{i+1}. {sorted_compared[i]["desc"]}')