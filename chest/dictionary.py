"""Blueprint for the /dictionary"""

from flask import Blueprint, abort, request

from chest.db import get_db
from .utils import json_response, validate_json

bp = Blueprint('dictionary', __name__, url_prefix='/')


@bp.route('/dictionary/<string:key>', methods=['GET'])
def dictionary_get_key(key):
    """Returns value by key"""
    database = get_db()
    if key not in database.getall():
        abort(404)

    return json_response(database.get(key))


@bp.route('/dictionary', methods=['POST'])
def dictionary_post():
    """Writing a value by key"""
    database = get_db()
    json = request.get_json(True)

    if not validate_json(json):
        abort(400)

    if json['key'] in database.getall():
        abort(409)

    database.set(json['key'], json['value'])

    return json_response(json['value'])


@bp.route('/dictionary', methods=['PUT'])
def dictionary_put_key():
    """Replacing a value by key"""
    database = get_db()
    json = request.get_json(True)

    if not validate_json(json):
        abort(400)

    if json['key'] not in database.getall():
        abort(404)

    database.set(json['key'], json['value'])

    return json_response(json['value'])


@bp.route('/dictionary/<string:key>', methods=['DELETE'])
def dictionary_delete_key(key):
    """Remove value by key and return its value"""
    database = get_db()
    if key in database.getall():
        value = database.get(key)
        database.rem(key)
        return json_response(value)
    return json_response()
