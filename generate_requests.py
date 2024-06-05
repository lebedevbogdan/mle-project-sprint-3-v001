import requests
import time
import json

with open('services/models/input_example.json', 'r') as json_file:
    example = json.load(json_file)
example_dict = dict(zip(example['columns'], example['data'][0]))

for j in range(50):
    for i in range(3):
        params = dict(zip(example['columns'], example['data'][i]))
        response = requests.post('http://localhost:1702/predict?flat_id=11111', json=params)
    time.sleep(1)