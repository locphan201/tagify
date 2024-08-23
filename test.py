from convert.v1 import convert_sentence_to_json
from compare.v1 import load_data, compare
from tqdm import tqdm

with open('test_prompts.txt', 'r', encoding='utf-8') as file:
    prompts = file.readlines()
    
videos = load_data()

with open('test.csv', 'w', encoding='utf-8') as file:
    file.write('Prompt;Similarity')

for prompt in tqdm(prompts):
    json_data = convert_sentence_to_json(prompt)
    compared = compare(videos, json_data)
    
    with open('test.csv', 'a', encoding='utf-8') as file:
        for i in range(5):
            file.write(f'{prompt.strip()};{compared[i]["desc"]}\n')