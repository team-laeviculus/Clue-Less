
from flask import Flask
from flask_socketio import SocketIO
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging
from Networking.ServerGameSession import GameSessionManager
# from Networking.RESTResources import HandlePlayerModification
# from Databases.DBController import DBController
from Databases.db_mgmt import CluelessDB

CLIENT_SESSION_INFO = None # Idk where to put this. Its for the client to store local info about what the server knows.

class ServerConfig:
    DB_CONTROLLER_CONN = CluelessDB()
    GAME_SESSION_MANAGER = GameSessionManager(DB_CONTROLLER_CONN)
    GLOBAL_USERNAMES = set()
# Initialize flask app
app = Flask(__name__)
app.config["DEBUG"] = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

# DB_CONTROLLER_CONN = DBController("../Databases/players.db", 0)


socketio = SocketIO(app, manage_session=False)
# session["test_stupid_object"] = "hello world please store"