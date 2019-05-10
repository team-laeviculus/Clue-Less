import threading
import random
import traceback

from collections import OrderedDict, defaultdict
from Databases.db_mgmt import CluelessDB
from ClueGameBoard.LocalGameBoard import GameBoard
from Logs.Logging import create_server_logger

"""
This file contains common classes each game might need,
or the Server needs to keep track of persistently.
"""

log = create_server_logger()

# State Machine Data
class GameState:
    # STATES
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    GAME_RUNNING = "GAME_RUNNING"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        self.CURRENT_STATE = self.WAITING_FOR_PLAYERS

    def set_state(self, state):
        """
        Note: No state validation
        :param state: A game state from the static class variables above
        :return:
        """
        if hasattr(self, state):
            self.CURRENT_STATE = state
        else:
            raise Exception(f"GameState Exception! Unknown State {state}")

    def get_state(self):
        return self.CURRENT_STATE

    def __repr__(self):
        return f"GameState: {self.CURRENT_STATE}"


class ClueLessCommon:
    """
    This class contains ACTUAL static variables that ALL game instances share.
    Because of this, this class is a singleton
    """

    db_controller = None
    CLUELESS_MUTEX = None
    # TODO: Remember to set timer to 30s
    #TIMEOUT_TIME = 30  # Timeout timer for players to join
    TIMEOUT_TIME = 5
    MIN_NUMBER_OF_PLAYERS = 3
    MAX_NUMBER_OF_PLAYERS = 6


    # Sets (not lists)
    TOKENS = {
        "Prof Plum",
        "Mrs. Peacock",
        "Mr. Green",
        "Mrs. White",
        "Col. Mustard",
        "Miss Scarlet"
    }

    HALLWAYS = {
        "study_hall",
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
    }

    ROOMS = {
        'Kitchen',
        'Conservatory',
        'Dining Room',
        'Ballroom',
        'Study',
        'Hall',
        'Lounge',
        'Library',
        'Billard Room',
    }

    # Ensures Only a single instance of this class will exist over lifetime of the server

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(ClueLessCommon)
        return cls._instance

    def __init__(self):
        self.CLUELESS_MUTEX = threading.Lock()
        self.__initialize_db_common()

    def __initialize_db_common(self):

        self.CLUELESS_MUTEX.acquire()

        try:
            self.db_controller = CluelessDB()
            self.db_controller.create_all_tables()
        finally:
            self.CLUELESS_MUTEX.release()


class Player:
    """
    Common Player Instance Class
    """

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
        # TODO: Tokens get assigned by order joined
        self.data['token'] = token

    def set_location(self, location):
        # TODO: Starting location fixed by token. Not a player choice
        self.data['location'] = location



class GameSession:

    """
    Holds and maintains info about a single game instance on the server
    """

    def __init__(self, game_id: int):
        self.game_id = game_id
        self.player_count = 0
        self.current_player_turn = -1
        self.player_data = OrderedDict()
        self.game_board = GameBoard(ClueLessCommon.db_controller)
        self.game_state = GameState()

        # Timeout timer with callback to start game
        self.timer_running = False
        self.timeout_timer_thread = threading.Timer(
            ClueLessCommon.TIMEOUT_TIME,
            self.start_game
        )

        game_session = ClueLessCommon()  # Singleton, so if it already exists, we just return it
        game_session.CLUELESS_MUTEX.acquire()

        try:
            print(f"GAME ID: {game_id}")
            game_session.db_controller.init_suspects(game_id)
            game_session.db_controller.init_weapons(game_id)
            game_session.db_controller.init_rooms(game_id)
            game_session.db_controller.init_cards(game_id)

            self.suspect, self.weapon, self.room = self._generate_solution()

            game_session.db_controller.init_case_file(
                game_id,
                self.suspect,
                self.weapon,
                self.room
            )
        except Exception as e:
            print(f"GameSession Instantiation Exception: {e}")
            traceback.print_exc()
        finally:
            game_session.CLUELESS_MUTEX.release()

        self.game_session = game_session

    def _generate_solution(self):
        """
        Randomizes solution for each game.
        :return: Game solution cards for Suspect, Weapon, and Room
        """

        # establish the solution for a game
        solution_suspect = random.randint(1, 6)
        solution_weapon = random.randint(7, 12)
        solution_room = random.randint(13, 21)
        return solution_suspect, solution_weapon, solution_room

    def start_game(self):
        """
        Starts the game
        :return:
        """
        if self.timer_running:
            self.timeout_timer_thread.cancel()
        db_conn = self.game_session.db_controller

        self.game_session.CLUELESS_MUTEX.acquire()
        try:
            db_conn.shuffle_deal_cards(
                self.game_id,
                self.player_count,
                self.suspect,
                self.weapon,
                self.room
            )

            db_conn.create_suggest_log_table()
            db_conn.create_accuse_log_table()
        except Exception as e:
            print(f"GameSession start_game Exception: {e}")
            traceback.print_exc()
        finally:
            self.game_session.CLUELESS_MUTEX.release()

    def add_player(self, player_name: str):
        """
        Adds a player to game session storage and to DB
        :param player_name:
        :return:
        """
        # TODO: Figure out how to add players better? Integrate with Game Board
        if self.player_count < ClueLessCommon.MAX_NUMBER_OF_PLAYERS:
            log.debug(f"Adding player {player_name}")
            self.player_data[player_name] = Player(player_name)
            self.player_count += 1
            self.game_session.CLUELESS_MUTEX.acquire()
            try:
                # TODO: Is this just general for all games or can we do by specific game??
                self.game_session.db_controller.put_player_in_game(player_name)
            finally:
                self.game_session.CLUELESS_MUTEX.release()

            self.__add_player()
            return self.player_data[player_name]



        else:
            # This should never happen, if games being full is properly handled
            # at the server level.
            raise Exception(f"Game-{self.game_id}: add_player exception! Game Full")

    def __add_player(self):
        """
        Private helper method for adding player and checking if game should start
        :return:
        """
        if self.player_count >= ClueLessCommon.MIN_NUMBER_OF_PLAYERS:
            log.info("Starting timeout timer")
            if self.timer_running:
                self.timeout_timer_thread.cancel()
                self.timeout_timer_thread = threading.Timer(
                    ClueLessCommon.TIMEOUT_TIME,
                    self.start_game
                )
                self.timeout_timer_thread.start()
            else:
                log.info("Starting timeout timer for first time")
                self.timeout_timer_thread.start()
                self.timer_running = True
                # self.game_state = Cl






