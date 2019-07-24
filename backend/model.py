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


def db_get_user_groups(uid):
    db = get_db()
    pipeline = [{
        "$match": {
            "uid": ObjectId(uid)
        }
    }, {
        "$lookup": {
            "from": "groups",
            "localField": "gid",
            "foreignField": "_id",
            "as": "group"
        }
    }, {
        "$group": {
            "_id": "$uid",
            "groups": {"$push": {"$arrayElemAt": ["$group", 0]}}
        }
    }]
    data = list(db.group_user.aggregate(pipeline))
    if data:
        data = data[0]["groups"]
    return data
