import unittest
import pathlib
import os
import tempfile
import json
from flask import jsonify
from http import HTTPStatus

from Networking import KISServer


class TestServerFunctionality(unittest.TestCase):
    """
    Full Server Side testing of Game Functionality. Emulates Clients. State driven,
    so all Client-Server interaction is scripted
    """
    def setUp(self):
        print("setting up TestServerFunctionality case")
        KISServer.app.config["TESTING"] = True
        KISServer.app.config["DEBUG"] = True
        KISServer.ClueLessCommon.initialize(reset=True)

        self.app = KISServer.app.test_client()
        self.server_url = "http://127.0.0.1:5000/"

    def tearDown(self) -> None:
        KISServer.GameState.CURRENT_STATE = KISServer.GameState.WAITING_FOR_PLAYERS
        KISServer.GameInfo.game = dict(KISServer.GameInfo.initial_state)
        KISServer.GameInfo.players_turn_name = None
        KISServer.GameInfo.current_players_turn = 0

    """
    Helper Functions
    """


    def createPlayerJSON(self, name, token=None, game_name="game1", in_game=False, location=None, request_msg=None):
        """
        Creates a Player json object. This object should be used for EVERYTHING involving player.
        Tweak fields as needed but keep it consistent.
        :param name:
        :param token:
        :param game_name:
        :param in_game:
        :param location:
        :param request:
        :return: Player JSON object
        """
        return {
            "name": name,
            "token": token,
            "game name": game_name,
            "in_game": in_game,
            "location": location,
            "request": request_msg
        }

    def postProfileToServerHelper(self, player_data):
        """
        Posts a request to server to add a player to a game
        :param player_data: a player JSON object AND HTTP status code
        :return:
        """
        print(f"Adding Player: {player_data}")
        response = self.app.post("/games/players", json=player_data)
        print("Posted Request to server")
        print("Example Git commit")
        return response

    def moveCreator(self, playerJSON, moveStringLocation):
        """
        Constructs a JSON object representing a game movement request for player. No validation
        :param playerJSON: A player JSON object
        :param moveStringLocation: A Room or Hallway Name
        :return: JSON object representing move to sent to server
        """

        move = dict(playerJSON)  # Create a copy
        move['move_to_location'] = moveStringLocation
        return move

    def getTurnHelper(self):
        """
        Helper function
        :return: JSON object with turn info AND HTTP status code
        """
        print("Getting Current Turn")
        r = self.app.get(self.server_url + "games/turn")
        return r.get_json(), r.status_code

    def makeTurnHelper(self, turn_info):
        """
        POSTS the players turn info. Does no validation, so exceptions may be thrown
        :param turn_info: JSON object containing turn info for server
        :return: Server Response AND HTTP status code
        """
        print("makeTurnHelper")
        return self.app.post(self.server_url + "games/turn", json=turn_info)

    def startGameHelper(self):
        """
        A helper method to start a game by adding 3 hard coded players
        :return: player_1, player_2, player_3
        """
        player_1 = self.createPlayerJSON(name="John")
        self.postProfileToServerHelper(player_1)
        player_2 = self.createPlayerJSON(name="Salley")
        self.postProfileToServerHelper(player_2)
        player_3 = self.createPlayerJSON(name="Ben")
        self.postProfileToServerHelper(player_3)

        return player_1, player_2, player_3

    def create_players_helper(self, num_players):
        """
        Just creates and returns JSON messages for players
        :param num_players:
        :return: list of player JSON objects
        """
        return [self.createPlayerJSON(name=f"player_{i+1}") for i in range(num_players)]



    #-------------------------------------------------------------
    # Test Cases
    def testGetNoPlayers(self):
        resp = self.app.get("/games")
        print(f"testGetPlayers [{resp.status_code}]: {resp.json}")


    def testAddOnePlayer(self):
        player = self.createPlayerJSON(name="John")
        print(f"Creating Player JSON: {player}")
        create_post = self.postProfileToServerHelper(player)

        print(f"Creating Player On Server: {create_post}")
        self.assertEqual(create_post.status_code, HTTPStatus.OK)
        data = create_post.get_json()
        print(f"Response Data: {data}")

        self.assertEqual(data['game_state'], ['WAITING_FOR_PLAYERS'])
        self.assertIsNotNone(data['location'])
        self.assertIsNotNone(data['token'])

    # @unittest.expectedFailure
    def testAddThreePlayers(self):
        """
        Tests starting a game by having 3 players join a game
        :return:
        """
        player_1 = self.createPlayerJSON(name="John")
        create_post = self.postProfileToServerHelper(player_1)
        self.assertEqual(create_post.status_code, HTTPStatus.OK)
        data_1 = create_post.get_json()
        self.assertEqual(data_1['game_state'], ['WAITING_FOR_PLAYERS'])
        # Tokens randomly assigned as of now
        self.assertIsNotNone(data_1['location'])
        self.assertIsNotNone(data_1['token'])

        player_2 = self.createPlayerJSON(name="Salley")
        create_post = self.postProfileToServerHelper(player_2)
        self.assertEqual(create_post.status_code, HTTPStatus.OK)
        data_2 = create_post.get_json()
        self.assertEqual(data_2['game_state'], ['WAITING_FOR_PLAYERS'])
        self.assertIsNotNone(data_2['location'])
        self.assertIsNotNone(data_2['token'])

        player_3 = self.createPlayerJSON(name="Ben")
        create_post = self.postProfileToServerHelper(player_3)
        self.assertEqual(create_post.status_code, HTTPStatus.OK)
        data_3 = create_post.get_json()
        self.assertEqual(data_3['game_state'], ['GAME_RUNNING'])
        self.assertIsNotNone(data_3['location'])
        self.assertIsNotNone(data_3['token'])

        # NOTE: This is hard coded to always be first player who joins
        print(f"First Players Turn: {self.getTurnHelper()}")

    def testGameStartedAndJoinWithExpectedError(self):
        """
        Tests having a started game and having another player trying to join (and hopefully failing)
        :return:
        """

        players = self.create_players_helper(3)
        print(f"players: {players}")
        r = None
        for p in players:
            r = self.postProfileToServerHelper(p)
            print(f"Response: {r}")

        self.assertEqual(r.get_json()['game_state'], ['GAME_RUNNING'])
        # Game should have started. Adding a new player to running game should fail

        p4 = self.createPlayerJSON(name="player_4")
        r = self.postProfileToServerHelper(p4)

        print(f"Response 4: {r}")
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)








