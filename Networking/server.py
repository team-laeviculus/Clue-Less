import flask
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
# Ensure you have your virtual environment properly set up and activated
# PyCharm should automatically do this for you
from Databases.DBController import *

# Used for PUT request validation
parser = reqparse.RequestParser()
parser.add_argument('weapon')
parser.add_argument('location')
parser.add_argument('suspect')

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
        print(f"Player Attribute Query. name: {playername}, attribute: {attribute}")
        if attribute in player_data:
            print("Attribute Exists!")
            return jsonify({attribute: player_data[attribute]}), HTTPStatus.OK
        print("Attribute Does Not Exist!!")
        return '', HTTPStatus.BAD_REQUEST



class HandleIndividualPlayerManagement(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self, playername):
        player = self.db_connection.get_player_by_name(playername)
        print(f"GET {playername}: {player}")
        return jsonify(player)

    def delete(self, playername):
        print(f"Attempting to delete {playername}")
        res = self.db_connection.delete_player_by_name(playername)
        if res:
            return '', HTTPStatus.OK
        return '', HTTPStatus.BAD_REQUEST

    def put(self, playername):
        print(f"PUT serverside: {playername}")
        args = parser.parse_args()
        print(f"PUT Args: {args}")
        ret_code = self.db_connection.update_player_by_name(playername,
                                                            weapon=args['weapon'],
                                                            suspect=args['suspect'],
                                                            space=args['location']
                                                            )
        if ret_code == True:
            return f'Player {playername} Updated', HTTPStatus.OK
        return f'Player {playername} Does Not Exist', HTTPStatus.BAD_REQUEST



# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self):
        all_players = self.db_connection.get_table_values('players')
        return jsonify(all_players)

    # TAP: Not sure how to link this command with a http call
    # def get(self):
    #     player = self.db_connection.get_player_by_name(name)
    #     return jsonify(player)

    def post(self):
        values = request.json
        print(f"Insert player server: {values}")
        return self.db_connection.add_table_value('players', values)

    def delete(self):
        # TODO: Validate Player exists in table
        values = [request.json["name"]]
        print(f"Deleting player: {values}")
        return self.db_connection.remove_table_value('players', values), HTTPStatus.OK


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)
db_conn = DBController("../Databases/players.db", 0)
api.add_resource(HandlePlayers, '/players', resource_class_kwargs={'db_connection': db_conn})
api.add_resource(HandleIndividualPlayerManagement, '/players/<playername>', resource_class_kwargs={'db_connection': db_conn})
# api.add_resource(HandlePlayerModification,
#                  '/players/<playername>',
#                  '/players/<playername>/<attribute>',
#                  resource_class_kwargs={'db_connection': db_conn})

api.add_resource(HandleHTTPCodes, '/')


def start_server():
    app.run()


if __name__ == "__main__":
    start_server()
