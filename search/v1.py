import spacy
import json
from tqdm import tqdm
import os
import json

nlp = spacy.load('en_core_web_sm')

VERSION = 'v1'

def load_data(minify=True):
    print('Search version:', VERSION)
    filename = f'metadata-{VERSION}.min.json' if minify else f'metadata-{VERSION}.json'
    
    if not os.path.isfile(os.path.join('data', filename)):
        print(f'MISSING: {filename}')
        print(f'FOUND: metadata.txt')
        print(f'Generating {filename} from metadata.txt')
        convert(os.path.join('data', 'metadata.txt'))
        
    with open(os.path.join('data', filename), 'r', encoding='utf-8') as f:
        videos = json.load(f)
    return videos
        
def convert_sentence_to_json(sentences):
    docs = nlp(sentences)
    results = []

    for sent in docs.sents:
        result_json = {
            'p': sent.text.strip(),
            'k': [],
            'n': {},
            'pn': [],
            'act': [],
        }

        for token in sent:
            if token.pos_ == 'NOUN':
                adjectives = [child.text for child in token.children if child.dep_ == 'amod']
                result_json['n'].setdefault(token.lemma_, {
                    'd': adjectives
                })
                if not token.lemma_ in result_json['k']:
                    result_json['k'].append(token.lemma_)
                
            if token.pos_ == 'PROPN':
                result_json['pn'].append(token.text)
                if not token.text in result_json['k']:
                    result_json['k'].append(token.text)
            
            if token.pos_ == 'VERB':
                negation = any(child.dep_ == 'neg' for child in token.children)
                verb_entry = token.lemma_
                
                adverbs = [child.text for child in token.children if child.pos_ == 'ADV']
                if adverbs:
                    verb_entry = f"{verb_entry} ({', '.join(adverbs)})"
                    [result_json['k'].append(adverb) for adverb in adverbs if not adverbs in result_json['k']]
                
                if negation:
                    verb_entry = f'not_{verb_entry}'
                    if not token.lemma_ in result_json['k']:
                        result_json['k'].append('not')
                    
                result_json['act'].append(verb_entry)
                if not token.lemma_ in result_json['k']:
                    result_json['k'].append(token.lemma_)
        results.append(result_json)
    return results

def convert(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines() 
    
    video_names = [line.split('|')[0] for line in lines]
    input_videos = [line.split('|')[1] for line in lines]
    
    result_json = []
    result_sm_json = [] 
    for name, desc in tqdm(zip(video_names, input_videos), total=len(video_names), desc='Convert'):
        json_data = convert_sentence_to_json(desc)
        result_json.append({
            'v': name,
            's': json_data
        })
        
        json_data_sm = [{
            'p': j['p'],
            'k': j['k'],
            'n': list(j['n'].keys())
        } for j in json_data]
        result_sm_json.append({
            'v': name,
            's': json_data_sm
        })

    with open(os.path.join('data', f'example-{VERSION}.json'), 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_json[0], indent=4))  

    with open(os.path.join('data', f'metadata-{VERSION}.json'), 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_json))
    
    with open(os.path.join('data', f'metadata-{VERSION}.min.json'), 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_sm_json))

def get_keywords(prompt):
    json_input = convert_sentence_to_json(prompt)
    keywords = []
    [keywords.extend(s['k']) for s in json_input]
    return keywords

def compare(videos, prompt):
    keywords = get_keywords(prompt)
    
    compared = []
    
    for video in videos:
        total_points = 0
        nouns = set()
        for desc in video['s']:
            matched_keys = set()
            
            for key in desc['k']:
                if key in keywords:
                    matched_keys.add(key)
            
            sentence_points = len(list(matched_keys))
            
            keys = desc['n'] if isinstance(desc['n'], list) else desc['n'].keys()
            for noun in keys:
                if noun in keywords:
                    nouns.add(noun)
   
            total_points += sentence_points
   
        num_nouns = len(list(nouns))     
        total_points = 0 if num_nouns == 0 else total_points + num_nouns * 3
        
        compared.append({
            'v': video['v'],
            'd': ' '.join([desc['p'] for desc in video['s']]),
            'p': total_points
        })            

    # Sort the results by the points in descending order
    compared.sort(key=lambda x: x['p'], reverse=True)
    return compared