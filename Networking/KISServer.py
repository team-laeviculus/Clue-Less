"""

Keep It Simple Stupid.....
"""

from flask import Flask, request, jsonify

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
        "players": dict(),
        "player_count": 0,
        "game_state": str(GameState.CURRENT_STATE)
    }

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


            return jsonify("Game is ready to Start!!!!!")
        return jsonify(GameInfo.game)



def handle_player_join(rquest_data):
    #TODO join
    print(f"Handle player joinm: {rquest_data}")
    print(rquest_data['name'])
    GameInfo.game['players'][rquest_data['name']] = Player(rquest_data['name']).get_player()
    GameInfo.game['player_count'] += 1
    if GameInfo.game['player_count'] >= 3:
        GameState.CURRENT_STATE = GameState.GAME_RUNNING
        print("Game Full STARTING!!")
    print(f"New Game info: {GameInfo.game}")
    response_msg = {
                "game_state": GameState.WAITING_FOR_PLAYERS
            }
    return response_msg







app.run()