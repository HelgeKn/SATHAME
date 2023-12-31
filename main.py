from flask import Flask, render_template, request
from schema_generator import generate_schema
from rq.job import Job
from rq.exceptions import NoSuchJobError
from redis import Redis
import os
import json

from flask.json import jsonify

redis_conn = Redis()

app = Flask(__name__)

@app.route("/")
def home():
    # Get the list of available schemas
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'schemas')
    schema_list = [os.path.splitext(f)[0] for f in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, f))]
    
    return render_template("index.html", contenta="Dataset", contentb="Error schema", datainput="Data entry", prediction="Prediction", truelabel="Label", schema_list = schema_list)


# Endpoint to create a new schema or update an existing one
# Receives the schema name, the dataset name, and the combinations
# Returns a message and a status code - schema is saved to a file
@app.route('/save-schema', methods=['POST'])
def handle_post():
    data = request.get_json()
    selected_schema = data['selectedSchema']
    dataset = data['dataset']
    json_file_path = os.path.join('static','schemas', f'{selected_schema}.json')

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

# Endpoint to get the a selected schema
# Receives the schema name
# Returns the schema as a JSON object - contains dataset name and combinations    
@app.route('/get-schema/<schema>', methods=['GET'])
def get_schema(schema):
  json_file_path = os.path.join('static','schemas',f'{schema}.json')
  try:
    with open(json_file_path, 'r') as file:
      data = json.load(file)
    return jsonify(data), 200
  except Exception as e:
    return str(e), 500
  
# Endpoint to get the list of available datasets
# Returns the list of datasets by returning the names of the folders in the datasets folder
# The dataset loaded into the UI always has the same name as the folder it is in  
@app.route('/get-dataset-names', methods=['GET'])
def get_dataset_names():
    dataset_path = os.path.join(os.path.dirname(__file__),'static','datasets')
    try:
        dataset_names = [name for name in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, name))]
        return jsonify(dataset_names), 200
    except Exception as e:
        return str(e), 500

# Endpoint to get the data from a selected dataset
# Receives the dataset name
# Returns the data as a JSON object - contains the id, prediction, label, and text for each entry    
@app.route('/get-dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    dataset_path = os.path.join(os.path.dirname(__file__), 'static', 'datasets', dataset_name, f'{dataset_name}.txt')
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
    
# Endpoint to trigger the schema generation
# Receives the isChecked and selectedSchema parameters
#   isChecked (should model be uploaded)    -   is a boolean
#   selectedSchema (schema containing the training combinations)    -  is a dictionary and contains the dataset name and the combinations   
@app.route('/generate-schema', methods=['POST'])
def generate_schema_endpoint():
    data = request.get_json()
    isChecked = data.get('isChecked')
    selectedSchema = data.get('selectedSchema')

    try:
        job_id = generate_schema(isChecked, selectedSchema)
    except Exception as e:
        job_id = None

    return jsonify({'message': 'Schema generation started', 'job_id': job_id}), 200

# Endpoint to get the status of a job
# Receives the job_id parameter
# Returns the status of the job as a JSON object - contains the job_id and the status
# Jobs are only used for schema generation
@app.route('/job-status', methods=['GET'])
def job_status():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'Missing job_id parameter'}), 400

    try:
        job = Job.fetch(job_id, connection=redis_conn)
        status = job.get_status()
    except NoSuchJobError:
        status = None

    if status is None:
        return jsonify({'error': 'Invalid job_id'}), 404

    return jsonify({'job_id': job_id, 'status': status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)