import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Networking.ServerData import *


class TestGameState(unittest.TestCase):
    """
    Tests the GameState Class
    """

    def test_createGameStateObj(self):
        game_state = GameState()
        self.assertEqual(game_state.get_state(), GameState.WAITING_FOR_PLAYERS)

    def test_changeOneState(self):
        game_state = GameState()
        game_state.set_state(GameState.GAME_RUNNING)
        self.assertEqual(game_state.get_state(), GameState.GAME_RUNNING)

    def test_twoInstances(self):
        game_state_1 = GameState()
        game_state_2 = GameState()

        self.assertEqual(game_state_1.get_state(), GameState.WAITING_FOR_PLAYERS)
        self.assertEqual(game_state_2.get_state(), GameState.WAITING_FOR_PLAYERS)

        game_state_1.set_state(GameState.GAME_RUNNING)

        self.assertEqual(game_state_1.get_state(), GameState.GAME_RUNNING)
        self.assertNotEqual(game_state_2.get_state(), GameState.GAME_RUNNING)


class TestClueLessCommon(unittest.TestCase):
    """
    Tests ClueLessCommon Singleton
    """
    def test_CreateInstance(self):
        COMMON = ClueLessCommon()
        self.assertIsNotNone(COMMON)

    def test_CreateTwoInstances(self):
        common_1 = ClueLessCommon()
        common_2 = ClueLessCommon()

        self.assertEqual(common_1, common_2)
        common_1.CLUELESS_MUTEX = "Test"

        self.assertEqual(common_1.CLUELESS_MUTEX, common_2.CLUELESS_MUTEX)


class TestGameSession(unittest.TestCase):
    """
    Tests a GameSession instance
    """


    def test_SessionInstantiation(self):

        sess = GameSession(1)

        self.assertEqual(sess.game_id, 1)
        self.assertEqual(sess.player_count, 0)

        self.assertIsNotNone(sess.room)
        self.assertIsNotNone(sess.suspect)
        self.assertIsNotNone(sess.weapon)

    def test_AddPlayersAndStartGame(self):

        sess = GameSession(1)

        print("Adding Players")
        sess.add_player("Joe")
        sess.add_player("Bob")
        sess.add_player("Tom")
        self.assertEqual(sess.player_count, 3)

        sess.start_game()

    def test_fullGameSession(self):
        sess = GameSession(1)

        print("Adding Players")
        sess.add_player("1")
        sess.add_player("2")
        sess.add_player("3")
        sess.add_player("4")
        sess.add_player("5")
        sess.add_player("6")

        with self.assertRaises(Exception):
            sess.add_player("7")


    def test_TwoGames(self):
        sess_1 = GameSession(1)
        sess_2 = GameSession(2)

        sess_1.add_player("Joe")
        sess_2.add_player("Bob")
        sess_1.add_player("Tom")
        sess_2.add_player("Jill")
        sess_1.add_player("Sarah")
        self.assertEqual(sess_1.player_count, 3)

        print("\n\nStarting Sess1")
        sess_1.start_game()

        sess_2.add_player("Paul")
        sess_2.add_player("Fred")
        print("\n\nStarting Sess2")
        sess_2.start_game()




