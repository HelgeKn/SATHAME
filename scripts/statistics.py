import numpy as np
import json
from datasets import load_dataset
from setfit import SetFitModel

def create_dataset_statistics(path_to_data, classifier_id_base, path_to_schema):
    data_list=[]
    full_list = []
    with open(path_to_data, "r", encoding="UTF-8") as file1:
        # Read the file line by line
        for line in file1:
            # Split the line contents into parts
            parts = line.split('###')
            # Split the first part further into two parts
            part1 = parts[0]
            part2 = parts[-1]
            # Save the parts in the list as a group
            full_list.append([part1, part2])
            data_list.append(part2)
    # Close the file
    file1.close()

    with open(path_to_schema, "r") as file2:
        data = json.load(file2)
        category_list = data['combinations']
    # Close the file
    file2.close()

    path_to_10mapping = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\10_example_set\SemEval_mapping.json"
    with open(path_to_10mapping, "r") as file3:
        data = json.load(file3)
        category_to_number = data

    path_to_20mapping = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\20_example_set\SemEval_mapping.json"
    with open(path_to_20mapping, "r") as file4:
        data = json.load(file4)
        category_to_number_20 = data

    for i in range(4, 12, 2):
        classifier_id = classifier_id_base + str(i)
        model = SetFitModel.from_pretrained(classifier_id)

        preds = model(data_list)
        preds_np = preds.numpy()

        prediction_dict = {}
        category_dict = {}

        for pred, full in zip(preds_np, full_list):
            key = next((k for k, v in category_to_number.items() if v == pred), None)
            prediction_dict[full[0]] = key

        correct_count = 0
        for category in category_list:
            if prediction_dict[category['error']] == category['category']:
                correct_count += 1
        
        accuracy = correct_count / len(category_list)

        print(f"Accuracy for {i} iterations: {accuracy}")

        counts = np.bincount(preds_np)

        for count, key in zip(counts, category_to_number_20):
            category_dict[key] = count

        # Convert numpy integers in category_dict to Python integers
        category_dict = {k: int(v) for k, v in category_dict.items()}

        prep = {'accuracy': accuracy, 'counts': category_dict}
        
        path = f"SemEval_Stats_{i}.json"
        with open(path, 'w') as file5:
            json.dump(prep, file5)
    
    # Separate stat extraction because of mapping for 20 examples per class
    classifier_id = classifier_id_base + str(20)
    model = SetFitModel.from_pretrained(classifier_id)

    preds = model(data_list)
    preds_np = preds.numpy()

    prediction_dict = {}
    category_dict = {}

    for pred, full in zip(preds_np, full_list):
        key = next((k for k, v in category_to_number_20.items() if v == pred), None)
        prediction_dict[full[0]] = key

    correct_count = 0
    for category in category_list:
        if prediction_dict[category['error']] == category['category']:
            correct_count += 1
    
    accuracy = correct_count / len(category_list)

    print(f"Accuracy for 20 iterations: {accuracy}")

    counts = np.bincount(preds_np)

    for count, key in zip(counts, category_to_number_20):
        category_dict[key] = count

    # Convert numpy integers in category_dict to Python integers
    category_dict = {k: int(v) for k, v in category_dict.items()}

    prep = {'accuracy': accuracy, 'counts': category_dict}
    
    with open("SemEval_Stats_20.json", 'w') as file5:
        json.dump(prep, file5)


# Main code
path_to_data = r"D:\ThesisRepo\SATHAME\static\datasets\SemEval\SemEval.txt"
path_to_schema = r"D:\ThesisRepo\SATHAME\static\schemas\SemEval_Gold.json"
classifier_id_base = "HelgeKn/SemEval-multi-class-"

create_dataset_statistics(path_to_data, classifier_id_base, path_to_schema)
