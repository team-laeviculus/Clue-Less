"""

Keep It Simple Stupid.....
"""

from flask import Flask, request, jsonify, make_response
from collections import OrderedDict
import random
import threading
from http import HTTPStatus
import traceback
from Databases.db_mgmt import CluelessDB
from ClueGameBoard.LocalGameBoard import GameBoard

app = Flask(__name__)
app.config['DEBUG'] = True

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

    def __init__(self, name):
        self.name = name
        self.data = {
            "name": name,
            "token": None,
            "location": None
        }
    def get_player(self):
        return self.data

    def set_token(self, token):
        self.data['token'] = token

    def set_location(self, location):
        self.data['location'] = location

class GameInfo:
    game = {
        "players": OrderedDict(),
        "player_count": 0,
        "game_state": str(GameState.CURRENT_STATE)
    }

    current_players_turn = 0 # Player dict
    players_turn_name = None

class ClueLessCommon:
    """
    DB Controller and game board. Initialized once
    """
    db_controller = None
    game_board = None
    CLUELESS_MUTEX = None
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
    def initialize():
        """
        Static method to initialize a game board
        :return:
        """
        # TODO: Change this from static to instance based so we can have multiple games
        if not (ClueLessCommon.db_controller and ClueLessCommon.game_board):
            ClueLessCommon.db_controller = CluelessDB()
            ClueLessCommon.db_controller.create_games_table()
            ClueLessCommon.db_controller.create_player_table()
            ClueLessCommon.game_board = GameBoard.create_game_board(ClueLessCommon.db_controller, print_board=True)
            ClueLessCommon.CLUELESS_MUTEX = threading.Lock()
            print(ClueLessCommon.TOKENS)
            ClueLessCommon.PLAYER_RANDOM_TOKENS = random.sample(ClueLessCommon.TOKENS, len(ClueLessCommon.TOKENS))
            ClueLessCommon.PLAYER_RANDOM_LOCATION = random.sample(ClueLessCommon.ROOMS, len(ClueLessCommon.TOKENS))
            print(ClueLessCommon.PLAYER_RANDOM_TOKENS)


    @staticmethod
    def start_game():
        """
        Database methods for starting a game.
        :return:
        """

        # TODO: Change this from static to instance based so we can support multiple games

        ClueLessCommon.CLUELESS_MUTEX.acquire()
        try:
            ClueLessCommon.db_controller.create_suspect_table()
            ClueLessCommon.db_controller.init_suspects(1)
            ClueLessCommon.db_controller.create_weapon_table()
            ClueLessCommon.db_controller.init_weapons(1)
            ClueLessCommon.db_controller.create_room_table()
            ClueLessCommon.db_controller.init_rooms(1)
            ClueLessCommon.db_controller.create_cards_table()
            ClueLessCommon.db_controller.init_cards(1)
            ClueLessCommon.db_controller.create_notebook_table()

            # initialize case file
            ClueLessCommon.db_controller.create_case_file_table()

            # establish the solution for a game
            solution_s = random.randint(1, 6)
            solution_w = random.randint(7, 12)
            solution_r = random.randint(13, 21)

            ClueLessCommon.db_controller.init_case_file(1, solution_s, solution_w, solution_r)

            ClueLessCommon.db_controller.update_suspects(1, solution_s)
            ClueLessCommon.db_controller.update_weapons(1, solution_w)
            ClueLessCommon.db_controller.update_rooms(1, solution_r)
            ClueLessCommon.db_controller.shuffle_deal_cards(1, GameInfo.game['player_count'], solution_s, solution_w, solution_r)
            ClueLessCommon.db_controller.create_suggest_log_table()  # only do this at the beginning of the game
            ClueLessCommon.db_controller.create_accuse_log_table()
        finally:
            ClueLessCommon.CLUELESS_MUTEX.release()
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


@app.route("/games/game_state", methods=["GET"])
def on_get_game_state():
    return jsonify("NULL")


@app.route("/games/turn", methods=["GET"])
def on_get_turn_request_info():
    """
    Handles GET requests for turn info
    :return:
    """
    # TODO: Update this so we can do 'games/<GAME_ID>/turn' to support multiple games
    # TODO: HTTP response codes
    #print(f"[GET][Turn]: {request.get_json()}")
    if GameState.CURRENT_STATE == GameState.WAITING_FOR_PLAYERS:
        print(f"Waiting for players....")
        return jsonify({
            "turn":{
                "name": "None",
                "status": "Waiting for players"
            }
        })
    elif GameState.CURRENT_STATE == GameState.GAME_RUNNING:
        print("Game Running")
        if GameInfo.players_turn_name is None:
            get_next_turn()
        return jsonify({"turn": GameInfo.players_turn_name[1]})


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
    ClueLessCommon.CLUELESS_MUTEX.acquire()
    resp = None
    try:
        if ClueLessCommon.game_board.check_if_legal_move(
                req['location'],
                req['request']['move_to_location']):
            print("Move is legal")
            ClueLessCommon.db_controller.update_player_location(req['name'], req['request']['move_to_location'])
            # ClueLessCommon.game_board
            resp = jsonify(get_next_turn())
        else:
            resp = make_response("Invalid Location", HTTPStatus.BAD_REQUEST)
    except:
        traceback.print_exc()
    finally:
        ClueLessCommon.CLUELESS_MUTEX.release()
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
        player = content['name']
        print(f"Player joined: {player}")
        res, status = handle_player_join(content)
        return jsonify(res), status



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
        p['token'] = ClueLessCommon.PLAYER_RANDOM_TOKENS.pop()
        p['location'] = ClueLessCommon.PLAYER_RANDOM_LOCATION.pop()
        ClueLessCommon.PLAYER_TOKEN_MAP[p['token']] = p['name']
        ClueLessCommon.db_controller.put_player_in_game(p['name'])
        GameInfo.game['players'][rquest_data['name']] = p
        GameInfo.game['player_count'] += 1
        # Start a game when some number of players have joined
        if GameInfo.game['player_count'] >= 3:
            GameState.CURRENT_STATE = GameState.GAME_RUNNING
            ClueLessCommon.start_game()
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
    ClueLessCommon.CLUELESS_MUTEX.acquire()

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
            ClueLessCommon.db_controller.update_active_turn(this_players_turn[0])
            print("DB stuff done")
        except:
            traceback.print_exc()
        finally:
            ClueLessCommon.CLUELESS_MUTEX.release()

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


"""
Initialize server constants
"""


ClueLessCommon.initialize()
app.run()