"""

Keep It Simple Stupid.....
"""

from flask import Flask, request, jsonify, make_response
from collections import OrderedDict, defaultdict
import random
import threading
from http import HTTPStatus
import traceback
from Databases.db_mgmt import CluelessDB
from ClueGameBoard.LocalGameBoard import GameBoard
from Networking.ServerData import GameSession, ClueLessCommon, log
from Networking import ServerData as SERV_DAT
import json

app = Flask(__name__)
app.config['DEBUG'] = True



# Games. Tracks all game sessions
GAME_SESSIONS = OrderedDict({
    1: GameSession(1)
})
# Tracks registered users by username and game_id
REGISTERED_PLAYERS = defaultdict()


class GameState:

    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS",
    GAME_RUNNING = "GAME_RUNNING",
    GAME_VER = "GAME_OVER"

    CURRENT_STATE = WAITING_FOR_PLAYERS

def create_game_tokens():
    #TODO: We might need to do more with this
    # Token_Name, Player Associated
    tokens_map = {
        "Prof Plum" : None,
        "Mrs. Peacock" : None,
        "Mr. Green" : None,
        "Mrs. White" : None,
        "Col. Mustard" : None,
        "Miss Scarlet" : None

    }
    return tokens_map


class Player:
    # TODO: Remove Me
    def __init__(self, name):
        self.name = name
        self.data = {
            "name": name,
            "token": None,
            "location": None,
        }

    def get_player(self):
        return self.data

    def set_token(self, token):
        self.data['token'] = token

    def set_location(self, location):
        self.data['location'] = location

class GameInfo:
    initial_state = {
        "players": OrderedDict(),
        "player_count": 0,
        "game_state": str(GameState.CURRENT_STATE)
    }
    game = dict(initial_state)

    current_players_turn = 0 # Player dict
    players_turn_name = None

class OLDClueLessCommon:
    """
    DB Controller and game board. Initialized once
    """
    db_controller = None
    game_board = None
    CLUELESS_MUTEX = threading.Lock()
    PLAYER_RANDOM_TOKENS = None
    PLAYER_RANDOM_LOCATION = None

    TOKENS = [
        "Prof Plum",
         "Mrs. Peacock",
        "Mr. Green",
        "Mrs. White",
        "Col. Mustard",
        "Miss Scarlet"
    ]
    PLAYER_TOKEN_MAP = OrderedDict()

    @staticmethod
    def initialize(reset=False, db=None):
        """
        Static method to initialize a game board
        :return:
        """
        # TODO: Change this from static to instance based so we can have multiple games
        if not (OLDClueLessCommon.db_controller and OLDClueLessCommon.game_board) or reset is True:
            # OLDClueLessCommon.CLUELESS_MUTEX.acquire()
            try:
                OLDClueLessCommon.db_controller = db#CluelessDB()
                # OLDClueLessCommon.db_controller.create_games_table()
                # OLDClueLessCommon.db_controller.create_player_table()
                OLDClueLessCommon.game_board = GameBoard(OLDClueLessCommon.db_controller)  # GameBoard.create_game_board(ClueLessCommon.db_controller, print_board=True)
                # OLDClueLessCommon.CLUELESS_MUTEX = threading.Lock()
                # print(OLDClueLessCommon.TOKENS)
                OLDClueLessCommon.PLAYER_RANDOM_TOKENS = random.sample(OLDClueLessCommon.TOKENS, len(OLDClueLessCommon.TOKENS))
                OLDClueLessCommon.PLAYER_RANDOM_LOCATION = random.sample(OLDClueLessCommon.ROOMS, len(OLDClueLessCommon.TOKENS))
                print(f" Random Tokens: {OLDClueLessCommon.PLAYER_RANDOM_TOKENS}")
            except:
                traceback.print_exc()
            finally:
                pass
                # OLDClueLessCommon.CLUELESS_MUTEX.release()
    @staticmethod
    def start_game():
        """
        Database methods for starting a game.
        :return:
        """

        # TODO: Change this from static to instance based so we can support multiple games
        OLDClueLessCommon.db_controller = GAME_SESSIONS[1].game_board.db_conn

    HALLWAYS = ["study_hall",
                "hall_lounge"
                "library_billard room",
                "billard room_dinning room",
                "conservatory_ballroom",
                "ballroom_kitchen",
                "study_library",
                "hall_billard room",
                "lounge_dining room",
                "library_conservatory",
                "billard room_ballroom",
                "dining room_kitchen",
    ]

    HALLWAYS_MAP = OrderedDict({k: v for k, v in enumerate(HALLWAYS)})

    ROOMS = [
        'Kitchen',
        'Conservatory',
        'Dining Room',
        'Ballroom',
        'Study',
        'Hall',
        'Lounge',
        'Library',
        'Billard Room',
    ]

    ROOM_MAP = OrderedDict({k: v for k, v in enumerate(ROOMS)})


def get_game_by_id(game_id):
    """
    Checks GAME_SESSIONS for game.
    :param game_id: gameID passed by client
    :return: GameSession for game_id or None if it doesnt exist
    """
    sess = None
    try:
        game_id = int(game_id)
        if game_id in GAME_SESSIONS:
            sess = GAME_SESSIONS[game_id]
    except Exception as e:
        log.error(f"Exception on __get_game_by_id: function given {game_id}. Exception - {e}")
        traceback.print_exc()
    finally:
        return sess


@app.route("/games/create_game/<game_id>/", methods=["POST"])
def create_game_test(game_id):
    # TODO: Exception handling
    GAME_SESSIONS[game_id] = GameSession(int(game_id))
    return "Game Session Created", GAME_SESSIONS[game_id]


#######
@app.route("/games/<game_id>/status", methods=["GET"])
def get_status(game_id):
    """
    Returns the status of the games state machine
    :param game_id:
    :return: HTTP response with game status
    """
    #TODO: Update this to return actual status for game
    return game_id, HTTPStatus.OK


@app.route("/games/<game_id>/turn", methods=["GET"])
def get_current_turn_for_game(game_id):
    game = get_game_by_id(game_id)
    if game:
        return jsonify(game.get_current_turn()), HTTPStatus.OK
    return jsonify({
        "error": f"game id {game_id} does not exist"
    }), HTTPStatus.BAD_REQUEST

@app.route("/games/<game_id>/turn", methods=["POST"])
def post_player_turn(game_id):
    game = get_game_by_id(game_id)
    turn_data = request.get_json()
    log.debug(f"post_player_turn - game_{game_id}: {turn_data}")
    current_players_turn = game.get_current_turn(True)
    # TEMP
    return jsonify({
        "game_id": game_id,
        "turn_status": "Success",  # "turn_status": Failure on bad move
        "message": None,
        "data_server_rcvd": turn_data
    }), HTTPStatus.OK



@app.route("/games/<game_id>/game_state", methods=["GET"])
def on_get_game_state(game_id):
    print(f"getting game state for game {game_id}")
    game_id = int(game_id)
    if game_id in GAME_SESSIONS:
        state = GAME_SESSIONS[int(game_id)].get_game_state_json()
        return jsonify(state), HTTPStatus.OK
    else:
        print(f"Couldnt find anything for game {game_id}")
    return jsonify("NULL")


@app.route("/games/<game_id>/<player_name>/cards", methods=["GET"])
def get_cards_for_player(game_id, player_name):
    game = get_game_by_id(game_id)
    print(f"player_name: {player_name}")
    print(f"registered players: {REGISTERED_PLAYERS}")
    print(f"Game: {game}")
    if game and player_name in REGISTERED_PLAYERS:
        print(f"Game State: {game.get_state()}")
        if game.get_state() == SERV_DAT.GameState.GAME_RUNNING:
            return jsonify({
                'name': player_name,
                'cards': game.get_player_cards(player_name)
            }), HTTPStatus.OK
        else:
            return jsonify({
                "error": "game state is set as not running",
                "state": game.get_state()
            }), HTTPStatus.BAD_REQUEST
    return jsonify({
        "error": f"Game {game_id} does not exist or player {player_name} is not in game",
        "game_id": f"{game_id}",
        "name": player_name
    }), HTTPStatus.BAD_REQUEST


@app.route("/games", methods=["GET", "POST", "PUT"])
def get_game_info():
    """
    Handles HTTP requests for games on the server
    :return:
    """

    # TODO: HTTP status codes on responses
    content = request.get_json()
    #print(f"[{request.method}]:New Request:  {content}")
    if request.method == "POST":
        player = content['name']
        print(f"Player joined: {player}")
        res = handle_player_join(content)
        print(f"CREATE PROFILE: {res}")
        return jsonify(res)

    elif request.method == "PUT":
        print(f"Game Update: {request}")
        return jsonify("Put")
    else:
        print("Return game state")
        if GameState.CURRENT_STATE == GameState.WAITING_FOR_PLAYERS:
            #print("Returning waiting for players...")
            return jsonify(f"waiting for players....current player count: {GameInfo.game['player_count']}, players: {GameInfo.game['players'].keys()}")
        elif GameState.CURRENT_STATE == GameState.GAME_RUNNING:
            # Game State stuff
            res = handle_game_running_request(content)
            return jsonify(res)


            #return jsonify("Game is ready to Start!!!!!")
        return jsonify(GameInfo.game)


# @app.route("/games/turn", methods=["GET"])
# def on_get_turn_request_info():
#     """
#     Handles GET requests for turn info
#     :return:
#     """
#     # TODO: Update this so we can do 'games/<GAME_ID>/turn' to support multiple games
#     # TODO: HTTP response codes
#     #print(f"[GET][Turn]: {request.get_json()}")
#     if GameState.CURRENT_STATE == GameState.WAITING_FOR_PLAYERS:
#         print(f"Waiting for players....")
#         return jsonify({
#             "turn": {
#                 "name": "None",
#                 "status": "Waiting for players"
#             }
#         })
#     elif GameState.CURRENT_STATE == GameState.GAME_RUNNING:
#         print("Game Running")
#         if GameInfo.players_turn_name is None:
#             get_next_turn()
#         return jsonify({"turn": GameInfo.players_turn_name[1]})


@app.route("/games/turn", methods=["POST"])
def on_post_turn_info():
    """
    Handles POST requests for clients updating turn info. Used to notify the server that the player
    has made some action on their turn
    :return:
    """
    # TODO: Update this so we can do 'games/<GAME_ID>/turn' to support multiple games
    # TODO: HTTP Status Codes
    req = request.get_json()
    print(f"[POST][Turn]: {req}")
    OLDClueLessCommon.CLUELESS_MUTEX.acquire()
    resp = None
    try:
        if OLDClueLessCommon.game_board.check_if_legal_move(
                req['location'],
                req['request']['move_to_location']):
            print("Move is legal")
            OLDClueLessCommon.db_controller.update_player_location(req['name'], req['request']['move_to_location'])
            # ClueLessCommon.game_board
            resp = jsonify(get_next_turn())
        else:
            resp = make_response("Invalid Location", HTTPStatus.BAD_REQUEST)
    except:
        traceback.print_exc()
    finally:
        OLDClueLessCommon.CLUELESS_MUTEX.release()
    print(f"Server Response to Turn: {resp}")
    return resp


@app.route("/games/players", methods=["GET", "POST", "DELETE"])
def on_players_request_method():
    """
    Handles players joining the game, requesting status of other players and removing players
    :return:
    """

    # req_data = req.get_json()
    print(f"on_players_request: {request.get_json()}")
    if request.method == "GET":
        # Returns the Players
        print(f"Getting players")
        return jsonify(GameInfo.game['players'])

    if request.method == "POST":
        # Adds a new player
        content = request.get_json()
        print(f"/game/players [POST]: {content}")
        if not content:
            # Used for Unit Testing, because for some reason get_json doesnt work out of the box
            try:
                content = json.loads(request.data)
            except:
                pass
        if content and 'name' in content:
            player = content['name']
            # If username already exists:
            if player in REGISTERED_PLAYERS:
                log.warning(f"Username {player} has already been registered")
                return jsonify({"name": player, "error": "name taken"}), HTTPStatus.BAD_REQUEST

            log.info(f"Player joined: {player}")
            # TODO: Do we automatically want to throw them in a game?
            game_sess = get_game_session()
            REGISTERED_PLAYERS[player] = game_sess
            p_add_r = game_sess.add_player(player)
            # res, status = handle_player_join(content)
            print(f"Add Return: {p_add_r.data}")
            resp = dict(p_add_r.data)
            resp['game_id'] = game_sess.game_id
            return jsonify(resp), HTTPStatus.OK

        return jsonify({"error": "Error! Invalid Player Message."}), HTTPStatus.BAD_REQUEST



def handle_player_join(rquest_data):
    """
    Handles the mechanics of actually putting a player into a game or
    :param rquest_data:
    :return:
    """
    #TODO Name already in use error
    #TODO game full error
    #TODO: 30s wait timer before starting game like before
    print(f"Handle player join: {rquest_data}")
    print(rquest_data['name'])
    response_msg = None
    if GameState.CURRENT_STATE != GameState.GAME_RUNNING:
        # Create a player object based on POST request info. Randomly assign player
        # token name and player starting location
        # TODO: Handle Client Side asking for player to pick token name and starting location
        p = Player(rquest_data['name']).get_player()
        p['token'] = OLDClueLessCommon.PLAYER_RANDOM_TOKENS.pop()
        p['location'] = OLDClueLessCommon.PLAYER_RANDOM_LOCATION.pop()
        OLDClueLessCommon.PLAYER_TOKEN_MAP[p['token']] = p['name']
        OLDClueLessCommon.db_controller.put_player_in_game(p['name'])
        GameInfo.game['players'][rquest_data['name']] = p
        GameInfo.game['player_count'] += 1
        # Start a game when some number of players have joined
        if GameInfo.game['player_count'] >= 3:
            GameState.CURRENT_STATE = GameState.GAME_RUNNING
            OLDClueLessCommon.start_game()
            print("Game Full STARTING!!")
            #GameInfo.players_turn_name = get_next_turn()
            print(f"First Player is: {GameInfo.players_turn_name}")
        print(f"New Game info: {GameInfo.game}")
        response_msg = {
                    "game_state": GameState.CURRENT_STATE,
                    "token": p['token'],
                    "location": p['location'],
                }, HTTPStatus.OK
    else:
        # TODO: Create a new game or handle game being unjoinable
        # Current game is full or already active...returning Error
        response_msg = "ERROR! Game is full or active", HTTPStatus.BAD_REQUEST

    return response_msg


def handle_game_running_request(request_data):
    print(f"game_running_request: {request_data}")
    player = request_data['name']
    player_token = request_data['token']
    if GameInfo.players_turn_name is None:
        print("players turn is none")
        GameInfo.players_turn_name = list(GameInfo.game['players'].items())[0]
        print(f"There was no player set for first turn. Now it is: {GameInfo.players_turn_name}")

    print(f"player whose turn it is: {GameInfo.players_turn_name}")
    return {"turn": GameInfo.players_turn_name[1]}


def get_turn(request_data):
    print(f"[GET][Turn]: {request_data}")
    player = request_data['name']

    player_token = request_data['token']

    if GameInfo.players_turn_name is None:
        print("players turn is none")
        GameInfo.players_turn_name = list(GameInfo.game['players'].items())[0]
        print(f"There was no player set for first turn. Now it is: {GameInfo.players_turn_name}")
    # if GameInfo.players_turn_name == player:
    #     turn_info = request_data['request']
    #     # TODO: Update Game Board
    #     print(f"Turn Info: {turn_info}")

    return {"turn": GameInfo.players_turn_name[1]}

def get_next_turn():
    """
    Rotates around by player count in the game to determine the turn.

    :return: the self.player[<playername>] object of player whose turn it is
    """
    OLDClueLessCommon.CLUELESS_MUTEX.acquire()

    print("get_next_turn")
    if GameState.CURRENT_STATE == GameState.GAME_RUNNING:
        if GameInfo.players_turn_name is None:
            # Assign the first player whose turn it will be
            # TODO: Switch from first player who joined to a random person in the game list
            print("players turn is none")
            GameInfo.players_turn_name = list(GameInfo.game['players'].items())[0]
            print(f"There was no player set for first turn. Now it is: {GameInfo.players_turn_name}")
        this_players_turn = list(GameInfo.game['players'].items())[GameInfo.current_players_turn]
        try:
            # this_players_turn[1]["my_turn"] = True
            print(f"New Player Turn: {this_players_turn}")
            GameInfo.current_players_turn = (GameInfo.current_players_turn + 1) % GameInfo.game['player_count']
            GameInfo.players_turn_name = this_players_turn
            print(f"Player: {this_players_turn} next")

            # TODO: Notify player its their turn
            OLDClueLessCommon.db_controller.update_active_turn(this_players_turn[0])
            print("DB stuff done")
        except:
            traceback.print_exc()
        finally:
            OLDClueLessCommon.CLUELESS_MUTEX.release()

        return this_players_turn
    elif GameState.CURRENT_STATE == GameState.WAITING_FOR_PLAYERS:
        print("Waiting for players")
        return {
            "turn": "None",
            "status": "Waiting for players"
        }
    else:
        print(f"ERROR: Undefined state")
    # log.info("Game state is not ready to return a players turn")
    # TODO, return something other then False?
    return False


def get_game_session():
    """
    Gets a game session object to add players to, or creates a new one if full
    :return: GameSession Reference
    """
    game_id = next(reversed(GAME_SESSIONS))
    game_sess = GAME_SESSIONS[game_id]
    # Get the last item added to sessions list, if joinable that session is returned,
    # otherwise a new one is created
    if game_sess.game_state.CURRENT_STATE == SERV_DAT.GameState.WAITING_FOR_PLAYERS \
            and game_sess.player_count < ClueLessCommon.MAX_NUMBER_OF_PLAYERS:
        print(f"get_game_session: Returned game session {game_sess.game_id}")
        return game_sess
    new_id = game_id + 1
    GAME_SESSIONS[new_id] = GameSession(new_id)
    print(f"Created a new game session with id: {new_id}")
    return GAME_SESSIONS[new_id]
"""
Initialize server constants
"""
def start_server():
    print("Starting Server......")
    OLDClueLessCommon.initialize()
    app.run()

if __name__ == "__main__":
    start_server()