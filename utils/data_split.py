import argparse
import json
from math import floor


DEFAULT_TRAIN_RATIO = 0.8
DEFAULT_VAL_RATIO = 0.1
DEFAULT_RANDOM_STATE = 42
DEFAULT_INDENT = 2


def load_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data


def split_data(filename, train_ratio=DEFAULT_TRAIN_RATIO, val_ratio=DEFAULT_VAL_RATIO, include_val=False):
    with open(filename, 'r', encoding='utf-8') as f:
        dataset = json.load(f)['data']

    data_train = []
    data_dev = []
    data_test = []
    last_train_index = floor(len(dataset) * train_ratio)
    last_dev_index = floor(len(dataset) * (train_ratio + val_ratio))
    i = 0

    for article in dataset:
        if i >= last_dev_index:
            data_test.append(article)
        elif include_val and i >= last_train_index:
            data_dev.append(article)
        else:
            data_train.append(article)
        i += 1

    return data_train, data_dev, data_test


def save_data(data, file_path, indent=DEFAULT_INDENT):
    with open(file_path, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=indent)


def main(input_file, output_dir, include_val, train_ratio=DEFAULT_TRAIN_RATIO,
         val_ratio=DEFAULT_VAL_RATIO, output_indent=DEFAULT_INDENT):
    train_data, val_data, test_data = split_data(input_file, train_ratio, val_ratio, include_val)

    save_data({"data": train_data, "version": "1.1"}, f"{output_dir}/train_dataset.json", output_indent)
    save_data({"data": test_data, "version": "1.1"}, f"{output_dir}/test_dataset.json", output_indent)
    if include_val:
        save_data({"data": val_data, "version": "1.1"}, f"{output_dir}/val_dataset.json", output_indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a dataset into train, validation, and test sets.')
    parser.add_argument('--input_file', type=str, default='dataset/dataset.json', help='Path to input dataset file')
    parser.add_argument('--output_dir', type=str, default='dataset', help='Path to output directory')
    parser.add_argument('--include_val', action='store_true', help='Whether to include a validation set or not')
    parser.add_argument('--train_ratio', type=float, default=DEFAULT_TRAIN_RATIO, help='Train/test split ratio')
    parser.add_argument('--val_ratio', type=float, default=DEFAULT_VAL_RATIO, help='Validation/test split ratio')
    parser.add_argument('--output_indent', type=int, default=DEFAULT_INDENT, help='Indentation level for the output JSON files')
    args = parser.parse_args()

    main(args.input_file, args.output_dir, args.include_val, args.train_ratio, args.val_ratio, args.output_indent)
