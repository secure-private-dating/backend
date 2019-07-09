from backend import socketio
from flask_socketio import emit


@socketio.on('fxhnb')
def handle_message(message):
    print('received fxhnb: ' + message)
    emit('fxhnb', 'received fxhnb: ' + message)


@socketio.on('fxhsb')
def handle_message(message):
    print('received fxhsb: ' + message)
    emit('fxhsb', 'received fxhsb: ' + message)
