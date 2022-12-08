import json

from jsonschema import validate


def verify_json(json: dict, schema: dict) -> dict:
    """
    If the json doesn't follow the schema an exception will be raised.
    Else the json will be returned.
    """
    validate(instance=json, schema=schema)
    return json


def read_json_file(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data
