from collections import OrderedDict
from enum import Enum
import threading
import time
import random
import os
import sys
from flask_socketio import emit
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ClueGameBoard.GameBoard_DatabaseCoordinates import GameBoard
from Logs.Logging import create_server_logger


log = create_server_logger()

class GameState(Enum):
    """
    Game State Enum
    """
    READY = "ready",
    WAITING = "waiting",
    TIMEOUT_STARTED = "timeout_started",
    STOPPED = "stopped",
    ACTIVE = "active_game",
    AWAITING_PLAYERS = "awaiting_players"

# class Player:
#     """
#     Server Side Representation of Player
#     """
#     def __init__(self, username):
#         self.username = username
#         self.data = dict()
#
#     def


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

class GameSession:

    """
    Server Side Game Session for handling the mechanics of a Clue Game Session
    Coordinates between players. Should be state based.
    """
    MAX_PLAYERS = 6
    MIN_PLAYER_COUNT = 3 # Min number of players to start a game
    TIMEOUT_TIME = 2 # 30 seconds

    def __init__(self, game_name, db_controller):
        self.game_name = game_name
        self.players = OrderedDict() # Preserves order of items added
        self.player_turn = 0
        self.player_count = 0
        self.db_controller = db_controller
        self.db_controller.create_games_table()

        self.game_tokens = create_game_tokens()

        self.game_board = GameBoard.create_game_board(db_controller)
        self.db_controller.create_player_table()
        self.game_state = GameState.STOPPED
        self.db_mutex = threading.Lock()

        self.timeout_timer_thread = threading.Timer(GameSession.TIMEOUT_TIME, self.__start_game)

        log.debug(f"Game Session Instance Created")


    def add_player(self, username):
        """
        add_player: Adds a player to this GameSession, if 3 or more players,
        timeout timer is started, once it expires game is started.

        :param name: player name
        :return:
        """
        #TODO: DB Controller Stuff


        if self.player_count < GameSession.MAX_PLAYERS:
            log.info(f"Attempting to Add player {username}")
            log.info(f"Game [{self.game_name}] now has {self.player_count} players.")
            # TODO: Database adds player to game
            self.db_controller.put_player_in_game(username)

            # Add the player
            self.player_count += 1
            # Add player as dictionary item in local datastruct
            player_info = self.__add_player(username)

            if self.game_state == GameState.STOPPED:
                log.info("Updating Game state")
                self.game_state = GameState.READY

            if self.player_count >= GameSession.MIN_PLAYER_COUNT:
                log.info("Starting timeout timer")
                # Start Timer to Launch the Game. If new player joins,
                #TODO: Watch out for any race connditions
                if self.game_state == GameState.TIMEOUT_STARTED:
                    # Timeout Timer already started. Cancel it and create a new one
                    log.info("Timeout Timer already started, new player joined, creating a new timeout timer")
                    self.timeout_timer_thread.cancel()
                    self.timeout_timer_thread = threading.Timer(GameSession.TIMEOUT_TIME, self.__start_game)
                    self.timeout_timer_thread.start()
                    # Callback
                else:
                    # 3rd player joined, start first timeout timer
                    log.info("Starting timeout timer for first time")
                    self.timeout_timer_thread.start()
                    self.game_state = GameState.TIMEOUT_STARTED
            return player_info


    def __add_player(self, username):
        """
        Private helper function for creating a new player entry in the players dict
        :param username: the username the player chose
        :return: Dict item
        """
        self.players[username] = {
            "turn" : self.player_count,
            "my_turn" : False,
            "is_active" : True, # hasnt lost
            "winner" : False,
            "token" : None, # Chosen Game Token
            "location" : None # GameBoard.Player item
        }

        log.info(f"New player item created: {self.players[username]}")
        return self.players[username]

    def is_full(self):
        """
        Basically a quick check to see if this session is joinable
        :return:
        """
        if self.player_count == 6 or self.game_state == GameState.ACTIVE:
            return True
        return False

    def get_available_tokens(self):
        """
        For server and client to interact and choose tokens
        :return: (integer, token_name) dictionary for clients to select token they want
        """
        #TODO: Fix enumerate issue where we get 0,1,4,5 returned instead of 0,1,2,3,4
        return dict({num: tok for num, tok in enumerate(self.game_tokens) if self.game_tokens[tok] is None})

    def set_players_token(self, playername, token_choice):
        """
        Sets a token as chosen by a player
        :param playername: The player who is chosing the token
        :param token_choice: the game token (i.e. 'miss peach')
        :return: True if success, False if taken (hopefully not an issue)
        """
        if token_choice in self.game_tokens and playername in self.players:
            log.info(f"Player {playername} chose token {token_choice}")
            # This is a bad way of doing all this stuff but w/e
            #TODO: Probably check both if none before we overwrite
            self.game_tokens[token_choice] = playername
            self.players[playername]['tokens'] = token_choice
            return True
        return False

    #TODO integrate game logic
    def __start_game(self):
        print("Starting Game! No new players can join")
        self.game_state = GameState.READY

        self.db_mutex.acquire() # LOCK the thread
        try:
            self.db_controller.create_suspect_table()
            self.db_controller.init_suspects(1)
            self.db_controller.create_weapon_table()
            self.db_controller.init_weapons(1)
            self.db_controller.create_room_table()
            self.db_controller.init_rooms(1)
            self.db_controller.create_cards_table()
            self.db_controller.init_cards(1)
            self.db_controller.create_notebook_table()

            # initialize case file
            self.db_controller.create_case_file_table()

            # establish the solution for a game
            solution_s = random.randint(1, 6)
            solution_w = random.randint(7, 12)
            solution_r = random.randint(13, 21)

            self.db_controller.init_case_file(1, solution_s, solution_w, solution_r)

            self.db_controller.update_suspects(1, solution_s)
            self.db_controller.update_weapons(1, solution_w)
            self.db_controller.update_rooms(1, solution_r)
            self.db_controller.shuffle_deal_cards(1, self.player_count, solution_s, solution_w, solution_r)

            self.db_controller.create_suggest_log_table()  # only do this at the beginning of the game
            self.db_controller.create_accuse_log_table()
        # Unlock thread
        finally:
            self.db_mutex.release()

        #TODO: Ask each player what token they want by order they joined
        #TODO: Store choice in DB
        #TODO: Once each player has a token,

    def get_next_turn(self):
        """
        Rotates around by player count in the game to determine the turn.

        :return: the self.player[<playername>] object of player whose turn it is
        """
        if self.game_state == GameState.READY or self.game_state == GameState.ACTIVE:
            #TODO:Bug, everyone gets set as my_turn being true. so dont use it
            this_players_turn = list(self.players.items())[self.player_turn]
            this_players_turn[1]["my_turn"] = True
            log.info(f"New Player Turn: {this_players_turn}")
            self.player_turn = (self.player_turn + 1) % self.player_count
            return this_players_turn
        log.info("Game state is not ready to return a players turn")
        return False


    # TRANSMIT FUNCTIONS

    def notify_all_players(self, event, data, game="game_1"):
        """
        Send a message to everyone in one game
        :param event: name of event for callback
        :param data: a dict, should be standard
        :param game: game_id
        :return: none
        """
        log.debug(f"Notifying all players in game {self.game_name} with event {event} and data {data}")
        emit(event=event, data=data, namespace="/games", room=game, broadcast=True)

    def notify_one_player(self, name, event, data, game="game_1"):
        """
        Send message to one player
        :param name: player name
        :param event: event name
        :param data: dict, should be standard
        :param game: game_id
        :return:
        """
        data['name'] = name
        emit(event=event, data=data, namespace="/games", room=game, broadcast=True)




    def turn_mechanics(self):
        while(True):
            log.info("Getting next turn")
            players_turn = self.get_next_turn()
            players_name = players_turn[0]
            # notify player of turn, get his movement
            self.notify_one_player(players_name, data={})
            players_movement = 'Library' #change this to actual player's movement
            self.game_board.move_player(players_name, players_movement, True)
            #For now, assume move is valid( no error handling )
            time.sleep(2)
            # ask player if he wants to make a suggestion
            # From player, get g_id, player_num, player_cnt, suggest_suspect, suggest_weapon, suggest_room
            # use hard-coded values for now
            player_cnt = self.players[players_name].get('turn')
            print("printing player_cnt")
            print(player_cnt)
            self.db_controller.make_suggestion(1, self.player_count, player_cnt, "Miss Scarlet", "Lead Pipe", "Study")

class GameSessionManager:
    """
    Manages all the games on the server. Each player will locally store the game name they are a member of
    to keep things simple. This is a singleton.
    """
    __instance = None
    @staticmethod
    def getInstance():
        if GameSessionManager.__instance == None:
            GameSessionManager()
        return GameSessionManager.__instance

    def __init__(self, db_controller, number_games=4):
        if not GameSessionManager.__instance is None:
            raise Exception("GameSessionManager object has already been created. Use getInsance")
        else:
            self.db_controller = db_controller
            print(f"DB Controller: {self.db_controller}")

            self.game_sessions = self.__create_game_sessions(number_games)
            GameSessionManager.__instance = self

    def __create_game_sessions(self, num_games):
        res = {}
        for i in range(num_games):
            name = f"game_{i}" #Unique Game Identifier
            res[name] = GameSession(name, self.db_controller)
        return res

    def get_game_sessions(self):
        return self.game_sessions




if __name__ == "__main__":
    print("Starting test")
    from Databases.db_mgmt import  CluelessDB
    db_conn = CluelessDB()
    print("DB controller created")
    sess = GameSession("testgame", db_controller=db_conn)


    # Test adding players to the game
    print("Session spawned")
    sess.add_player("player1")
    sess.add_player("player2")
    sess.add_player("player3")

    # Test game start timeout timer
    print("Test adding player after timeout started")
    time.sleep(1)
    sess.add_player("player4")
    time.sleep(0.5)
    sess.add_player("player5")
    sess.add_player("player6")

    #test add full game
    print("Test adding player in full game")
    time.sleep(0.5)
    sess.add_player("player7")

    # Test getting player turns
    print("Getting players turns")
    time.sleep(2.1)
    sess.get_next_turn()
    sess.get_next_turn()
    sess.get_next_turn()
    sess.get_next_turn()
    sess.get_next_turn()
    sess.get_next_turn()
    # Return to player 1
    sess.get_next_turn()
    sess.get_next_turn()
    sess.get_next_turn()


    # Test Token functionality
    #TODO: Integrate with get_next_turn()
    time.sleep(0.2)
    print("Token GET and SET test")
    #print(f"Available Tokens: {sess.get_available_tokens()}")
    sess.set_players_token("player3", "Mrs. White")
    print("Test set")
    #print(f"Available Tokens: {sess.get_available_tokens()}")

    print("Main game mechanics")
    sess.turn_mechanics()


