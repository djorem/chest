"""Helper utilitie"""

from datetime import datetime
from jsonschema import validate, exceptions
from flask import jsonify


def validate_json(json):
    """
    Validate json with a json schema
    like
    {
        "key": "mail.ru",
        "value": "target"
    }
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "title": "kv",
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "minLength": 1,
                "pattern": "^[^\\s]*$"
            },
            "value": {
                "type": "string"
            },
        },
        "required": ["key", "value"],
        "additionalProperties": False
    }
    try:
        validate(instance=json, schema=schema)
    except exceptions.ValidationError:
        return False
    return True


def json_response(value=None):
    """ Return a flask.wrappers.Response object containing json in accepted response format """
    return jsonify({
        "result": value,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
