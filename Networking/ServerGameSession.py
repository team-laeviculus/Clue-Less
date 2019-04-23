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


class GameSession:

    """
    Server Side Game Session for handling the mechanics of a Clue Game Session
    Coordinates between players. Should be state based.
    """
    MAX_PLAYERS = 6
    MIN_PLAYER_COUNT = 3 # Min number of players to start a game
    TIMEOUT_TIME = 4 # 30 seconds

    def __init__(self, game_name, db_controller):
        self.game_name = game_name
        self.players = OrderedDict() # Preserves order of items added
        self.player_turn = 0
        self.player_count = 0

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
                #TODO: This wont work
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

    def __start_game(self):
        print("Starting Game! No new players can join")
        self.game_state = GameState.READY








if __name__ == "__main__":
    print("Starting test")
    from Databases.DBController import  DBController
    db_conn = DBController("../Databases/players.db", 0)
    print("DB controller created")
    sess = GameSession("testgame", db_controller=db_conn)
    print("Session spawned")
    sess.add_player("player1")
    sess.add_player("player2")
    sess.add_player("player3")
    print("Test adding player after timeout started")
    time.sleep(1)
    sess.add_player("player4")
    time.sleep(0.5)
    sess.add_player("player5")
    sess.add_player("player6")
    print("Test adding player in full game")
    time.sleep(0.5)
    sess.add_player("player7")