from flask_socketio import send, emit
from config import socketio


# @socketio.on('message')
# def handle_client_connect_event(json):
#     print('received json: {0}'.format(str(json)))

# @socketio.on('message')
# def handle_json_button(json):
#     # it will forward the json to all clients.
#     send(json, json=True)


# @socketio.on('alert_button')
# def handle_alert_event(json):
#     # it will forward the json to all clients.
#     print('Message from client was {0}'.format(json))
#     emit('alert', 'Message from backend')
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')

def handle_my_custom_event(json):
    emit('my response', json)

@socketio.on('my test')
def handle_my_custom_event(json):
    print('vdsvdsvsdvsdvsdvsv')
    emit('myresponse', "json")