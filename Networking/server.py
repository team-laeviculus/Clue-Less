import flask
from flask import jsonify, request
from flask_restful import Resource, Api

# This requires python path to be set correctly, i.e.
# export PYTHONPATH=$PYTHONPATH:/path/to/MainFolder
# TODO: What's a better way to do this?
from Databases.DBController import *

# TODO: This shouldn't be declared in global scope, but I'm not sure
# where the best place for this is
db_controller = DBController('./Databases/players.db', 0)

# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):

    def get(self):
        all_players = db_controller.get_table_values('players')
        return jsonify(all_players)

    def post(self):
        values = [request.json["name"]]
        return db_controller.add_table_value('players', values)

    def delete(self):
        values = [request.json["name"]]
        return db_controller.remove_table_value('players', values)

def end_game():
    return(jsonify("Ending Game"))

def go():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    api = Api(app)

    api.add_resource(HandlePlayers, '/players')
    #api.add_resource(end_game, '/end_game')


    app.run()

if __name__ == "__main__":
    go()
