from collections import OrderedDict
from Networking import create_server_logger
from enum import Enum
import threading
import time
from ClueGameBoard.GameBoard_DatabaseCoordinates import GameBoard

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
    tokens_map = OrderedDict({
        "Prof Plum" : None,
        "Mrs. Peacock" : None,
        "Mr. Green" : None,
        "Mrs. White" : None,
        "Col. Mustard" : None,
        "Miss Scarlet" : None

    })
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

        self.game_tokens = create_game_tokens()

        self.game_board = GameBoard(db_controller)
        self.game_state = GameState.STOPPED

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

            # Add the player
            self.player_count += 1
            # Add player as dictionary item in local datastruct
            self.__add_player(username)

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
    # TODO: Get Next Turn
    #TODO integrate game logic
    def __start_game(self):
        print("Starting Game! No new players can join")
        self.game_state = GameState.READY
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
            this_players_turn = list(self.players.values())[self.player_turn]
            this_players_turn["my_turn"] = True
            log.info(f"New Player Turn: {this_players_turn}")
            self.player_turn = (self.player_turn + 1) % self.player_count
            return this_players_turn
        log.info("Game state is not ready to return a players turn")
        return False










if __name__ == "__main__":
    print("Starting test")
    from Databases.DBController import  DBController
    db_conn = DBController("../Databases/players.db", 0)
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


