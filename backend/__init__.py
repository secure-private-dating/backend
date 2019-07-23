import eventlet  # for socketio

eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO
from flask_session import Session
from backend.middleware import WeAppSessionFix

app = Flask(__name__)
# app.wsgi_app = WeAppSessionFix(app.wsgi_app)

app.config.from_object('backend.config')
app.config.from_envvar('BACKEND_SETTINGS')

if not app.config['APP_ID']:
    raise ValueError("No APP_ID set for backend")
if not app.config['APP_SECRET']:
    raise ValueError("No APP_SECRET set for backend")

socketio = SocketIO(app, async_mode='eventlet')

sess = Session()
sess.init_app(app)

import backend.api
import backend.socket

#
# @app.before_request
# def before_request_func():
#     print("before_request is running!")
#     code = request.headers.get('Authorization')
#     print(request.environ)
#     # headers = request.headers.__dict__
#     # pprint(headers)
#     # headers['HTTP_COOKIE'] = ''
#     # request.__dict__['headers'] = headers
#     # request.environ['HTTP_COOKIE'] = ''
#
#     # print(request.headers.set('Cookie', 'session=d7661218-d192-4399-b1c6-d01f380b2ec5;'))
#     # print(request.cookies.items())


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app, debug=True)
