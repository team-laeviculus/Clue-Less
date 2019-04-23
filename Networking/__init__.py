
from flask import Flask
from flask_socketio import SocketIO
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging
from Networking.ServerGameSession import GameSessionManager
from Databases.DBController import DBController
server_logger = None
# Create a Global Server Logger
def create_server_logger():
    global server_logger
    if not server_logger:
        server_logger = Logging.create_logger("server", "../Logs")
    return server_logger
# Initialize flask app
app = Flask(__name__)
app.config["DEBUG"] = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

DB_CONTROLLER_CONN = DBController("../Databases/players.db", 0)
GAME_SESSION_MANAGER = GameSessionManager(DB_CONTROLLER_CONN)

socketio = SocketIO(app, manage_session=False)
# session["test_stupid_object"] = "hello world please store"