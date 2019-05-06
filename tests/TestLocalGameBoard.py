import unittest
import os, sys
import sqlite3

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
        self.game_board = GameBoard(self.db_conn)  # GameBoard.create_game_board(self.db_conn, print_board=False)
        self.test_game_num = 1
        self.db_conn.create_games_table()
        self.db_conn.create_suspect_table()
        self.db_conn.init_suspects(self.test_game_num)
        self.db_conn.create_room_table()
        self.db_conn.init_rooms(self.test_game_num)

        self.db_conn.create_player_table()

    def tearDown(self):
        pass

    # ----------------------------
    #   Helper Functions


    # Print Players Helper Function
    def printPlayersTable(self):
        c = self.db_conn.conn.cursor()  # only added to show results
        c.execute("SELECT * FROM games WHERE game_id = ?", (self.test_game_num,))
        print("games table: " + str(c.fetchall()))
        c.execute("SELECT * FROM players WHERE game_id = ?", (self.test_game_num,))
        print("players table: " + str(c.fetchall()))
        c.close()

    # print rooms helper function
    def printRooms(self):
        c = self.db_conn.conn.cursor()  # only added to show results
        c.execute("SELECT * FROM room WHERE game_id = ?", (self.test_game_num,))
        print("room table: ")
        for row in c:
            print(row)
        c.close()

    # --------------------------------------
    # Test Cases

    def test_setPlayerWinner(self):
        john = Player('John', 5, 5)
        print(f"New Player: {john}")
        self.game_board.set_game_winner(john)

        self.assertEqual(john.get_name(), self.game_board.winner)

    def test_playerUpdatePosition(self):
        # print(f"New Player: {john}")
        #
        # john.set_player_position(self.game_board.study.positionY, self.game_board.study.positionX)
        john = self.game_board.add_player('John', 5, 5)
        john = self.game_board.update_player_location(john, 'Study')
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

    def test_checkMovePlayerToLegalLocation(self):
        print("Test moving player to LEGAL location")
        # john = Player('John', 5, 5)
        # john.set_player_position(self.game_board.study.positionY, self.game_board.study.positionX)
        # john.set_board_location(GameBoard.study)
        # johns_current_location = john.get_board_location().name

        john = self.game_board.add_player('John', 5, 5)
        john = self.game_board.get_player_obj_by_name('John')
        john = self.game_board.update_player_location(john, 'Study')
        johns_current_location = john.get_board_location().name
        print(f"Current Location: {johns_current_location}")
        print(f"Adjacent Rooms: {self.game_board.get_connected_rooms(johns_current_location)}")
        self.assertEqual(
            self.game_board.check_if_legal_move(johns_current_location, "Kitchen"),
            True
        )

        self.assertEqual(
            self.game_board.check_if_legal_move(johns_current_location, "study_hall"),
            True
        )

        self.assertEqual(
            self.game_board.check_if_legal_move(johns_current_location, "study_library"),
            True
         )

    def test_checkMovePlayerToIllegalLocation(self):
        print("Test moving player to ILLEGAL location")
        # john = Player('John', 5, 5)
        # john.set_player_position(self.game_board.study.positionY, self.game_board.study.positionX)
        # john.set_board_location(GameBoard.study)
        # johns_current_location = john.get_board_location().name

        john = self.game_board.add_player('John', 5, 5)
        john = self.game_board.get_player_obj_by_name('John')
        john = self.game_board.update_player_location(john, 'Study')
        johns_current_location = john.get_board_location().name
        print(f"Current Location: {johns_current_location}")
        print(f"Adjacent Rooms: {self.game_board.get_connected_rooms(johns_current_location)}")

        self.assertEqual(
            self.game_board.check_if_legal_move(johns_current_location, "Ballroom"),
            False
        )

        self.assertEqual(
            self.game_board.check_if_legal_move(johns_current_location, "billard room_ballroom"),
            False
        )

    def test_movePlayerToLegalLocation(self):
        print("Test moving player to LEGAL location")
        # john = Player('John', 5, 5)
        # john.set_player_position(self.game_board.study.positionY, self.game_board.study.positionX)
        # john.set_board_location(GameBoard.study)
        # johns_current_location = john.get_board_location().name
        john = self.game_board.add_player('John', 5, 5)
        john = self.game_board.update_player_location(john, 'Study')
        johns_current_location = john.get_board_location().name
        print(f"Current Location: {johns_current_location}")
        print(f"Adjacent Rooms: {self.game_board.get_connected_rooms(johns_current_location)}")

        # Insert Player into DB
        # self.db_conn.put_player_in_game(john.name)
        # self.db_conn.update_player_location(john.name, johns_current_location)
        print(f"Testing If player in location in DB: {self.db_conn.get_player_by_location('Study')}")

        # print("Dumping Player Table")
        # self.printPlayersTable()
        # Move player
        self.game_board.move_player(john, "study_hall")
        print("Moving Player...")
        db_location = self.db_conn.get_player_location(john.name)
        print(f"DB Location: {db_location}")
        self.assertEqual(
            db_location,
            "study_hall"
        )






