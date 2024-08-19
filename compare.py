import json
from convert import convert_sentence_to_json
import time
import argparse

def load_data():
    with open('metadata.json', 'r') as f:
        videos = json.load(f)
    return videos

def compare(videos, sentence):
    result_json = convert_sentence_to_json(sentence)
    
    keywords = []
    for s in result_json:
        keywords.extend(s['keywords'])
    
    compared = []
    
    for video in videos:
        points = set()
        areNounsMatched = False
        for desc in video:
            for key in desc['keywords']:
                if key in keywords:
                    points.add(key)
            if key in desc['nouns'].keys():
                areNounsMatched = True
        
        compared.append({
            'desc': ' '.join([desc['prompt'] for desc in video]),
            'points': len(list(points)) if areNounsMatched else 0
        })            

    compared.sort(key=lambda x: x['points'], reverse=True)

    print(keywords, '\n')
    for i in range(5):
        print(f'{compared[i]["points"]}pts - {compared[i]["desc"]}')

def compare_stream(times):
    t1 = time.time()
    videos = load_data()
    t2 = time.time()
    print(f'\nLoad {len(videos)} videos - {round(t2 - t1, 2)}s')
    
    while True:
        sentence = input('\nYou: ')
        if sentence.lower() == 'exit':
            print('See you later')
            break    
        
        t1 = time.time()
        compare(videos, sentence)
        t2 = time.time()
        
        print(f'Comparing takes {round(t2 - t1, 2)}s')
        
        if times != 0:
            return
        
        print('\n-----------------------------------\n')

def main():
    parser = argparse.ArgumentParser(description='Compare the input sentences with the data in metadata.json')
    parser.add_argument('--s', action='store_true', help='Compare from user inputs')
    args = parser.parse_args()

    if args.s:
        compare_stream(0)
    else:
        compare_stream(1)

if __name__ == '__main__':
    main()