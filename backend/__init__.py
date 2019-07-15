import eventlet  # for socketio

eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

app.config.from_object('backend.config')

socketio = SocketIO(app, async_mode='eventlet')

import backend.api
import backend.socket


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app, debug=True)
