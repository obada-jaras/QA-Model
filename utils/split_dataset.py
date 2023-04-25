"""
Code by: Obada Jaras (https://github.com/obada-jaras)
This code may need to be enhanced to support more general cases.
If you can improve it, please send a pull request (https://github.com/obada-jaras/QA-Model).
"""

import argparse
import json
from sklearn.model_selection import train_test_split


DEFAULT_INCLUDE_VAL = False
DEFAULT_TRAIN_RATIO = 0.8
DEFAULT_VAL_RATIO = 0.1
DEFAULT_RANDOM_STATE = 42
DEFAULT_INDENT = 2


def load_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data


def split_data(data, train_ratio=DEFAULT_TRAIN_RATIO, val_ratio=DEFAULT_VAL_RATIO,
               include_val=DEFAULT_INCLUDE_VAL, random_state=DEFAULT_RANDOM_STATE):
    train_data, temp_data = train_test_split(data["data"], test_size=1 - train_ratio, random_state=random_state)

    if include_val:
        val_data, test_data = train_test_split(temp_data, test_size=val_ratio / (1 - train_ratio), random_state=random_state)
    else:
        val_data = None
        test_data = temp_data

    return train_data, val_data, test_data


def save_data(data, file_path, indent=DEFAULT_INDENT):
    with open(file_path, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=indent)


def main(input_file, output_dir, include_val=DEFAULT_INCLUDE_VAL, train_ratio=DEFAULT_TRAIN_RATIO,
         val_ratio=DEFAULT_VAL_RATIO, random_state=DEFAULT_RANDOM_STATE, output_indent=DEFAULT_INDENT):
    merged_data = load_data(input_file)
    train_data, val_data, test_data = split_data(merged_data, train_ratio, val_ratio, include_val, random_state)

    save_data({"data": train_data, "version": merged_data["version"]}, f"{output_dir}/train_dataset.json", output_indent)
    save_data({"data": test_data, "version": merged_data["version"]}, f"{output_dir}/test_dataset.json", output_indent)
    if include_val:
        save_data({"data": val_data, "version": merged_data["version"]}, f"{output_dir}/val_dataset.json", output_indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a dataset into train, validation, and test sets.')
    parser.add_argument('--input_file', type=str, default='dataset/dataset.json', help='Path to input dataset file')
    parser.add_argument('--output_dir', type=str, default='dataset', help='Path to output directory')
    parser.add_argument('--include_val', action='store_true', help='Whether to include a validation set or not')
    parser.add_argument('--train_ratio', type=float, default=DEFAULT_TRAIN_RATIO, help='Train/test split ratio')
    parser.add_argument('--val_ratio', type=float, default=DEFAULT_VAL_RATIO, help='Validation/test split ratio')
    parser.add_argument('--random_state', type=int, default=DEFAULT_RANDOM_STATE, help='Random state for reproducibility')
    parser.add_argument('--output_indent', type=int, default=DEFAULT_INDENT, help='Indentation level for the output JSON files')
    args = parser.parse_args()

    main(args.input_file, args.output_dir, args.include_val, args.train_ratio, args.val_ratio, args.random_state, args.output_indent)
