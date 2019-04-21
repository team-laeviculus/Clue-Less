
from flask import Flask
from flask_socketio import SocketIO
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Logs import Logging

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
app.secret_key = "super_secret_key" # Required for session objects
socketio = SocketIO(app)