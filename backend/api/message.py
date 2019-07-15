from backend import app
from backend.utils import check_argument, form_argument
from backend.model import get_db, ObjectId, jsonify


@app.route('/api/message', methods=['POST'])
@form_argument
@check_argument("uid")
@check_argument("gid")
# @check_argument("outercypher")
# @check_argument("noncestr")
# @check_argument("ephermeralpubkey")
# def post_message(uid, gid, outercypher, noncestr, ephermeralpubkey):
#     print(uid, gid, outercypher, noncestr, ephermeralpubkey)
def post_message(uid, gid):
    print(uid, gid)
    return jsonify([uid, gid])
