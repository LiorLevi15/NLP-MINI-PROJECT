import glob
import json
import random
import string


if __name__ == "__main__":
    json_files = glob.glob(
            f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/DATA/parsed_data_splits/*.json')
    print(json_files)
    sum = 0
    # Iterate through each JSON file and print the data size
    for file in json_files:
        with open(file, "r") as f:
            data = json.load(f)
            sum += len(data)
            print(f'size of {file} is: {len(data)}')
    print(f'total data size: {sum}')

