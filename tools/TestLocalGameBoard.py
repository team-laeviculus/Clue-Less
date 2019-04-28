import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ClueGameBoard.LocalGameBoard import GameBoard, Player
from Databases.db_mgmt import CluelessDB


class BasicLocalGameboardTest(unittest.TestCase):
    """
    Unit Tests for LocalGameBoard class
    """

    def setUp(self):
        print("Setting up for Local Gameboard Test")
        # Create DB instance
        self.db_conn = CluelessDB()
        self.game_board = GameBoard.create_game_board(self.db_conn, print_board=False)

    def tearDown(self):
        pass

    def test_setPlayerWinner(self):
        john = Player('John', 5, 5)
        print(f"New Player: {john}")
        self.game_board.set_game_winner(john)

        self.assertEqual(john.get_name(), self.game_board.winner)

    def test_playerUpdatePosition(self):
        john = Player('John', 5, 5)
        print(f"New Player: {john}")

        john.set_player_position(self.game_board.study.positionY, self.game_board.study.positionX)

        self.assertNotEqual(john.positionX, 5)
        self.assertNotEqual(john.positionY, 5)
        self.assertEqual(john.positionX, self.game_board.study.positionX)
        self.assertEqual(john.positionY, self.game_board.study.positionY)

    def test_getConnectedRooms(self):
        print("Testing get adjacent rooms")
        adjacent_rooms = self.game_board.get_connected_rooms('Kitchen')
        self.assertIn('Study', adjacent_rooms)
        self.assertIn('ballroom_kitchen', adjacent_rooms)
        self.assertIn('dining room_kitchen', adjacent_rooms)




