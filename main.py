from flask import Flask, render_template, request
from schema_generator import generate_schema
import os
import json

from flask.json import jsonify

app = Flask(__name__)

@app.route("/")
def home():
    # Get the list of available schemas
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'schemas')
    schema_list = [os.path.splitext(f)[0] for f in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, f))]
    
    return render_template("index.html", contenta="Dataset", contentb="Error schema", datainput="Data entry", prediction="Prediction", truelabel="Label", schema_list = schema_list)

@app.route('/save-schema', methods=['POST'])
def handle_post():
    data = request.get_json()
    selected_schema = data['selectedSchema']
    dataset = data['dataset']
    json_file_path = f'static/schemas/{selected_schema}.json'

    try:
        with open(json_file_path, 'w') as file:
            schema_data = {
                'combinations' : data['combinations'],
                'dataset' : dataset
            }
            json.dump(schema_data, file)
        return jsonify({'message': 'Success!'}), 200
    except Exception as e:
        return str(e), 500
    
@app.route('/get-schema/<schema>', methods=['GET'])
def get_schema(schema):
  json_file_path = f'static/schemas/{schema}.json'
  try:
    with open(json_file_path, 'r') as file:
      data = json.load(file)
    return jsonify(data), 200
  except Exception as e:
    return str(e), 500
  
@app.route('/get-dataset-names', methods=['GET'])
def get_dataset_names():
    dataset_path = os.path.join(os.path.dirname(__file__), 'static/datasets')
    try:
        dataset_names = [name for name in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, name))]
        return jsonify(dataset_names), 200
    except Exception as e:
        return str(e), 500
    
@app.route('/get-dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    dataset_path = os.path.join(os.path.dirname(__file__), 'static/datasets', dataset_name, f'{dataset_name}.txt')
    try:
        with open(dataset_path, 'r', encoding='utf-8') as file:
            data = file.read()
        
        # Parse the data
        parsed_data = []
        for line in data.splitlines():
          if line: # Ignore empty lines
            overall_values = line.split('###')
            for i in range(1, 3): # Parse predictions and labels
               overall_values[i] = [item.split('|||') for item in overall_values[i].split('@@@')]
            parsed_data.append({
                'id': overall_values[0],
                'prediction': overall_values[1],
                'label': overall_values[2],
                'text': overall_values[-1]
            })
        return jsonify({'data': parsed_data}), 200
    except Exception as e:
        return str(e), 500
    
@app.route('/generate-schema', methods=['POST'])
def generate_schema():
    data = request.get_json()
    isChecked = data.get('isChecked')
    selectedSchema = data.get('selectedSchema')

    job_id = generate_schema(isChecked, selectedSchema)

    return jsonify({'message': 'Schema generation started', 'job_id': job_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)