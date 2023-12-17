from rq import Queue, get_current_job
from redis import Redis
import json
import os
from huggingface_hub import HfApi
import numpy as np
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer, sample_dataset

# Set up a Redis connection and initialize a queue
redis_conn = Redis()
q = Queue(connection=redis_conn)

api = HfApi()
generator_repo = "HelgeKn/SATHAME-generator-train"
model_id = "sentence-transformers/paraphrase-mpnet-base-v2"
huggingbase = "HelgeKn/"
huggingtoken = "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"

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

def train_model(isChecked, selectedSchema):
    # Get the current job
    job = get_current_job()

    # Get the job ID
    job_id = job.get_id() if job else None
    
    schema_path = os.path.join('static','schemas', f'{selectedSchema}.json')
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    
    dataset_name = schema['dataset']
    dataset_path = os.path.join('static', 'datasets', dataset_name, f'{dataset_name}.txt')

    data_list=[]
    text_list = []
    full_ids = []
    with open(dataset_path, "r", encoding="utf-8") as file:
        # Read the file line by line
        for line in file:
            # Split the line contents into parts
            parts = line.split('###')
            # Split the first part further into two parts
            part1 = parts[0]
            part2 = parts[-1]
            # Save the parts in the list as a group
            text_list.append(part2)
            full_ids.append(part1)
            data_list.append([part1, part2])
    # Close the file
    file.close()

    category_list=[]
    category_list = schema['combinations']

    # Create a set of unique errors
    unique_categories = set(entry['category'] for entry in category_list)

    # Create a dictionary where the keys are the unique errors and the values are the unique numbers
    category_to_number = {category: number for number, category in enumerate(unique_categories)}

    train_json = create_json(category_list, data_list, category_to_number)
    
    # Save train_json to a file
    output_filename = f'train_{job_id}.json' if job_id else 'train.json'
    output_path = os.path.join('static', 'generator', output_filename)
    with open(output_path, 'w') as file2:
        file2.write(train_json)
    
    api.upload_file(
        path_or_fileobj=output_path,
        path_in_repo="train.json",
        repo_id=generator_repo,
        repo_type="dataset",
        token=huggingtoken,
    )

    with open (output_path, 'r') as file3:
        train_json = json.load(file3)

    dataset = load_dataset(generator_repo)

    eval_dataset = sample_dataset(dataset["train"], label_column="label", num_samples=1)
    train_dataset = dataset["train"] 

    num_classes = len(train_dataset.unique("label"))
    model = SetFitModel.from_pretrained(model_id, use_differentiable_head=True, head_params={"out_features": num_classes})

    trainer = SetFitTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss_class=CosineSimilarityLoss,
        num_iterations=20,
        num_epochs=2,
        column_mapping={"text": "text", "label": "label"},
    )

    trainer.train()

    if isChecked:
        classifier_id = huggingbase + selectedSchema + '-' + job_id
        trainer.push_to_hub(classifier_id, token=huggingtoken)

    preds = model(text_list)
    preds_np = preds.numpy()

    prediction_dict = {}
    category_dict = {}

    for pred, full in zip(preds_np, data_list):
        key = next((k for k, v in category_to_number.items() if v == pred), None)
        prediction_dict[full[0]] = key

    correct_count = 0
    for category in category_list:
        if prediction_dict[category['error']] == category['category']:
            correct_count += 1
    
    accuracy = correct_count / len(category_list)

    print(f"Accuracy for {job_id}: {accuracy}")

    counts = np.bincount(preds_np)

    for count, key in zip(counts, category_to_number):
        category_dict[key] = count

    # Convert numpy integers in category_dict to Python integers
    category_dict = {k: int(v) for k, v in category_dict.items()}

    prep = {'accuracy': accuracy, 'counts': category_dict}
    
    new_combinations = []

    for sample in train_json:
        category = next((combination["category"] for combination in category_list if combination["error"] == sample["id"]), None)
        new_combination = {"error": sample["id"], "category": category}
        new_combinations.append(new_combination)

    gen_stats_name = selectedSchema + '_Gen_' + job_id
    gen_stats_path = os.path.join('static','statistics',dataset_name, f'{gen_stats_name}.json')
    with open(gen_stats_path, 'w') as file5:
        json.dump(prep, file5)

    prediction_dict = []
    category_dict = {}

    for pred, full in zip(preds_np, full_ids):
        if any(full == combination["error"] for combination in new_combinations):
            category = next((combination["category"] for combination in new_combinations if combination["error"] == full), None)
            prep = {'error': full, 'category': category}
            prediction_dict.append(prep)
        else:
            key = next((k for k, v in category_to_number.items() if v == pred), None)
            prep = {'error': full, 'category': key}
            prediction_dict.append(prep)

    schema['combinations'] = prediction_dict

    gen_schema_name = selectedSchema + '_Gen'
    schema_path = os.path.join('static','schemas', f'{gen_schema_name}.json')
    with open(schema_path, 'w') as file7:
        json.dump(schema, file7)

def generate_schema(isChecked, selectedSchema):
    # This will add long_running_task to the queue and return immediately
    job = q.enqueue(train_model, isChecked, selectedSchema)

    train_model(isChecked, selectedSchema)
    return job.get_id()  # Returns the ID of the job

# generate_schema(True, 'Testing')