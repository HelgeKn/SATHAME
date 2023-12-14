import transformers
import json

schema_path = r"D:\ThesisRepo\SATHAME\static\schemas\BEA2019_Gold.json"

with open(schema_path, 'r') as file:
    data = json.load(file)

consolidated_combinations = []
for combination in data['combinations']:
    if combination['category'] == 'unclear':
        consolidated_combinations.append({'category': 'wording', 'error': combination['error']})
    elif combination['category'] == 'pronoun':
        consolidated_combinations.append({'category': 'preposition', 'error': combination['error']})
    elif combination['category'] == 'capital':
        consolidated_combinations.append({'category': 'spelling', 'error': combination['error']})
    elif combination['category'] == 'deletions':
        consolidated_combinations.append({'category': 'wording', 'error': combination['error']})
    elif combination['category'] == 'article':
        consolidated_combinations.append({'category': 'preposition', 'error': combination['error']})
    else:
        consolidated_combinations.append(combination)

data['combinations'] = consolidated_combinations

with open("BEA2019_Gold_Consolidated.json", 'w') as file:
    json.dump(data, file)

# dataset_path = r"D:\ThesisRepo\SATHAME\static\datasets\BEA2019\BEA2019.txt"
# try:
#     with open(dataset_path, 'r', encoding='utf-8') as file:
#         data = file.read()
    
#     # Parse the data
#     parsed_data = []
#     for line in data.splitlines():
#         if line: # Ignore empty lines
#             overall_values = line.split('###')
#             for i in range(1, 3): # Parse predictions and labels
#                 overall_values[i] = [item.split('|||') for item in overall_values[i].split('@@@')]
#             parsed_data.append({
#                 'id': overall_values[0],
#                 'prediction': overall_values[1],
#                 'label': overall_values[2],
#                 'text': overall_values[-1]
#             })
#     print({'data': parsed_data})
# except Exception as e:
#     print(str(e))

# path_to_data = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\wsd.txt"

# data_list=[]
# with open(path_to_data, "r") as file:
#     # Read the file line by line
#     for line in file:
#         # Split the line contents into parts
#         parts = line.split('###')
#         # Split the first part further into two parts
#         part1 = parts[0]

#         full_id = part1.split('.')
#         full_id.pop()
#         sentence_id = '.'.join(full_id)

#         # Save the parts in the list as a group
#         data_list.append(sentence_id)
# # Close the file
# file.close()

# unique_values = set(data_list)
# print(len(unique_values))