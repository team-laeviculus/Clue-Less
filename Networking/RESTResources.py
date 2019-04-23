from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response, session
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from . import create_server_logger
from http import HTTPStatus
from Networking import app, ServerConfig
from Logs.Logging import create_server_logger


##############################################
######### TCP RESTful code ###################
##############################################

# Used for PUT request validation
parser = reqparse.RequestParser()
parser.add_argument('weapon')
parser.add_argument('location')
parser.add_argument('suspect')
logger = create_server_logger()

mock_games = {
    "game1" : {
        "players": list()
    },
    "game2" : {
        "players": list()
    }
}

def create_user_session(username, **kwargs):
    # session['name'] = username
    # session.modified = True
    pass




@app.route('/games/join/')
def join_game():
    # if ''
    pass



# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):

    def __init__(self, **kwargs):
        self.db_connection = kwargs['db_connection']

    def get(self):
        all_players = self.db_connection.get_table_values('players')
        logger.debug(f"Getting All Players")
        # logger.debug(f"Get SEssion info: {session.items()}")
        return jsonify(all_players)

    # TAP: Not sure how to link this command with a http call
    # def get(self):
    #     player = self.db_connection.get_player_by_name(name)
    #     return jsonify(player)

    def post(self):
        '''
        Creates a player session. Adds them to the database.
        :return:
        '''
        values = request.json
        name = values["name"].split()
        if not name[0] in ServerConfig.GLOBAL_USERNAMES:
            # Create Flask wide session for user
            ServerConfig.GLOBAL_USERNAMES.add(name[0])

            logger.debug(f"Name: {name}")
            # if not name[0] in session:
            #     logger.info("Adding name to session")
            #     # session['name'] = name[0]
            # else:
            #     return f"{name} Already in the table"

            logger.debug(f"Added {values} to table")
            # logger.debug(f"Created session for {name}: {session['name']}")
            return f"Added {values} to table 'players'. Players: {ServerConfig.GLOBAL_USERNAMES}", HTTPStatus.OK
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

class HandleJoinGame(Resource):
    def __init__(self, **kwargs):
        pass

    #TODO use sessions
    def post(self):
        values = request.json
        logger.debug(f"Data recvd JSON: {values}")
        playername = values["playername"]

        print(f"POST playername stuff: {playername}")
        sess = ServerConfig.GAME_SESSION_MANAGER.get_game_sessions()["game_1"]
        print(f"Adding to session: {sess}")

        player_info = sess.add_player(playername)
        # logger.debug(f"Player joined game: {mock_games['game1']['players']}")
        # return f"you joined game1. Current players: {mock_games['game1']['players']}", HTTPStatus.OK
        return {
            "game_joined": "game_1",
            "server_player_info": player_info
        }

    def get(self):
        logger.debug("Get request for /games")
        return jsonify(mock_games)



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

