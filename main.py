from flask import Flask, render_template, request
import os
import json

from flask.json import jsonify

app = Flask(__name__)

@app.route("/")
def home():
    with open('static/datasets/SemEval/wsd.txt', 'r') as file:
        data = file.read()

    # Split the data on the "###" separator and store each line in a nested list
    data = [line.split("###") for line in data.split("\n") if line]
    
    # Create a list with the first element of each nested list
    error_example_list = [line[0] for line in data]

    # Get the list of available schemas
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'schemas')
    schema_list = [os.path.splitext(f)[0] for f in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, f))]
    
    return render_template("index.html", contenta="SemEval", contentb="Error schema", datainput="Data entry", prediction="Prediction", truelabel="Label", file_data=data, error_example_list=error_example_list, schema_list = schema_list)

@app.route('/save-schema', methods=['POST'])
def handle_post():
    data = request.get_json()
    selected_schema = data['selectedSchema']
    json_file_path = f'static/schemas/{selected_schema}.json'

    try:
        with open(json_file_path, 'w') as file:
            json.dump(data['combinations'], file)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)