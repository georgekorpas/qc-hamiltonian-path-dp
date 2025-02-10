import json

input_file_name = "input.json"

# Load input data from JSON file
with open(input_file_name) as f:
    dic = json.load(f)

# Extract 'extra_arguments' if present, otherwise default to an empty dictionary
extra_arguments = dic.get('extra_arguments', {})

# Extract 'solver_params' if present, otherwise default to an empty dictionary
solver_params = dic.get('solver_params', {})

# Import the run function from main.py
import main

# Execute the run function with the input data, solver parameters, and any extra arguments
result = main.run(dic['data'], solver_params, extra_arguments)

print(result)