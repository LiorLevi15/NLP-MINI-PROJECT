import json
from datasets import load_dataset
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import datetime

API_URL = "https://api-inference.huggingface.co/models/ThatGuyVanquish/kook-model-output-dir"
headers = {"Authorization": "Bearer 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"}
dataset = load_dataset("NLP-MINI-PROJECT/rabbi_kook")
split = 'validation'

model_name = "ThatGuyVanquish/mt5-small-rabbi-kook"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_summaries():
    paragraphs = dataset[split]['paragraph']
    generated_summaries = []

    batch_size = 2
    for i in range(1, len(paragraphs)//batch_size):
        curr_paragraphs = paragraphs[(i-1)*batch_size: i*batch_size]
        input_ids = tokenizer(
            curr_paragraphs,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )["input_ids"]

        elapsed_time = datetime.datetime.now()
        output_ids = model.generate(
            input_ids=input_ids,
            max_length=1044,
            min_length=100,
            no_repeat_ngram_size=2,
            num_beams=4
        )
        elapsed_time = datetime.datetime.now() - elapsed_time
        print(f'summary {i} elapsed time={int(elapsed_time.total_seconds()*1000)}')

        for output_id in output_ids:
            generated_summary = tokenizer.decode(
                output_id,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )
            print(generated_summary)

            filtered_summary = remove_substrings(generated_summary)
            generated_summaries.append(filtered_summary)
            print(filtered_summary)

    with open(
            '/Users/llevi1/Desktop/personal/degree/Mini_Project/rouge_score/model_generated_summaries.json',
            'w') as file:
        file.write(json.dumps(generated_summaries, ensure_ascii=False))


def remove_substrings(text):
    # Define a regular expression to match substrings in the format "<some chars>"
    pattern = r"<.*?>"

    # Use the re.sub() function to replace all occurrences of the pattern with an empty string
    result = re.sub(pattern, "", text)

    return result


if __name__ == '__main__':
    full_elapsed_time = datetime.datetime.now()
    generate_summaries()
    full_elapsed_time = datetime.datetime.now() - full_elapsed_time
    print(f'full elapsed time={int(full_elapsed_time.total_seconds()*1000)}')

