import json

def read_json(file_name):
    with open(file_name) as file:
        json_text=json.load(file)
        return json_text

#print(read_json("state.json")["ready"]["message"])
