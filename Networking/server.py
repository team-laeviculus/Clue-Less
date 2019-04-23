from flask_restful import Resource, Api, reqparse
from flask_socketio import SocketIO, emit
import flask_socketio
# from Networking import logger

from http import HTTPStatus
import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging
# Ensure you have your virtual environment properly set up and activated
# PyCharm should automatically do this for you
from Logs.Logging import create_server_logger
from Databases.DBController import *
from Networking.RESTResources import *
from Networking import socketio, app

logger = create_server_logger()




@socketio.on('message')
def on_message(message):
    logger.debug(f"Received Message: {message}")
    emit("server reply", {'data': 'I got your message'})


# // event='message', namespace=
@socketio.on('message', namespace='/chat')
def on_namespace_msg(message):
    logger.debug(f"Received message on namespace /chat: {message}")
    # logger.debug(f"SEssion: {session.get('room')}")


@socketio.on('connect')
def on_connect():
    logger.debug("Client connected")
    # emit('Server Response: ', {'data': 'Connected!'})
    logger.debug("Data sent")


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
    # TODO: Logic for joining room
    flask_socketio.join_room((room))
    print(f"User {username} has joined room: {room}")
    flask_socketio.send(f"{username} has entered the room.", room=room, broadcast=True)


@socketio.on('chat message')
def on_chat_message(data):
    logger.debug(f"Received a chat message: {data}")
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






# IDK if this blocks, if so run this in a thread
def start_server():
    # api.add_resource(end_game, '/end_game')
    logger.debug("Starting server....")
    app.run()


def end_game():
    logger.debug("Ending Game....")
    return jsonify("Ending Game")


######################################
#####   Flask Server Setup      ######
######################################

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
api = Api(app)
# Create Database Connection
db_conn = DBController("../Databases/players.db", 0)
# Attach our resources for HTTP Requests
# db_conn = DB_CONTROLLER_CONN
api.add_resource(HandlePlayers, '/players', resource_class_kwargs={'db_connection': db_conn})
api.add_resource(HandleIndividualPlayerManagement, '/players/<playername>',
                 resource_class_kwargs={'db_connection': db_conn})
api.add_resource(HandleJoinGame, "/games")
# api.add_resource(HandlePlayerModification,
#                  '/players/<playername>',
#                  '/players/<playername>/<attribute>',
#                  resource_class_kwargs={'db_connection': db_conn})

api.add_resource(HandleHTTPCodes, '/')

if __name__ == "__main__":
    socketio.run(app)
