from tqdm import tqdm
from search import get_top_closest
from search.v2 import compare, load_data
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

def load_user_prompts() -> List[str]:
    try:
        with open('cleaned_prompts.txt', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines    
    except Exception as e:
        print(e)
        return []

videos = load_data()
user_prompts = load_user_prompts()

file = open('evaluate.txt', 'w', encoding='utf-8')

# Load SentenceTransformer model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

for prompt in tqdm(user_prompts, total=len(user_prompts), desc='Prompt'):
    compared = compare(videos, prompt)
    return_data = get_top_closest(compared)
    
    if len(return_data) > 25:
        return_data = return_data[:25] 
    
    prompt_embedding = model.encode([prompt])[0]  # Get embedding for prompt
    return_sentences = [data.split(' - ')[2] for data in return_data]  # Extract only the description sentences
    sentence_embeddings = model.encode(return_sentences)  # Get embeddings for the return sentences
    
    # Calculate cosine similarity between prompt and each sentence embedding
    similarities = np.dot(sentence_embeddings, prompt_embedding) / (
        np.linalg.norm(sentence_embeddings, axis=1) * np.linalg.norm(prompt_embedding)
    )
    
    # Sort based on similarity scores and get the top 5 closest sentences
    sorted_indices = np.argsort(similarities)[::-1][:5]
    top_5_closest = [return_data[i] for i in sorted_indices]
    
    ### Embedding models
    
    file.write(prompt)
    for d in top_5_closest:
        file.write(f'\n - {d}')
    file.write('\n\n')
    file.flush()

file.close()