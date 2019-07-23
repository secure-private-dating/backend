from backend import app
from backend.utils import check_argument, query_argument
from backend.model import get_db, jsonify

import requests
import json
from flask import session


@app.route('/user/login')
@query_argument
@check_argument("code")
def login(code):
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
                'name': '',
                'avatar': '',
                'publicKey': '',
            })
            row = db.users.find_one({'openid': data['openid']})

        session['openid'] = data['openid']
        session['session_key'] = data['session_key']
        session['uid'] = row['_id']
        print(row)
        print(session.sid)
        return jsonify({'sid': session.sid, 'uid': row['_id'], 'publicKey': row['publicKey']})
    else:
        pass
