import json
import sys

def convert_ids_to_string(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for article in data['data']:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                qa['id'] = str(qa['id'])

    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_file = sys.argv[1]
    convert_ids_to_string(input_file)
