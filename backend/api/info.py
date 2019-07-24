# from flask import jsonify
from backend import app
from backend.utils import check_argument, query_argument, check_permission
from backend.model import get_db, ObjectId, jsonify, db_get_user_groups

from flask import session


@app.route('/api/groups')
@check_permission
@query_argument
@check_argument("uid")
def get_user_groups(uid):
    uid = session['uid']
    data = db_get_user_groups(uid)
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


@app.route('/api/group')
@query_argument
@check_argument("gid")
def get_group(gid):
    db = get_db()
    data = db.groups.find_one({
        '_id': ObjectId(gid)
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
