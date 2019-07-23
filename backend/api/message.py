from backend import app
from backend.utils import check_argument, form_argument, query_argument, check_permission
from backend.model import get_db, ObjectId, jsonify

from flask import session


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


@app.route('/api/message', methods=['GET'])
@check_permission
@query_argument
@check_argument("uid")
@check_argument("gid")
def get_message(uid, gid, from_id=''):
    # print(uid, gid)
    db = get_db()
    uid = session['uid']
    query = {
        'gid': ObjectId(gid),
        'uid': {'$ne': ObjectId(uid)},
    }
    if from_id:
        query['_id'] = {'$gt': ObjectId(from_id)}
    projection = {
        'uid': 0,
        'gid': 0
    }
    data = db.messages.find(query, projection)
    return jsonify(list(data))
