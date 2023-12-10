import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

print(tokenizer("Hello world!"))


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