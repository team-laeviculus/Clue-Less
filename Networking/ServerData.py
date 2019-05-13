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
            "location": None,
        }

    def get_player(self):
        return self.data

    def set_token(self, token):
        # TODO: Tokens get assigned by order joined
        self.data['token'] = token

    def set_location(self, location):
        # TODO: Starting location fixed by token. Not a player choice
        self.data['location'] = location

    def get_json(self):
        return {
            'name': self.name,
            'data': self.data
        }


class GameSession:

    """
    Holds and maintains info about a single game instance on the server
    """

    def __init__(self, game_id: int):
        self.game_id = game_id

        # Active Game Info
        self.player_count = 0  # Number of Players
        self.current_player_turn = -1  # Current Players turn (-1 until game starts)
        self.players_turn_name = None
        self.player_data = OrderedDict()  # Holds an ordered list of players
        self.game_board = GameBoard(ClueLessCommon.db_controller)  # DB connection
        self.game_state = GameState()  # Game State Object

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
        log.debug(f"New GameSession created with object ID: {self.game_id}")


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
            log.debug(f"[game: {self.game_id}]: Canceling timer... is canceled? {self.timeout_timer_thread.is_alive()}")
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

            self.game_state.set_state(GameState.GAME_RUNNING)
            self.get_next_turn()
            log.debug(f"[game: {self.game_id}]: Game started")
        except Exception as e:
            log.error(f"GameSession start_game Exception: {e}")
            traceback.print_exc()
        finally:
            self.game_session.CLUELESS_MUTEX.release()



    def add_player(self, player_name: str):
        """
        Adds a player to game session storage and to DB
        :param player_name:
        :return: Player object which was just added
        """
        log.debug(f"[game: {self.game_id}]: Attempting to add player {player_name}")
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
            log.debug(f"[game: {self.game_id}]: Player {player_name} added")
            return self.player_data[player_name]

        else:
            # This should never happen, if games being full is properly handled
            # at the server level.
            log.fatal(f"[game: {self.game_id}]: Game is full!")
            raise Exception(f"Game-{self.game_id}: add_player exception! Game Full")

    def get_player_cards(self, name):
        """
        Returns a list of the players cards from the database
        :param name: players name as a string
        :return: list of card tuples: [(card_id, card_type, card_info)]
        """
        return self.__get_player_cards(name)

    def get_next_turn(self):
        """
        Rotates around by player count in the game to determine the turn.

        :return: the self.player[<playername>] object of player whose turn it is
        or None if game not ready
        """
        state = self.game_state.get_state()
        log.info(f"[game: {self.game_id}]: get_next_turn. Current state is {state}")

        if state == GameState.GAME_RUNNING:
            if self.players_turn_name is None or self.current_player_turn == -1:
                # Assign the first player whose turn it will be
                log.info(f"[game: {self.game_id}]: players turn is none, setting first players turn")
                self.players_turn_name = next(iter(self.player_data.items()))[0]
                self.current_player_turn = 0

            this_players_turn = list(self.player_data.items())[self.current_player_turn]
            # this_players_turn[1]["my_turn"] = True
            log.info(f"[game: {self.game_id}]: New Current Players Turn: {this_players_turn}")
            self.__set_next_players_turn_in_db(this_players_turn[0])
            self.current_player_turn = (self.current_player_turn + 1) % self.player_count
            log.info(f"[game: {self.game_id}]: Players Turn set!")
            return this_players_turn

        log.info(f"[game: {self.game_id}]: Game state is not ready to return a players turn")
        return None

    # -----------------------------------------------------------------
    #                       Helper Functions
    # -----------------------------------------------------------------
    def __add_player(self):
        """
        Private helper method for adding player and checking if game should start
        :return:
        """
        if self.player_count >= ClueLessCommon.MIN_NUMBER_OF_PLAYERS:
            log.info(f"[game: {self.game_id}]: Starting timeout timer")
            if self.timer_running:
                self.timeout_timer_thread.cancel()
                self.timeout_timer_thread = threading.Timer(
                    ClueLessCommon.TIMEOUT_TIME,
                    self.start_game
                )
                self.timeout_timer_thread.start()
            else:
                log.info(f"[game: {self.game_id}]: Starting timeout timer for first time")
                self.timeout_timer_thread.start()
                self.timer_running = True
                # self.game_state = Cl

    def __set_next_players_turn_in_db(self, player_name: str):
        self.game_session.db_controller.update_active_turn(player_name)

    def __get_player_cards(self, player_name):
        db = self.game_session.db_controller
        log.info(f"[get_cards] Getting cards for player: {player_name}")
        row = db.get_player_by_name(player_name)
        log.info(f"[get_cards] Player id: {row[2]}")
        cards = db.get_player_cards(self.game_id, int(row[2]))
        log.info(f"[get_cards] Cards: {cards}")
        return cards


    def get_state(self):
        return self.game_state.get_state()

    # -----------------------------------------------------------------
    #                    JSON Message Creators
    # -----------------------------------------------------------------

    def get_game_state_json(self):
        """
        Creates a json object representing the game state
        :return: JSON object representing game state
        """
        current_turn = None
        # if self.current_player_turn in self.player_data:
        #     current_turn = self.player_data[self.current_player_turn]
        # else:
        #     current_turn = self.player_data[0]
        return {
            'game_id': self.game_id,
            'state': self.game_state.get_state(),
            'players': {name: pdata.data for name, pdata in self.player_data.items()},
            'player_count': self.player_count,
            'turn': self.get_current_turn(True)
        }

    def get_current_turn(self, player_only=False):
        turn = {'name': "None"}
        if self.players_turn_name:
            print(f"Player name: {self.players_turn_name[0]}")
            turn = self.player_data[self.players_turn_name].get_json()

        print(f"Turn Info")
        if player_only:
            return turn
        return {
            'game_id': self.game_id,
            'state': self.game_state.get_state(),
            'turn': turn
        }






