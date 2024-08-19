import spacy
import json
from tqdm import tqdm

nlp = spacy.load('en_core_web_sm')

def convert_sentence_to_json(sentences):
    docs = nlp(sentences)
    results = []

    for sent in docs.sents:
        result_json = {
            'prompt': sent.text,
            'keywords': [],
            'nouns': {},
            'activity': [],
        }

        for token in sent:
            if token.pos_ == 'NOUN':
                adjectives = [child.text for child in token.children if child.dep_ == 'amod']
                result_json['nouns'].setdefault(token.lemma_, {
                    'details': adjectives
                })
                if not token.lemma_ in result_json['keywords']:
                    result_json['keywords'].append(token.lemma_)
                
            if token.pos_ == 'VERB':
                negation = any(child.dep_ == 'neg' for child in token.children)
                verb_entry = token.lemma_
                
                if negation:
                    verb_entry = f'not_{verb_entry}'
                    if not token.lemma_ in result_json['keywords']:
                        result_json['keywords'].append('not')
                    
                result_json['activity'].append(verb_entry)
                if not token.lemma_ in result_json['keywords']:
                    result_json['keywords'].append(token.lemma_)
        results.append(result_json)
    return results

def convert_one(sentence):
    result_json = convert_sentence_to_json(sentence)

    with open('result.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_json, indent=4))

def convert_all():
    with open('metadata.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    input_videos = [line.split('|')[2] for line in lines]    
    
    result_json = []
    for video_desc in tqdm(input_videos, desc=''):
        result_json.append(convert_sentence_to_json(video_desc))

    with open('metadata.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(result_json, indent=4))

if __name__ == '__main__':
    # convert_one('A dog playing in the park')
    convert_all()
