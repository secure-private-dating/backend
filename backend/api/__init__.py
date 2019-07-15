# from flask import jsonify
from backend import app
from backend.utils import check_argument, query_argument, form_argument
from backend.model import get_db, ObjectId, jsonify


@app.route('/api/groups')
@query_argument
@check_argument("uid")
def get_user_groups(uid):
    db = get_db()
    # print(uid)
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

