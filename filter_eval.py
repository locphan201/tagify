def clean_prompts(prompt_file_path, cleaned_description_file_path):
    # Read the files
    with open(prompt_file_path, 'r', encoding='utf-8') as prompt_file:
        prompt_sentences = prompt_file.readlines()

    with open(cleaned_description_file_path, 'r', encoding='utf-8') as cleaned_file:
        cleaned_sentences = cleaned_file.readlines()

    # Strip whitespaces and remove duplicates
    prompt_sentences = list(dict.fromkeys([sentence.strip() for sentence in prompt_sentences if sentence.strip()]))
    cleaned_sentences = [sentence.strip() for sentence in cleaned_sentences if sentence.strip()]

    # Remove matching sentences
    remaining_sentences = [sentence for sentence in prompt_sentences if sentence not in cleaned_sentences]

    return remaining_sentences


def save_cleaned_prompts(remaining_sentences, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for sentence in remaining_sentences:
            output_file.write(sentence + '\n')


# Usage example
prompt_file = 'prompts.txt'  # path to your prompt file
cleaned_description_file = 'data/cleaned_description_video.txt'  # path to the cleaned description file
output_file = 'cleaned_prompts.txt'  # output file for cleaned prompts

remaining_sentences = clean_prompts(prompt_file, cleaned_description_file)
save_cleaned_prompts(remaining_sentences, output_file)

print("Cleaned and filtered prompts saved to:", output_file)