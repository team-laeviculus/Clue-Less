from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import flask_socketio

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def on_message(message):
    print(f"Received Message: {message}")
    emit("server reply", {'data': 'I got your message'})

# // event='message', namespace=
@socketio.on('message', namespace='/chat')
def on_namespace_msg(message):
    print(f"Received message on namespace /chat: {message}")
    print(f"SEssion: {session.get('room')}")

@socketio.on('connect')
def on_connect():
    print("Client connected")
    # emit('Server Response: ', {'data': 'Connected!'})
    print("Data sent")


"""
player -> 'get tokens' -> server
"""
# @socketio.on("get tokens")
# def on_get_tokens():
#     '''Connect to database, get list of tokens for game<n>'''
#     # 1. We receive message.
#     #2. Talk to database
#     all_tokens = get_tokens_from_database(game_id)
#     all_available_tokens = GetUnused(all_tokens)
#     # 3. Tell other players
#     emit("new player joined: ", {
#         "data": {
#             "tokens list": all_available_tokens
#         }
#     })


# Chatroom join/leave style rooms
@socketio.on('join')
def on_join(data):
    print(f"Received request for user to join room: {data}")
    username = data['username']
    room = data['room']
    #TODO: Logic for joining room
    flask_socketio.join_room((room))
    print(f"User {username} has joined room: {room}")
    flask_socketio.send(f"{username} has entered the room.", room=room, broadcast=True)

@socketio.on('chat message')
def on_chat_message(data):
    print(f"Received a chat message: {data}")
    username = data['username']
    room = data['room']
    message = data['message']
    emit('chat message', data={'data': message}, room=room, broadcast=True)
    emit('new player move', data={'data', "I moved to new room"}, room=room, broadcast=True)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print(f"User {username} has left room {room}")
    flask_socketio.leave_room(room)
    flask_socketio.send(f"{username} has left the room.", room=room)
if __name__ == "__main__":
    socketio.run(app)