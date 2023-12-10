import json

path_to_data = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\wsd.txt"

path_to_categories = r"D:\ThesisRepo\SATHAME\static\embeddings\wsd_gold.json"

data_list=[]
with open(path_to_data, "r") as file:
    # Read the file line by line
    for line in file:
        # Split the line contents into parts
        parts = line.split('###')
        # Split the first part further into two parts
        part1 = parts[0]
        part2 = parts[-1]
        # Save the parts in the list as a group
        data_list.append([part1, part2])
# Close the file
file.close()

category_list=[]
with open(path_to_categories, "r") as file:
    category_list = json.load(file)

count_category = 0
for entry in category_list:
    if entry['category'] == 'Inside Context':
        count_category += 1

labeled_category_dataset_training = []
labeled_num = 0
unlabeled_num = 0

for entry in category_list:
    if labeled_num == 8 and unlabeled_num == 8:
        break
    match = None
    for data in data_list:
        if entry['error'] in data:
            match = data
            break
    if match and not any(match[1] == sublist[1] for sublist in labeled_category_dataset_training):
        if entry['category'] == 'Inside Context':
            if labeled_num < 8:
                labeled_category_dataset_training.append([match[0], match[1], 1])
                labeled_num += 1
        else:
            if unlabeled_num < 8:
                labeled_category_dataset_training.append([match[0], match[1], 0])
                unlabeled_num += 1

labeled_category_dataset = []

for entry in category_list:
    match = None
    for data in data_list:
        if entry['error'] in data:
            match = data
            break
    if match and not any(match[1] == sublist[1] for sublist in labeled_category_dataset_training) and not any(match[1] == sublist[1] for sublist in labeled_category_dataset):
        if entry['category'] == 'Inside Context':
            labeled_category_dataset.append([match[0], match[1], 1])
        else:
            labeled_category_dataset.append([match[0], match[1], 0])

# Convert labeled_category_dataset to a list of dictionaries
labeled_category_dataset_val_dicts = [{'id': item[0], 'text': item[1], 'label': item[2]} for item in labeled_category_dataset]
labeled_category_dataset_train_dicts = [{'id': item[0], 'text': item[1], 'label': item[2]} for item in labeled_category_dataset_training]

# Write the list of dictionaries to a JSON file
with open('train.json', 'w') as file:
    json.dump(labeled_category_dataset_train_dicts, file) 
with open('validation.json', 'w') as file:
    json.dump(labeled_category_dataset_val_dicts, file)    