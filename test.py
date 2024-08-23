from convert.v1 import convert_sentence_to_json
from compare.v2 import load_data, compare
from tqdm import tqdm
import os

with open('test_prompts.txt', 'r', encoding='utf-8') as file:
    prompts = file.readlines()
    
videos = load_data()

os.makedirs('test', exist_ok=True)
for i in range(1, 3):
    if i == 1:
        from compare.v1 import load_data, compare
    else:
        from compare.v2 import load_data, compare
        
    
    with open(f'test/test_v{i}.csv', 'w', encoding='utf-8') as file:
        file.write('Prompt;Similarity\n')

    for prompt in tqdm(prompts, desc=f'Test version v{i}'):
        json_data = convert_sentence_to_json(prompt)
        compared = compare(videos, json_data)
        
        with open(f'test/test_v{i}.csv', 'a', encoding='utf-8') as file:
            for j in range(5):
                file.write(f'{prompt.strip()};{compared[j]["desc"]}\n')