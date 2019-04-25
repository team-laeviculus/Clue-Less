"""

Keep It Simple Stupid.....
"""

from flask import Flask, request, jsonify
from collections import OrderedDict
import random
import threading
import traceback
from Databases.db_mgmt import CluelessDB
from ClueGameBoard.GameBoard_DatabaseCoordinates import GameBoard

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
        if not (ClueLessCommon.db_controller and ClueLessCommon.game_board):
            ClueLessCommon.db_controller = CluelessDB()
            ClueLessCommon.db_controller.create_games_table()
            ClueLessCommon.db_controller.create_player_table()
            ClueLessCommon.game_board = GameBoard.create_game_board(ClueLessCommon.db_controller, print_board=True)
            ClueLessCommon.CLUELESS_MUTEX = threading.Lock()
            print(ClueLessCommon.TOKENS)
            ClueLessCommon.PLAYER_RANDOM_TOKENS = random.sample(ClueLessCommon.TOKENS, len(ClueLessCommon.TOKENS))
            print(ClueLessCommon.PLAYER_RANDOM_TOKENS)


    @staticmethod
    def start_game():

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



def handle_player_join(rquest_data):
    #TODO join
    #TODO Name already in use error
    #TODO game full error
    print(f"Handle player joinm: {rquest_data}")
    print(rquest_data['name'])
    p = Player(rquest_data['name']).get_player()
    p['token'] = ClueLessCommon.PLAYER_RANDOM_TOKENS.pop()
    ClueLessCommon.PLAYER_TOKEN_MAP[p['token']] = p['name']
    ClueLessCommon.db_controller.put_player_in_game(p['name'])
    GameInfo.game['players'][rquest_data['name']] = p
    GameInfo.game['player_count'] += 1
    if GameInfo.game['player_count'] >= 2:
        GameState.CURRENT_STATE = GameState.GAME_RUNNING
        ClueLessCommon.start_game()
        print("Game Full STARTING!!")
        #GameInfo.players_turn_name = get_next_turn()
        print(f"First Player is: {GameInfo.players_turn_name}")
    print(f"New Game info: {GameInfo.game}")
    response_msg = {
                "game_state": GameState.WAITING_FOR_PLAYERS,
                "token": p['token'],
                "location": p['location']
            }
    return response_msg


def handle_game_running_request(request_data):
    print(f"game_running_request: {request_data}")
    player = request_data['name']
    player_token = request_data['token']
    if GameInfo.players_turn_name is None:
        print("players turn is none")
        GameInfo.players_turn_name = list(GameInfo.game['players'].items())[0]
        print(f"There was no player set for first turn. Now it is: {GameInfo.players_turn_name}")
    if GameInfo.players_turn_name == player:
        turn_info = request_data['request']
        # TODO: Update Game Board
        print(f"Turn Info: {turn_info}")

        return {"turn": GameInfo.players_turn_name[1]}
    print(f"player whose turn it is: {GameInfo.players_turn_name}")
    return {"turn": GameInfo.players_turn_name[1]}

def get_next_turn():
    """
    Rotates around by player count in the game to determine the turn.

    :return: the self.player[<playername>] object of player whose turn it is
    """
    ClueLessCommon.CLUELESS_MUTEX.acquire()

    print("get_next_turn")
    if GameState.CURRENT_STATE == GameState.GAME_RUNNING:
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
    # log.info("Game state is not ready to return a players turn")
    return False


"""
Initialize server constants
"""


ClueLessCommon.initialize()
app.run()