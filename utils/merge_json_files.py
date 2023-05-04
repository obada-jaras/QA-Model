import argparse
import json


def merge_json_files(output_file, filenames):
    '''
    Assumes json files are in SQuAD format, i.e see https://github.com/facebookresearch/DrQA#format-b
    '''
    combined_data = []
    for fname in filenames:
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)['data']
        for article in data:
            combined_data.append(article)

    combined_data = {
        'data': combined_data,
        'version': "1.1"
    }

    with open(output_file,'w', encoding="utf-8") as f:
        json.dump(combined_data,f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge multiple JSON files into a single file')
    parser.add_argument('--input', '-i', required=True, help='Input files to merge')
    parser.add_argument('--output', '-o', required=True, help='Output file path')

    args = parser.parse_args()
    input_files = args.input
    
    # Split the filenames string into a list and remove any empty strings
    input_files = input_files.split('\n')
    input_files = list(filter(None, input_files))

    output_file = args.output

    merge_json_files(output_file, input_files)
