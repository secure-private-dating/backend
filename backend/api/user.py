from backend import app
from backend.utils import check_argument, form_argument, query_argument, check_permission
from backend.model import get_db, jsonify, db_get_user_groups

import requests
import json
from flask import session


@app.route('/user/login', methods=['POST'])
@form_argument
@check_argument("code")
@check_argument("name")
@check_argument("avatar")
@check_argument("gender")
def login(code, name, avatar, gender):
    params = {
        'appid': app.config['APP_ID'],
        'secret': app.config['APP_SECRET'],
        'js_code': code,
        'grant_type': 'authorization_code',
    }
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
    data = json.loads(r.text)
    if data['openid']:
        db = get_db()
        row = db.users.find_one({'openid': data['openid']})
        if not row:
            # register
            db.users.insert({
                'openid': data['openid'],
                'name': name,
                'avatar': avatar,
                'gender': gender,
                'publicKey': '',
            })
            row = db.users.find_one({'openid': data['openid']})
        elif name != row['name'] or avatar != row['avatar'] or gender != row['gender']:
            # update user info
            db.users.update({
                '_id': row['_id']
            }, {
                '$set': {
                    'name': name,
                    'avatar': avatar,
                    'gender': gender,
                }
            })
        session['openid'] = data['openid']
        session['session_key'] = data['session_key']
        session['uid'] = row['_id']
        print(row)
        print(session.sid)
        return jsonify({
            'sid': session.sid,
            'uid': row['_id'],
            'publicKey': row['publicKey'],
            'avatar': row['avatar'],
        })
    else:
        pass


@app.route('/user/update_public_key')
@check_permission
@query_argument
@check_argument("key")
def update_public_key(key):
    uid = session['uid']
    db = get_db()
    db.users.update({
        '_id': uid
    }, {
        '$set': {
            'publicKey': key,
        }
    })
    return jsonify({'status': 'ok'})
