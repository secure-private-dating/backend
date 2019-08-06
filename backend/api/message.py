from backend import app
from backend.utils import check_argument, form_argument, query_argument, check_permission
from backend.model import get_db, ObjectId, jsonify, db_get_user_groups

from flask import session
import json


@app.route('/api/message', methods=['POST'])
@form_argument
@check_argument("uid")
@check_argument("gid")
@check_argument("outercypher")
@check_argument("noncestr")
@check_argument("ephermeralpubkey")
def post_message(uid, gid, outercypher, noncestr, ephermeralpubkey):
    # print(uid, gid, outercypher, noncestr, ephermeralpubkey)
    db = get_db()
    db.messages.insert_one({
        'uid': ObjectId(uid),
        'gid': ObjectId(gid),
        'outercypher': outercypher,
        'noncestr': noncestr,
        'ephermeralpubkey': ephermeralpubkey,
    })
    return jsonify({'status': "ok"})


@app.route('/api/pull_message', methods=['POST'])
@check_permission
@form_argument
def get_message(latest_message_id='{}'):
    latest_message_dict = json.loads(latest_message_id)
    db = get_db()
    uid = session['uid']
    data = {}
    groups = db_get_user_groups(uid)
    for group in groups:
        gid = str(group['_id'])
        query = {
            'gid': ObjectId(gid),
            'uid': {'$ne': ObjectId(uid)},
        }
        if gid in latest_message_dict:
            query['_id'] = {'$gt': ObjectId(latest_message_dict[gid])}
        projection = {
            'uid': 0,
            'gid': 0,
        }
        data[gid] = list(db.messages.find(query, projection))
    return jsonify(data)
