
from flask import Flask
from flask_socketio import SocketIO
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging
from Networking.ServerGameSession import GameSessionManager, GameSession
# from Networking.RESTResources import HandlePlayerModification
# from Databases.DBController import DBController
from Databases.db_mgmt import CluelessDB

CLIENT_SESSION_INFO = None # Idk where to put this. Its for the client to store local info about what the server knows.

class ServerConfig:
    # Should only have one instance created server Side
    DB_CONTROLLER_CONN = None
    GAME_SESSION_MANAGER = None
    GLOBAL_USERNAMES = None
    @staticmethod
    def create_server_config():
        if not (ServerConfig.DB_CONTROLLER_CONN and \
                ServerConfig.GLOBAL_USERNAMES and \
                ServerConfig.GAME_SESSION_MANAGER):
            ServerConfig.DB_CONTROLLER_CONN = CluelessDB()
            ServerConfig.GLOBAL_USERNAMES = set()
            ServerConfig.GAME_SESSION_MANAGER = GameSessionManager(ServerConfig.DB_CONTROLLER_CONN)
# Initialize flask app
app = Flask(__name__)
app.config["DEBUG"] = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

# DB_CONTROLLER_CONN = DBController("../Databases/players.db", 0)


socketio = SocketIO(app, manage_session=False)
GameSession.set_socketio_ctx(socketio)
# session["test_stupid_object"] = "hello world please store"