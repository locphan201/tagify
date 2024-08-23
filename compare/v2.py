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
        areNounsMatched = False
        for desc in video['s']:
            sentence_points = 0
            matched_keys = set()
            
            for key in desc['k']:
                if key in keywords:
                    matched_keys.add(key)
                    sentence_points += 1  # Add 1 point for each matched keyword

            if 'n' in desc.keys():
                for noun in desc['n'].keys():
                    if noun in keywords:
                        sentence_points += 2  # Add 2 points for matching nouns
                        areNounsMatched = True

            total_points += sentence_points

        # If nouns are matched, keep the points, otherwise set points to 0
        if not areNounsMatched:
            total_points = 0
        
        compared.append({
            'video': video['v'],
            'desc': ' '.join([desc['p'] for desc in video['s']]),
            'points': total_points
        })            

    # Sort the results by the points in descending order
    compared.sort(key=lambda x: x['points'], reverse=True)
    return compared

if __name__ == '__main__':
    videos = load_data()
    keywords = ["example", "keyword", "list"]  # Replace with your actual keywords
    result = compare(videos, keywords)
    print(result)
