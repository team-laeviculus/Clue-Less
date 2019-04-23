
from flask import Flask
from flask_socketio import SocketIO
import os
import sys
import datetime
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
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
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
# # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config.from_object(__name__)
# # app.permanent_session_lifetime = datetime.timedelta(days=365)
# app.secret_key = "super_secret_key" # Required for session objects
# app.permanent_session_lifetime = True

# db = SQLAlchemy(app)
# session = Session(app)
# session.permanent = True
# session.init_app(app)
# session.app.session_interface.db.create_all()
socketio = SocketIO(app, manage_session=False)
# session["test_stupid_object"] = "hello world please store"