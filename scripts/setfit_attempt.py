import numpy as np
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer, TrainingArguments, sample_dataset

dataset_id = "HelgeKn/wsd_categories"
model_id = "sentence-transformers/paraphrase-mpnet-base-v2"

dataset = load_dataset(dataset_id)

train_dataset = sample_dataset(dataset["train"])
eval_dataset = dataset["validation"] 

num_classes = len(train_dataset.unique("label"))
model = SetFitModel.from_pretrained(model_id, use_differentiable_head=True, head_params={"out_features": num_classes})
trainer = SetFitTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss_class=CosineSimilarityLoss,
    num_iterations=20,
    column_mapping={"text": "text", "label": "label"},
)

# trainer.freeze()
# trainer.train(body_learning_rate=1e-5, num_epochs=1)

# trainer.unfreeze(keep_body_frozen=True)
trainer.train(learning_rate=1e-2, num_epochs=50)

# trainer.train()

metrics = trainer.evaluate()
print(metrics) 

trainer.push_to_hub("HelgeKn/SemEval-multi-label-v2", token="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")

model = SetFitModel.from_pretrained("HelgeKn/SemEval-multi-label-v2")

preds = model(
    [
        "The art of change-ringing is peculiar to the English , and , like most English peculiarities , unintelligible to the rest of the world . ",
        "Of all scenes that evoke rural England , this is one of the loveliest : An ancient stone church stands amid the fields , the sound of bells cascading from its tower , calling the faithful to evensong . "
    ]
)

print(preds)



# Multilabel Approach

# model_id = "sentence-transformers/paraphrase-mpnet-base-v2"
# dataset = load_dataset("HelgeKn/wsd_categories")

# features = dataset["train"].column_names
# features.remove("text")
# features

# num_samples = 8
# samples = np.concatenate(
#     [np.random.choice(np.where(dataset["train"][f])[0], num_samples) for f in features]
# )

# def encode_labels(record):
#     return {"labels": [record[feature] for feature in features]}


# dataset = dataset.map(encode_labels)

# train_dataset = dataset["train"].select(samples)
# eval_dataset = dataset["train"].select(
#     np.setdiff1d(np.arange(len(dataset["train"])), samples)
# )

# model = SetFitModel.from_pretrained(model_id, multi_target_strategy="one-vs-rest")

# trainer = SetFitTrainer(
#     model=model,
#     train_dataset=train_dataset,
#     eval_dataset=eval_dataset,
#     loss_class=CosineSimilarityLoss,
#     num_iterations=20,
#     column_mapping={"text": "text", "labels": "label"},
# )

# trainer.train()
# metrics = trainer.evaluate()
# print(metrics)

# trainer.push_to_hub("HelgeKn/SemEval-multi-label-v1", token="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")

# model = SetFitModel.from_pretrained("HelgeKn/SemEval-multi-label-v1")

# preds = model(
#     [
#         "The art of change-ringing is peculiar to the English , and , like most English peculiarities , unintelligible to the rest of the world . ",
#         "Of all scenes that evoke rural England , this is one of the loveliest : An ancient stone church stands amid the fields , the sound of bells cascading from its tower , calling the faithful to evensong . "
#     ]
# )

# print(preds)