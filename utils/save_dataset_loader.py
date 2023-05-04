import argparse
import re

def update_and_save_code(dataset_loader_path, train_file_path, dev_file_path, output_file_path):
    with open(dataset_loader_path, "r") as input_file:
        code_lines = input_file.readlines()

    with open(output_file_path, "w") as output_file:
        in_code = False
        for line in code_lines:
            if "_URLs = {" in line:
                in_code = True
            if in_code:
                line = re.sub(r'"train": .*', f'"train": "{train_file_path}",', line)
                line = re.sub(r'"dev": .*', f'"dev": "{dev_file_path}",', line)
            if "}" in line:
                in_code = False
            output_file.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save Dataset Loader with Custom File Paths")
    parser.add_argument("--dataset_loader", type=str, help="Path to the dataset_loader file")
    parser.add_argument("--train_file", type=str, help="Path to the train file")
    parser.add_argument("--dev_file", type=str, help="Path to the dev file")
    parser.add_argument("--output_file", type=str, help="Path to save the output Python file")
    args = parser.parse_args()

    update_and_save_code(args.dataset_loader, args.train_file, args.dev_file, args.output_file)
