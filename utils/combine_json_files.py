import json


def combine_json_files(output_file, filenames):
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