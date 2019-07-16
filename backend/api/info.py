# from flask import jsonify
from backend import app
from backend.utils import check_argument, query_argument
from backend.model import get_db, ObjectId, jsonify


@app.route('/api/groups')
@query_argument
@check_argument("uid")
def get_user_groups(uid):
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
    # print(jsonify(data))
    return jsonify(data)


@app.route('/api/user')
@query_argument
@check_argument("uid")
def get_user(uid):
    db = get_db()
    data = db.users.find_one({
        '_id': ObjectId(uid)
    })
    return jsonify(data)


@app.route('/api/group_users')
@query_argument
@check_argument("gid")
def get_group_users(gid):
    db = get_db()
    pipeline = [{
        "$match": {
            "gid": ObjectId(gid)
        }
    }, {
        "$lookup": {
            "from": "users",
            "localField": "uid",
            "foreignField": "_id",
            "as": "user"
        }
    }, {
        "$group": {
            "_id": "$gid",
            "users": {"$push": {"$arrayElemAt": ["$user", 0]}}
        }
    }]
    data = list(db.group_user.aggregate(pipeline))
    if data:
        data = data[0]["users"]
    # print(jsonify(data))
    return jsonify(data)
