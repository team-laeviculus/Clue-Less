# Current GUI is set to Width = 600 and Height = 600. 75,75 is currently static middle position of top left room. All other rooms are 225 in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...
class Room:

    name = None
    positionX = None
    positionY = None

    def __init__(self, room_name, room_position_x, room_position_y):
        self.name = room_name
        self.positionX = room_position_x
        self.positionY =  room_position_y

# Current GUI is set to Width = 600 and Height = 600. 187.5,75 is currently static middle position of hallway from top left room to top middle room. All other rooms are 225 in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...
#Hallways are 75 in pixels in length. (75/2) + length of room (150)...

class Hall:

    name = None
    positionX = None
    positionY = None

    def __init__(self, hall_name, hall_position_x, hall_position_y):
        self.name = hall_name
        self.positionX = hall_position_x
        self.positionY = hall_position_y

class Player:

    name = None
    positionX = None
    positionY = None

    def __init__(self, player_name, player_position_x, player_position_y):
        self.name = player_name
        self.positionX = player_position_x
        self.positionY = player_position_y

    def set_player_position(self,player_position_x, player_position_y):
        self.positionX = player_position_x
        self.positionY = player_position_y

class GameBoard:

    name = None
    rooms = []
    hallways = []
    winner = None

    def __init__(self):
        self.name = "Clue-Less GameBoard"
        self.rooms = []
        self.hallways = []
        self.winner = None

    def add_room(self,room):
        self.rooms.append(room)

    def add_hall(self,hall):
        self.hallways.append(hall)

    def set_game_winner(self,player):
        self.winner = player.name

# Current GUI is set to Width = 600 and Height = 600, 225 currently static distance of closes room in either direction.
# Width and Height need to be class attribute passed into this class for 225 to be variable...
    def get_connected_rooms(self, room):
        connected = []
        current = self.rooms + self.hallways
        current.remove(room)
        for rooms in current:
            if room.positionX == rooms.positionX:
                if rooms.positionY -225 <= room.positionY <= rooms.positionY +225:
                    connected.append(rooms)

            if room.positionY == rooms.positionY:
                if rooms.positionX - 225 <= room.positionX <= rooms.positionX + 225:
                    connected.append(rooms)

            if abs(room.positionX - rooms.positionX) == 450:
                if abs(room.positionY - rooms.positionY) == 450:
                    connected.append(rooms)

        return connected

#   def move(player,location)
#       #each move would be 112.5
        #if abs(player.location - location.location) <= (dice_roll)112.5
        #check if player is in the way
        #else: player.location = location.location

if __name__ == '__main__':
    kitchen = Room('Kitchen',525,525)
    conservatory = Room('Conservatory',75,525)
    dining_room = Room('Dining Room', 525, 300)
    ballroom = Room('Ballroom', 300, 525)
    study = Room('Study', 75, 75)
    hall = Room('Hall', 300, 75)
    lounge = Room('Lounge', 525, 75)
    library = Room('Library', 75, 300)
    billard_room = Room('Billard Room', 300, 300)

    john = Player('John',525,525)

    s_h = Hall("study_hall",187.5,75)
    h_l = Hall("hall_lounge",412.5,75)
    li_br = Hall("library_billard room",187.5,300)
    br_dr = Hall("billard room_dinning room", 412.5, 300)
    c_b = Hall("conservatory_ballroom",187.5,525)
    b_k = Hall("ballroom_kitchen", 412.5, 525)
    s_li = Hall("study_library", 75, 187.5)
    h_br = Hall("hall_billard room", 300, 187.5)
    l_dr = Hall("lounge_dining room", 525, 187.5)
    li_c = Hall("library_conservatory", 75, 412.5)
    br_b = Hall("billard room_ballroom", 300, 412.5)
    dr_k = Hall("dining room_kitchen", 525, 412.5)

    game_board = GameBoard()
    game_board.add_room(kitchen)
    game_board.add_room(conservatory)
    game_board.add_room(dining_room)
    game_board.add_room(ballroom)
    game_board.add_room(study)
    game_board.add_room(hall)
    game_board.add_room(lounge)
    game_board.add_room(library)
    game_board.add_room(billard_room)

    game_board.add_hall(s_h)
    game_board.add_hall(h_l)
    game_board.add_hall(li_br)
    game_board.add_hall(br_dr)
    game_board.add_hall(c_b)
    game_board.add_hall(b_k)
    game_board.add_hall(s_li)
    game_board.add_hall(h_br)
    game_board.add_hall(l_dr)
    game_board.add_hall(li_c)
    game_board.add_hall(br_b)
    game_board.add_hall(dr_k)

    for room in game_board.rooms:
        print(room.name)

    game_board.set_game_winner(john)
    print(game_board.winner)

    john.set_player_position(study.positionY,study.positionX)
    print(john.positionX, john.positionY)

    room_list = game_board.get_connected_rooms(study)
    for room in room_list:
        print(room.name)




