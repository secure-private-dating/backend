import flask
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS

from backend import app


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'mongodb'):
        client = MongoClient()
        flask.g.mongodb = client[app.config['DATABASE_NAME']]
    return flask.g.mongodb


def jsonify(data):
    return dumps(data, json_options=RELAXED_JSON_OPTIONS)
