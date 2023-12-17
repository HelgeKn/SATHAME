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

## Installation

## Extension Guide

## Results

## License
Copyright [2023] [Helge Kneiske - Humboldt University Berlin]

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License
