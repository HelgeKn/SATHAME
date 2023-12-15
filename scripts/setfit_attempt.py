import numpy as np
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer, TrainingArguments, sample_dataset

dataset_id = "HelgeKn/Swag_categories"
classifier_id = "HelgeKn/Swag-multi-class-4"
model_id = "sentence-transformers/paraphrase-mpnet-base-v2"

dataset = load_dataset(dataset_id)

train_dataset = sample_dataset(dataset["train"], label_column="label", num_samples=4)
eval_dataset = dataset["validation"] 

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

metrics = trainer.evaluate()
print(metrics) 

trainer.push_to_hub(classifier_id, token="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")

path_to_data = r"D:\ThesisRepo\SATHAME\static\datasets\Swag\Swag.txt"
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
        data_list.append(part2)
# Close the file
file.close()

model = SetFitModel.from_pretrained(classifier_id)

preds = model(data_list)

preds_np = preds.numpy()
counts = np.bincount(preds_np)

print(counts)