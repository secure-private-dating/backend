# Echo client program
import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000', namespaces=['/'])


@sio.on('fxhsb')
def on_message(data):
    print('I received a message!')
    print(data)


@sio.on('fxhnb')
def on_message(data):
    print('I received a message!')
    print(data)


sio.emit('fxhnb', 'fxhnb')
sio.emit('fxhsb', 'fxhsb')
