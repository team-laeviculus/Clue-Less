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