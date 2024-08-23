import json
from constant import *

def load_data():
    with open(DATA_MIN_FILE, 'r') as f:
        videos = json.load(f)
    return videos

def compare(videos, keywords):
    compared = []
    
    for video in videos:
        points = set()
        areNounsMatched = False
        for desc in video['s']:
            for key in desc['k']:
                if key in keywords:
                    points.add(key)
            if 'n' in desc.keys() and key in desc['n'].keys():
                areNounsMatched = True
        
        compared.append({
            'video': video['v'],
            'desc': ' '.join([desc['p'] for desc in video['s']]),
            'points': len(list(points)) if areNounsMatched or not 'n' in desc.keys() else 0
        })            

    compared.sort(key=lambda x: x['points'], reverse=True)
    return compared