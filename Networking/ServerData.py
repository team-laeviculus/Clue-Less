import threading
import random
import traceback

from collections import OrderedDict
from Databases.db_mgmt import CluelessDB

"""
This file contains common classes each game might need,
or the Server needs to keep track of persistently.
"""


# State Machine Data
class GameState:
    # STATES
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    GAME_RUNNING = "GAME_RUNNING"
    GAME_VER = "GAME_OVER"

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
            self.db_controller.create_games_table()
            self.db_controller.create_player_table()
            self.db_controller.create_suspect_table()
            self.db_controller.create_weapon_table()
            self.db_controller.create_room_table()
            self.db_controller.create_cards_table()
            self.db_controller.create_notebook_table()
            self.db_controller.create_case_file_table()
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
        self.data['token'] = token

    def set_location(self, location):
        self.data['location'] = location



class GameSession:

    """
    Holds and maintains info about a single game instance on the server
    """

    def __init__(self, game_id: int):
        self.game_id = game_id
        self.player_count = 0
        self.player_data = OrderedDict()

        game_session = ClueLessCommon() # Singleton, so if it already exists, we just return it
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
        # TODO: Figure out how to add players better?
        if self.player_count < 6:
            self.player_data[player_name] = Player(player_name)
            self.player_count += 1
            self.game_session.CLUELESS_MUTEX.acquire()
            try:
                # TODO: Is this just general for all games or can we do by specific game??
                self.game_session.db_controller.put_player_in_game(player_name)
            finally:
                self.game_session.CLUELESS_MUTEX.release()
        else:
            # This should never happen, if games being full is properly handled
            # at the server level.
            raise Exception(f"Game-{self.game_id}: add_player exception! Game Full")





