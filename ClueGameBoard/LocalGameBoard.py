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


class Hall(BoardLocation):

    def __init__(self, name, x, y):
        self.room_type = "Hall"
        BoardLocation.__init__(self, name, x, y)


class Player:
    # TODO: Common Player Class
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

    ROOMS = [kitchen, conservatory, dining_room, ballroom, study, hall, lounge, library, billard_room]
    HALLWAYS = [s_h, h_l, li_br, br_dr, c_b, b_k, s_li, h_br, l_dr, li_c, br_b, dr_k]

    def __init__(self, db_controller):
        self.name = "Clue-Less GameBoard"
        self.rooms = list(GameBoard.ROOMS)
        self.hallways = list(GameBoard.HALLWAYS)
        self.players = []
        self.winner = None
        self.db_conn = db_controller

    def add_player_by_room(self, name: str, location: BoardLocation):
        """
        Helper method so we can just pass a Board Location
        :param name: player name
        :param location: A board location
        :return:
        """
        self.add_player(name, location.positionX, location.positionY)

    def add_player(self, name, player_position_x, player_position_y):
        """
        Adds a player to game board
        :param name: player name
        :param player_position_x: room x value
        :param player_position_y: room y value
        :return:
        """
        location = self.get_board_location_obj_by_coords(player_position_x, player_position_y)
        # TODO: Player object already created elsewhere
        player = Player(name, player_position_x, player_position_y)
        player.set_board_location(location)
        self.players.append(player)
        self.db_conn.put_player_in_game(name)
        self.db_conn.update_player_location(player.name, player.get_board_location().name)
        return player

    def remove_player(self, name):
        pass

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

    def get_players(self):
        return self.players

    def get_player_names(self):
        player_objs = self.get_players()
        player_names = []
        for player in player_objs:
            player_names.append(player.name)
        return player_names

    def get_player_obj_by_name(self, name):
        player_objs = self.get_players()
        for player in player_objs:
            if player.name == name:
                return player

    def get_player_location(self, name):
        obj = self.get_player_obj_by_name(name)
        return obj.board_location

    def update_player_location(self, player: Player, dest_name):
        location_obj = self.get_board_location_obj_by_name(dest_name)
        for p in self.players:
            if player.name == p.name:
                p.set_board_location(location_obj)
                self.db_conn.update_player_location(player.name, dest_name)
                return p

        print("No player found in player list")
        return None

    def get_board_location_obj_by_coords(self, position_x, position_y):
        location_list = self.rooms + self.hallways
        for location in location_list:
            if location.positionX == position_x and location.positionY == position_y:
                return location
        print("No location at these coordinates")
        return None

    def get_board_location_obj_by_name(self, name):
        location_list = self.rooms + self.hallways
        for location in location_list:
            if location.name == name:
                return location
        print("No location by this name")
        return None

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
        self.update_player_location(player, dest_space)

    def get_room_object(self, room_name):
        # TODO: This can be optimized
        current = self.rooms + self.hallways
        for room in current:
            if room.name == room_name:
                return room


if __name__ == '__main__':
    # db_conn = DBController("../Databases/players.db", 0)
    db_conn = CluelessDB()
    game_board = GameBoard(db_controller=db_conn)  # GameBoard.create_game_board(db_conn, print_board=True)

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

