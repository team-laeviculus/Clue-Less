import flask
from flask import jsonify, request
from flask_restful import Resource, Api

# Ensure you have your virtual environment properly set up and activated
# PyCharm should automatically do this for you
from Databases.DBController import *


class Server(object):

    def __init__(self, db_connection: DBController, port=5000):
        self.port = port
        self.db_connection = db_connection

    # Access to the player database
    # Posts new players to the database, gets lists of all active players
    class HandlePlayers(Resource):

        def __init__(self, **kwargs):
            self.db_connection = kwargs['db_connection']

        def get(self):
            all_players = self.db_connection.get_table_values('players')
            return jsonify(all_players)

        def post(self):
            values = [request.json["name"]]
            return self.db_connection.add_table_value('players', values)

        def delete(self):
            values = [request.json["name"]]
            return self.db_connection.db_controller.remove_table_value('players', values)

    # IDK if this blocks, if so run this in a thread
    def start_server(self):
        app = flask.Flask("Clueless Server")
        app.config["DEBUG"] = True
        api = Api(app)

        api.add_resource(self.HandlePlayers, '/players', resource_class_kwargs={'db_connection': self.db_connection})
        # api.add_resource(end_game, '/end_game')

        app.run()

    def end_game(self):
        return jsonify("Ending Game")


if __name__ == "__main__":
    dbController = DBController('../Networking/players.db', 0)
    server = Server(dbController)
    server.start_server()
    #server.end_game()
