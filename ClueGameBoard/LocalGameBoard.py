# from Databases.DBController import *
from Databases.db_mgmt import CluelessDB
# Current GUI is set to Width = 600 and Height = 600. 75,75 is currently static middle position of top left room. All other rooms are 225 in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...


class BoardLocation:

    def __init__(self, name, position_x, position_y):
        self.name = name
        self.positionX = position_x
        self.positionY = position_y


class Room(BoardLocation):

    def __init__(self, name, x, y):
        self.room_type = "Room"
        BoardLocation.__init__(self, name, x, y)

# Current GUI is set to Width = 600 and Height = 600. 187.5,75 is currently static middle position of hallway from top left room to top middle room. All other rooms are 225 in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...
#Hallways are 75 in pixels in length. (75/2) + length of room (150)...


class Hall(BoardLocation):

    def __init__(self, name, x, y):
        self.room_type = "Hall"
        BoardLocation.__init__(self, name, x, y)


class Player:

    def __init__(self, player_name, player_position_x, player_position_y):
        self.name = player_name
        self.positionX = player_position_x
        self.positionY = player_position_y
        # TODO: Update stuff to take Board Location object for location info
        self.board_location = None

    def set_board_location(self, board_location: BoardLocation):
        """

        :param board_location:
        :return:
        """
        self.board_location = board_location
        self.set_player_position(board_location.positionX, board_location.positionY)

    def set_player_position(self, player_position_x, player_position_y):
        self.positionX = player_position_x
        self.positionY = player_position_y

    def get_name(self) -> str:
        return self.name

    def get_board_location(self) -> BoardLocation:
        return self.board_location

    def __str__(self):
        return (f'Name: {self.name}'
                + f', x: {self.positionX}'
                + f', y: {self.positionY}')

    def __repr__(self):
        return f"Player({self.name}, {self.positionX}, {self.positionY})"

class GameBoard:

    """
    Gameboard object
    """

    # Static Variables

    # Rooms
    kitchen = Room('Kitchen', 5, 5)
    conservatory = Room('Conservatory', 5, 1)
    dining_room = Room('Dining Room', 3, 5)
    ballroom = Room('Ballroom', 5, 3)
    study = Room('Study', 1, 1)
    hall = Room('Hall', 1, 3)
    lounge = Room('Lounge', 1, 5)
    library = Room('Library', 3, 1)
    billard_room = Room('Billard Room', 3, 3)

    # Hallways
    s_h = Hall("study_hall", 1, 2)
    h_l = Hall("hall_lounge", 1, 4)
    li_br = Hall("library_billard room", 3, 2)
    br_dr = Hall("billard room_dinning room", 3, 4)
    c_b = Hall("conservatory_ballroom", 5, 2)
    b_k = Hall("ballroom_kitchen", 5, 4)
    s_li = Hall("study_library", 2, 1)
    h_br = Hall("hall_billard room", 2, 3)
    l_dr = Hall("lounge_dining room", 2, 5)
    li_c = Hall("library_conservatory", 4, 1)
    br_b = Hall("billard room_ballroom", 4, 3)
    dr_k = Hall("dining room_kitchen", 4, 5)

    def __init__(self, db_controller):
        self.name = "Clue-Less GameBoard"
        self.rooms = []
        self.hallways = []
        self.winner = None
        self.db_conn = db_controller

    def add_room(self, room):
        self.rooms.append(room)

    def add_hall(self, hall):
        self.hallways.append(hall)

    def set_game_winner(self, player):
        """
        Sets the game board winner by player name
        :param player:
        :return:
        """
        self.winner = player.name

    def get_halls(self):
        return self.hallways

    def get_hall_names(self):
        hall_objs = self.get_halls()
        hall_names = []
        for hall in hall_objs:
            hall_names.append(hall.name)
        return hall_names

# Current GUI is set to Width = 600 and Height = 600, 225 currently static distance of closes room in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...
    def get_connected_rooms(self, room_name):
        room_obj = self.get_room_object(room_name)
        if room_obj is None:
            print("No room object found")
            return None
        connected = []
        current = self.rooms + self.hallways
        current.remove(room_obj)
        for rooms in current:
            if room_obj.positionX == rooms.positionX:
                if rooms.positionY -1 <= room_obj.positionY <= rooms.positionY +1:
                    connected.append(rooms.name)

            if room_obj.positionY == rooms.positionY:
                if rooms.positionX - 1 <= room_obj.positionX <= rooms.positionX + 1:
                    connected.append(rooms.name)

            if abs(room_obj.positionX - rooms.positionX) == 4:
                if abs(room_obj.positionY - rooms.positionY) == 4:
                    connected.append(rooms.name)

        return connected

    def check_if_legal_move(self, current_location, dest_location):

        #if moving to a connected room
        print(self.get_connected_rooms(current_location))
        if dest_location in self.get_connected_rooms(current_location):

            #if moving to a hall, check if it's empty
            if dest_location in self.get_hall_names():
                space_info = self.db_conn.get_player_by_location(dest_location)
                if not space_info:
                    return True
                else:
                    return False
            else:
                return True

        return False

    def move_player(self, player: Player, dest_space, is_suggestion=False):
        if not is_suggestion:
            is_legal = self.check_if_legal_move(player.board_location.name, dest_space)
            if not is_legal:
                # throw some error
                print("This move is illegal")
                return False
        self.db_conn.update_player_location(player.name, dest_space)

    @staticmethod
    def create_game_board(db_controller: CluelessDB, print_board=False):

        game_board = GameBoard(db_controller)

        game_board.add_room(GameBoard.kitchen)
        game_board.add_room(GameBoard.conservatory)
        game_board.add_room(GameBoard.dining_room)
        game_board.add_room(GameBoard.ballroom)
        game_board.add_room(GameBoard.study)
        game_board.add_room(GameBoard.hall)
        game_board.add_room(GameBoard.lounge)
        game_board.add_room(GameBoard.library)
        game_board.add_room(GameBoard.billard_room)

        game_board.add_hall(GameBoard.s_h)
        game_board.add_hall(GameBoard.h_l)
        game_board.add_hall(GameBoard.li_br)
        game_board.add_hall(GameBoard.br_dr)
        game_board.add_hall(GameBoard.c_b)
        game_board.add_hall(GameBoard.b_k)
        game_board.add_hall(GameBoard.s_li)
        game_board.add_hall(GameBoard.h_br)
        game_board.add_hall(GameBoard.l_dr)
        game_board.add_hall(GameBoard.li_c)
        game_board.add_hall(GameBoard.br_b)
        game_board.add_hall(GameBoard.dr_k)

        if print_board:
            for room in game_board.rooms:
                print(room.name)

        return game_board

    def get_room_object(self, room_name):
        # TODO: This can be optimized
        current = self.rooms + self.hallways
        for room in current:
            if room.name == room_name:
                return room


if __name__ == '__main__':
    # db_conn = DBController("../Databases/players.db", 0)
    db_conn = CluelessDB()
    game_board = GameBoard.create_game_board(db_conn, print_board=True)

    print("="*30)
    print("Creating player John. Setting John as winner.")
    john = Player('John', 5, 5)
    game_board.set_game_winner(john)
    print(game_board.winner)

    print("="*30)
    print("Setting player position for 'john'")
    john.set_player_position(game_board.study.positionY, game_board.study.positionX)
    print(john.positionX, john.positionY)

    print("="*30)
    room_list = game_board.get_connected_rooms("Kitchen")
    print(f"Connected rooms for Kitchen: {room_list}")


    #print(game_board.check_if_legal_move(game_board.kitchen, game_board.study))
    #print(game_board.check_if_legal_move(game_board.kitchen, game_board.dr_k))

    print("Getting object")
    room_obj = game_board.get_room_object('Kitchen')
    print(room_obj.name)
    print(room_obj.positionX)
    print(room_obj.positionY)

    print(game_board.get_connected_rooms("conservatory_ballroom"))

    print(game_board.check_if_legal_move("Kitchen", "Study"))

