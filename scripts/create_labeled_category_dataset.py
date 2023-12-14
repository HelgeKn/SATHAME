import json
import random

def create_json(category_samples, data_list, category_to_number):
    # Create an empty list to store the dictionaries
    json_list = []

    # Iterate over category_samples
    for category_sample in category_samples:
        # Create a dictionary for each sample
        sample_dict = {
            "id": category_sample['error'],
            "text": next((data[1] for data in data_list if data[0] == category_sample['error']), None).rstrip('\n'),
            "label": category_to_number[category_sample['category']]
        }
        
        # Append the dictionary to the list
        json_list.append(sample_dict)

    # Convert the list to a JSON string
    json_string = json.dumps(json_list)

    return json_string

path_to_data = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\SemEval.txt"

path_to_categories = r"D:\ThesisRepo\SATHAME\static\schemas\SemEval_Gold.json"

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
    data = json.load(file)
    category_list = data['combinations']

# Create a set of unique errors
unique_categories = set(entry['category'] for entry in category_list)

# Create a dictionary where the keys are the unique errors and the values are the unique numbers
category_to_number = {category: number for number, category in enumerate(unique_categories)}

category_samples = []
for category in unique_categories:
    # Select 10 random entries for this category
    samples = random.sample([entry for entry in category_list if entry['category'] == category], 10)
    
    # Add the samples to the list
    category_samples.extend(samples)
    
    # Remove the selected samples from category_list
    category_list = [entry for entry in category_list if entry not in samples]

train_json = create_json(category_samples, data_list, category_to_number)

val_json = create_json(category_list, data_list, category_to_number)

# Save train_json to a file
with open('train.json', 'w') as file:
    file.write(train_json)

# Save val_json to a file
with open('validation.json', 'w') as file:
    file.write(val_json)