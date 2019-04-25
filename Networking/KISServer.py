"""

Keep It Simple Stupid.....
"""

from flask import Flask, request, jsonify
from collections import OrderedDict
app = Flask(__name__)
app.config['DEBUG'] = True

class GameState:
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS",
    GAME_RUNNING = "GAME_RUNNING",
    GAME_VER = "GAME_OVER"

    CURRENT_STATE = WAITING_FOR_PLAYERS

class Player:

    def __init__(self, name):
        self.name = name
        self.data = {
            "name": name,
            "token": None,
            "location": None
        }
    def get_player(self):
        return  self.data

class GameInfo:
    game = {
        "players": OrderedDict(),
        "player_count": 0,
        "game_state": str(GameState.CURRENT_STATE)
    }

    current_players_turn = 0 # Player dict
    players_turn_name = None

@app.route("/games",methods=["GET","POST","PUT"])
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
    print(f"Handle player joinm: {rquest_data}")
    print(rquest_data['name'])
    GameInfo.game['players'][rquest_data['name']] = Player(rquest_data['name']).get_player()
    GameInfo.game['player_count'] += 1
    if GameInfo.game['player_count'] >= 2:
        GameState.CURRENT_STATE = GameState.GAME_RUNNING
        print("Game Full STARTING!!")
        get_next_turn()
    print(f"New Game info: {GameInfo.game}")
    response_msg = {
                "game_state": GameState.WAITING_FOR_PLAYERS
            }
    return response_msg


def handle_game_running_request(request_data):
    print(f"game_running_request: {request_data}")
    player = request_data['name']
    player_token = request_data['token']
    if GameInfo.players_turn_name == player:
        turn_info = request_data['request']
        # TODO: Update Game Board

        return {"turn": GameInfo.players_turn_name[1]}

    return {"turn": GameInfo.players_turn_name[1]}

def get_next_turn():
    """
    Rotates around by player count in the game to determine the turn.

    :return: the self.player[<playername>] object of player whose turn it is
    """
    print("get_next_turn")
    if GameState.CURRENT_STATE == GameState.GAME_RUNNING:
        this_players_turn = list(GameInfo.game['players'].items())[GameInfo.current_players_turn]
        # this_players_turn[1]["my_turn"] = True
        print(f"New Player Turn: {this_players_turn}")
        GameInfo.current_players_turn = (GameInfo.current_players_turn + 1) % GameInfo.game['player_count']
        GameInfo.players_turn_name = this_players_turn
        # TODO: Notify player its their turn
        print(f"Player: {this_players_turn} next")

        return this_players_turn
    # log.info("Game state is not ready to return a players turn")
    return False





app.run()