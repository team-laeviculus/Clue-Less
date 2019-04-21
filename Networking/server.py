import flask
from flask import jsonify, request, make_response, Flask, render_template, session
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import flask_socketio
from flask_socketio import SocketIO, emit
import flask_socketio

from http import HTTPStatus
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging
# Ensure you have your virtual environment properly set up and activated
# PyCharm should automatically do this for you
from Databases.DBController import *

# Used for PUT request validation
parser = reqparse.RequestParser()
parser.add_argument('weapon')
parser.add_argument('location')
parser.add_argument('suspect')

# Create a Global Server Logger
logger = Logging.create_logger("server")

# Initialize flask app
app = Flask(__name__)
app.config["DEBUG"] = True
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




##############################################
######### TCP RESTful code ###################
##############################################
class HandlePlayerModification(Resource):
    """
    Handler for getting player attributes.
    Query format: /players/<playername>/<attribute>
    """

    # TODO: Update Sql queries for this
    def __init(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self, playername, attribute):
        player_data = self.db_connection.get_player_by_name(playername)
        logger.debug(f"Player Attribute Query. name: {playername}, attribute: {attribute}")
        if attribute in player_data:
            return jsonify({attribute: player_data[attribute]}), HTTPStatus.OK
        logger.warning(f"Attribute {attribute} Does Not Exist!!")
        return f'"Attribute {attribute} Does Not Exist!', HTTPStatus.BAD_REQUEST



class HandleIndividualPlayerManagement(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self, playername):
        player = self.db_connection.get_player_by_name(playername)
        logger.debug(f"GET {playername}: {player}")
        return jsonify(player)

    def delete(self, playername):
        logger.debug(f"Attempting to delete {playername}")
        res = self.db_connection.delete_player_by_name(playername)
        if res:
            logger.debug(f"Player {playername} Deleted!")
            return f'Player {playername} has left the game', HTTPStatus.OK
        logger.warning(f"Cant delete {playername}, they do not exist in players table!")
        return f'Error! Cannot delete player {playername} since they arent in the game.', HTTPStatus.BAD_REQUEST

    def put(self, playername):
        args = parser.parse_args()
        logger.debug(f"PUT Request: Player - {playername}, Args -{args}")
        ret_code = self.db_connection.update_player_by_name(playername,
                                                            weapon=args['weapon'],
                                                            suspect=args['suspect'],
                                                            space=args['location']
                                                            )
        if ret_code:
            logger.debug(f"Player {playername} updated.")
            return f'Player {playername} Updated', HTTPStatus.OK
        logger.warning(f"Player {playername} Does Not Exist!")
        return f'Player {playername} Does Not Exist', HTTPStatus.BAD_REQUEST



# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self):
        all_players = self.db_connection.get_table_values('players')
        logger.debug(f"Getting All Players")
        return jsonify(all_players)

    # TAP: Not sure how to link this command with a http call
    # def get(self):
    #     player = self.db_connection.get_player_by_name(name)
    #     return jsonify(player)

    def post(self):
        values = request.json
        if self.db_connection.add_table_value('players', values):
            logger.debug(f"Added {values} to table")
            return f"Added {values} to table 'players'", HTTPStatus.OK
        logger.warning(f"Error! Could not add {values} to table!")
        return f'Error! Could not add {values} to table', HTTPStatus.BAD_REQUEST

    def delete(self):
        # TODO: Validate Player exists in table
        values = [request.json["name"]]
        if self.db_connection.remove_table_value('players', values):
            logger.debug(f"Removed Table Value {values} from table 'players'.")
            return f"Removed Table Value {values} from table 'players'.", HTTPStatus.OK
        logger.warning(f"Error! Could not remove {values} from table 'players'")
        return f"Error! Could not remove {values} from table 'players'", HTTPStatus.BAD_REQUEST


class HandleHTTPCodes(Resource):

    def get(self):
        logger.debug("Dummy GET request")
        return make_response(jsonify({"ROOT": "Test"}), HTTPStatus.OK)


# IDK if this blocks, if so run this in a thread
def start_server():

    # api.add_resource(end_game, '/end_game')
    logger.debug("Starting server....")
    app.run()


def end_game():
    logger.debug("Ending Game....")
    return jsonify("Ending Game")



# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
api = Api(app)
# Create Database Connection
db_conn = DBController("../Databases/players.db", 0)
# Attach our resources for HTTP Requests
api.add_resource(HandlePlayers, '/players', resource_class_kwargs={'db_connection': db_conn})
api.add_resource(HandleIndividualPlayerManagement, '/players/<playername>', resource_class_kwargs={'db_connection': db_conn})
# api.add_resource(HandlePlayerModification,
#                  '/players/<playername>',
#                  '/players/<playername>/<attribute>',
#                  resource_class_kwargs={'db_connection': db_conn})

api.add_resource(HandleHTTPCodes, '/')



if __name__ == "__main__":
    socketio.run(app)
