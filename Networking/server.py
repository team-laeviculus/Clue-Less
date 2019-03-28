import flask
from flask import jsonify, request, make_response
from flask_restful import Resource, Api
from http import HTTPStatus
# Ensure you have your virtual environment properly set up and activated
# PyCharm should automatically do this for you
from Databases.DBController import *

# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self):
        all_players = self.db_connection.get_table_values('players')
        return jsonify(all_players)

    def post(self):
        values = request.json
        return self.db_connection.add_table_value('players', values)

    def delete(self):
        values = [request.json["name"]]
        print(f"Deleting player: {values}")
        return self.db_connection.remove_table_value('players', values)


class HandleHTTPCodes(Resource):

    def get(self):
        return make_response(jsonify({"ROOT": "Test"}), HTTPStatus.OK)


# IDK if this blocks, if so run this in a thread
def start_server():

    # api.add_resource(end_game, '/end_game')

    app.run()


def end_game():
    return jsonify("Ending Game")



app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
api.add_resource(HandlePlayers, '/players', resource_class_kwargs={'db_connection': DBController("../Databases/players.db", 0)})
api.add_resource(HandleHTTPCodes, '/')


def start_server():
    app.run()


if __name__ == "__main__":
    start_server()
