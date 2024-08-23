import spacy
import json
from tqdm import tqdm
from constant import *

nlp = spacy.load(MODEL)

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

def convert_all():
    with open(RAW_FILE, 'r', encoding='utf-8') as file:
        lines = file.readlines() 
    
    video_names = [line.split('|')[0] for line in lines]
    input_videos = [line.split('|')[1] for line in lines]
    
    result_json = []
    result_sm_json = [] 
    for name, desc in tqdm(zip(video_names, input_videos), desc=''):
        json_data = convert_sentence_to_json(desc)
        result_json.append({
            'v': name,
            's': json_data
        })
        
        json_data_sm = [{
            'p': j['p'],
            'k': j['k']
        } for j in json_data]
        result_sm_json.append({
            'v': name,
            's': json_data_sm
        })

    with open(EXAMPLE_FILE, 'w', encoding='utf-8') as file:
        file.write(json.dumps([result_json[0]]), indent=4)
    print(f'Saved as {EXAMPLE_FILE}')   

    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_json))
    print(f'Saved as {DATA_FILE}')    
    
    with open(DATA_MIN_FILE, 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_sm_json))
    print(f'Saved as {DATA_MIN_FILE}')    

if __name__ == '__main__':
    convert_all()