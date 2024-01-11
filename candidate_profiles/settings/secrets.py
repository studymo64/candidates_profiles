import json


def get_system_key(key_name: str):
    with open("./settings/keys.json") as keys_file:
        json_data = json.load(keys_file)
    return json_data.get(key_name, None)
