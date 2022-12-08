"""JSON utilities  module"""
import json

from jsonschema import validate


def verify_json(json_instance: dict, schema: dict) -> dict:
    """
    If the json doesn't follow the schema an exception will be raised.
    Else the json will be returned.
    """

    validate(instance=json_instance, schema=schema)
    return json_instance


def read_json_file(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data
