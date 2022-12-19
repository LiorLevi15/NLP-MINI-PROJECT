import glob
import json
import random
import string


def parse(paragraph_file_name: string, summery_file_name: string, current_id: int, occur, s_letter, p_letter):
    parsed_file = []
    with open(paragraph_file_name, encoding='UTF-8') as p_file, open(summery_file_name, encoding='UTF-8') as s_file:
        while True:
            p_line = p_file.readline()
            s_line = s_file.readline()
            if p_line == "" or s_line == "":
                random.shuffle(parsed_file)
                lenth = len(parsed_file)
                train_len = int(lenth * 0.8)
                test_len = int((lenth - train_len) * 0.5)
                return parsed_file[:train_len], \
                       parsed_file[train_len:train_len + test_len], \
                       parsed_file[train_len + test_len:], \
                       current_id
                # return parsed_file, current_id
            start_of_par = 0
            p_index_letters = ''
            for i, letter in enumerate(p_line):
                if p_letter(letter):
                    start_of_par = i + 2
                    p_index_letters = p_line[:i]
                    break
            paragraph = p_line[start_of_par:]
            start_of_sum = 0
            s_index_letters = ''
            count = 0
            for i, letter in enumerate(s_line):
                if s_letter(letter):
                    count += 1
                    if occur(count):
                        start_of_sum = i + 1
                        s_index_letters = s_line[:i]
                        break
            summary = s_line[start_of_sum:]
            entry = {"id": current_id, "paragraph": paragraph, "summary": summary}
            # entry = {'id': current_id, 'paragraph': paragraph, 'summary': summary, 'p_index_letters': p_index_letters,
            #          's_index_letters': s_index_letters}
            # print(json.dumps(entry))
            parsed_file.append(entry)
            # parsed_file.append(entry)
            current_id += 1


def tap_pred(letter):
    return letter == '\t'


def dot_pred(letter):
    return letter == '.'


def tab_occur_pred_b(occur):
    return occur == 2


def tab_occur_pred(occur):
    return occur == 1


def load_parsed_file(file_sufix, occur, s_letter, p_letter, current_id):
    paragraph_path = f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/raw_files/{file_sufix}.txt'
    summary_path = f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/raw_files/{file_sufix}_summary.txt'
    # parsed_file, current_id = parse(paragraph_path, summary_path, current_id, occur, s_letter, p_letter)
    parsed_file_train, parsed_file_test, parsed_file_validate, current_id = parse(paragraph_path, summary_path,
                                                                                  current_id, occur, s_letter, p_letter)

    with open(
            f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/parsed_files/{file_sufix}_train.json',
            'w') as file:
        file.write(json.dumps(parsed_file_train, ensure_ascii=False))

    with open(
            f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/parsed_files/{file_sufix}_test.json',
            'w') as file:
        file.write(json.dumps(parsed_file_test, ensure_ascii=False))

    with open(
            f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/parsed_files/{file_sufix}_validate.json',
            'w') as file:
        file.write(json.dumps(parsed_file_validate, ensure_ascii=False))

    # for entry in parsed_file: if entry['p_index_letters'] != entry['s_index_letters']: print( f"mismatch!!!!
    # p_index_letters= {entry['p_index_letters']} s_index_letters={entry['s_index_letters']}")
    return current_id


def parser_init():
    current_id = 0
    for letter in "acdefgh":
        current_id = load_parsed_file(f'file_{letter}', tab_occur_pred, tap_pred, dot_pred, current_id)

    current_id = load_parsed_file('file_b', tab_occur_pred_b, tap_pred, dot_pred, current_id)

    names = ['israel_and_its_revival', 'land_of_israel', 'light_of_israel', 'light_of_revival', 'light_of_the_answer',
             'lights_of_holiness_a', 'lights_of_holiness_b', 'light_of_holiness_c', 'lights_of_holiness_d',
             'lights_of_the_bible', 'measures_of_sight', 'the_war']
    for name in names:
        current_id = load_parsed_file(name, tab_occur_pred, tap_pred, tap_pred, current_id)
    print(f'finished parsing text files into json files. Total number of entries: {current_id + 1}')


def concatenate_files_split(split):
    # List of JSON files to be concatenated
    json_files = glob.glob(
        f'/Users/llevi1/Desktop/personal/degree/Mini_Project/NLP-MINI-PROJECT/parsed_files/*_{split}.json')
    print(json_files)

    # Create an empty list to store the contents of each JSON file
    json_data = []
    # Iterate through each JSON file and concatenate the data into the list
    for file in json_files:
        with open(file, "r") as f:
            data = json.load(f)
            json_data.extend(data)
    # print(json_data)

    # Write the concatenated data to a new JSON file
    with open(f"rabbi_kook_{split}.json", "w") as f:
        json.dump(json_data, f, ensure_ascii=False)


def concatenate_files():
    concatenate_files_split("train")
    concatenate_files_split("test")
    concatenate_files_split("validate")


if __name__ == "__main__":
    parser_init()
    concatenate_files()
