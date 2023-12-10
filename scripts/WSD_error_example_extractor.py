import xml.etree.ElementTree as ET

# This script only works with GLOSSBERT repository

def extract_results(result_file_path):
    result_list = []

    with open(result_file_path, "r") as file:
        # Read the file line by line
        for line in file:
            # Split the line contents into parts
            parts = line.split()
            # Split the first part further into two parts
            part1 = parts[0]
            part2 = parts[1]
            # Save the parts in the list as a group
            result_list.append([part1, part2])

    # Close the file
    file.close()

    return result_list

def get_sentence_by_id(root, sentence_id):
    for text in root:
        for sentence in text:
            if sentence.attrib["id"] == sentence_id:
                full_sentence = ""
                for word in sentence:
                    full_sentence += word.text + " "
                return full_sentence

def generate_full_token_set():
    # Fetch the results
    result_file_path = r"path_to_final_result_ALL.txt"
    result = extract_results(result_file_path)

    # Fetch the evaluation dataset
    eval_file_path = r"path_to_all_gold_keys.txt"
    eval = extract_results(eval_file_path)

    # XML file containing full text
    xml_file_path = r"path_to_all_data.xml"
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Compare the results
    mismatched_result = []
    mismatched_eval = []

    for i in range(len(result)):
        if result[i][1] != eval[i][1]:
            mismatched_result.append(result[i])
            mismatched_eval.append(eval[i])

    # Load the dictionary from wordnet as nested list
    word_sense_path = r"path_to_index.sense.gloss"
    dic_list = []
    with open(word_sense_path, "r") as new_file:
        for line in new_file:
            line_values = line.strip().split("\t")
            if line_values:
                first_value = line_values[0]
                last_value = line_values[-1]
                dic_list.append([first_value, last_value])

    # Add wordnet definitions to mismatched_result
    for i in range(len(dic_list)):
        for j in range(len(mismatched_result)):
            if dic_list[i][0] == mismatched_result[j][1]:
                mismatched_result[j].append(dic_list[i][1])

    # Add wordnet definitions to mismatched_eval
    for i in range(len(dic_list)):
        for j in range(len(mismatched_eval)):
            if dic_list[i][0] == mismatched_eval[j][1]:
                mismatched_eval[j].append(dic_list[i][1])


    # Combine mismatched_result and mismatched_eval based on first value
    for i in range(len(mismatched_result)):
        for j in range(len(mismatched_eval)):
            if mismatched_result[i][0] == mismatched_eval[j][0]:
                mismatched_result[i].extend(mismatched_eval[j][1:])

    # Add full sentence to the set
    for i in range(len(mismatched_result)):
        split = mismatched_result[i][0].split(".")
        sentence_id = split[0] + "." + split[1] + "." + split[2]
        mismatched_result[i].append(get_sentence_by_id(root, sentence_id))

    # Write final set to a text file
    output_file_path = r"output_path.txt"
    separator = "###"  # Choose a separator that is not used in mismatched_result

    with open(output_file_path, "w") as file:
        for sublist in mismatched_result:
            line = separator.join(sublist)
            file.write(line + "\n")

def generate_sentence_set(token_set_path):
    with open(token_set_path, "r") as file, \
         open('wsd_sentence.txt', 'w', encoding='utf-8') as output:
        data_lines = file.readlines()

        current_sentence_id = ""
        current_sentence_text = ""
        prediction_list = []
        label_list = []
        for data_line in data_lines:
            split_line = data_line.split("###")

            id_line = split_line[0].split(".")
            sentence_id = id_line[0] + "." + id_line[1] + "." + id_line[2]

            if not current_sentence_id:
                current_sentence_id = sentence_id
                current_sentence_text = split_line[5]
            
            if current_sentence_id != sentence_id:
                predictions = "@@@".join(prediction_list)
                labels = "@@@".join(label_list)
                output.write(f'{current_sentence_id}###{predictions}###{labels}###{current_sentence_text}\n')
                current_sentence_id = sentence_id
                current_sentence_text = split_line[5]
                prediction_list = []
                label_list = []
            
            prediction_line = '|||'.join(split_line[1:3])
            prediction_list.append(prediction_line)
            label_line = '|||'.join(split_line[3:5])
            label_list.append(label_line)

path = r'D:\ThesisRepo\SATHAME\static\datasets\SemEval\wsd.txt'
generate_sentence_set(path)
print("Done")
# word.tag, word.attrib, word.text