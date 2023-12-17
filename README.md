# SATHAME
semi-automated tool helping analyse model errors - bachelor thesis HU Berlin

## Motivation

Related work in error analysis for language models indicates few standards and best practices.
The available tools lead many projects toward manual error analysis, which is time-consuming and tedious.
This tool aims to provide a starting point for developers of any skill level. 
You create some error categories and label a few errors for each category, and a sentence transformer combined with a classifier head does the rest.
A generated schema then indicates the following steps and areas that promise significant results worth your time.

## Features
### SATHAME UI
![Example of SATHAME UI](static/images/SATHAME_Full_UI_Labeled.png?raw=true "SATHAME UI")

1 - Name of the dataset - Number of entries - Number of categorized errors - Search the error list - Filter list by category

2 - Display for the full text of each error of the list

3 - Display for the predictions made by the original language model

4 - Display for the gold labels for the dataset

5 - Schema select box and list of error categories contained in the schema with error counter

6 - Input field to create a new schema (requires a dataset selection on a modal) or category

7 - Error list containing the errors ids for all dataset entries

"Models" - Top bar - optional dialog to trigger classifier fine-tuning from the tool UI

### Scripts
Editing schemas and labeling of errors is best done through the UI. However, the repository contains a range of scripts. 
They can be found in the directory "scripts".

Dataset formatting - Sets of prediction errors are consumed as txt files. A range of "error-example-extractor" scripts showcase conversions for three dataset examples.

Fine-tuning a classification head - This project uses [SetFit](https://github.com/huggingface/setfit) and [Huggingface](https://huggingface.co) to fine-tune pretrained models and manage models / training data. Check out the "setfit_fine-tuning_classifier" script for more details.

Results - The "statistics" script from the repository helps to calculate overall statistics like accuracy or category distribution for the fine-tuned models.

## Code Examples
SATHAME was developed and tested on python 3.9+

The schemas for error clustering are based on a json file with the following structure:
``` python
combinations = [{
  'error' : errorID
  'category' : selectedCategory
}]

schema = {
    'combinations' : combinations,
    'dataset' : datasetName
}
```
Because of the older version of SetFit this project still includes the "SetFitTrainer" instead of "Trainer". These are the default settings in the script and flask endpoint:
``` python
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
```
This project includes Hugging Face to unlock SATHAME's full capabilities and track all your work. Hugging Face is used explicitly for training sets and model tracking. SetFit harmonizes well with the API, so this project also adapted Hugging Face.

## Installation
The project contains a [requirements.txt](requirements.txt) with specific versions of each python library used.

``` sh
﻿datasets
Flask
huggingface-hub
redis
sentence-transformers
setfit
transformers
``` 
Redis is only required if you want to trigger fine-tuning from the SATHAME UI to track the fine-tuning job and run it in the background.
Ensure your Redis Server runs on the default port (localhost:6379) for the system to reach it.

The "https://huggingface.co/HelgeKn" repository contains a testing dataset and room for models, but it is recommended to use your own.
Adjust the "schema_generator.py" and the "setfit_fine-tuning_classifier.py" parameters to work with your huggingface repository.

If you want to use the UI on your local device - navigate to the root of the repository, install requirements, and run:
``` sh
python main.py
```

## Extension Guide

Check out the main.py and corresponding index.html or main.css to improve the UI or add custom functionality. These three files build the foundation for the Flask app.
Example datasets and their corresponding schema are in the "static" directory. Flask has access to all files in that directory.

The scripts should be received as an open invitation to customize them for your needs. Implementing more options into schemas to adjust hyperparameters could considerably improve usability.

## License
Copyright [2023] [Helge Kneiske - Humboldt University Berlin]

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License
