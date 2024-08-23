import json
from constant import *

def load_data():
    with open(DATA_MIN_FILE, 'r') as f:
        videos = json.load(f)
    return videos

def compare(videos, keywords):
    compared = []
    
    for video in videos:
        total_points = 0
        for desc in video['s']:
            sentence_points = 0
            matched_keys = set()
            
            for key in desc['k']:
                if key in keywords:
                    matched_keys.add(key)
                    sentence_points += 1  
                    
            if 'n' in desc.keys():
                for noun in desc['n'].keys():
                    if noun in keywords:
                        sentence_points += 2  
                        
            total_points += sentence_points
        
        compared.append({
            'video': video['v'],
            'desc': ' '.join([desc['p'] for desc in video['s']]),
            'points': total_points
        })            

    # Sort the results by the points in descending order
    compared.sort(key=lambda x: x['points'], reverse=True)
    return compared
