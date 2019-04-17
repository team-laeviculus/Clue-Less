from Databases.DBController import *

# A Clue Game Board object. This is where we internally keep track of the current
# Game State, enforce the game rules, and generate list of next moves from player to choose from.
# This object should be directly re-usable on the Server


class ClueGameBoard(object):
    pass

# helper function to change the location of a player
# necessary in suggestion and movement steps
def move_player(player, room):
    DBController.update_player_by_name(player, None, None, room)

# helper function to change the location of a weapon
# necessary in suggestion step
# TODO: This depends on how weapons are stored in the game database
def move_weapon(weapon, room):
    pass

# Logic to check if next move is legal
# TODO: Update once actual game board is coded
def is_legal(current_location, next_location):

    # rooms and halls should be member variables of gameboard class
    rooms = ["Study", "Hall", "Library", "Lounge",
             "Billiard Room", "Dining Room", "Conservatory",
             "Ball Room", "Kitchen"]

    # name format for hallways is just both rooms that the hallway connects
    hallways = ["Study Hall", "Study Library", "Hall Lounge",
                    "Hall Billiard Room", "Lounge Dining Room",
                    "Library Conservatory", "Library Billiard Room"
                    "Billiard Room Dining Room", "Billiard Room Ball Room",
                    "Dining Room Kitchen", "Conservatory Ball Room", "Ball Room Kitchen"]

    if current_location in rooms:
        if next_location in hallways:

            # If you're in a room, moving to an adjacent hallway, i.e. the hallway contains the room name
            #TODO: Also check if hallway is empty (pull data from game info db)
            if current_location in next_location:
                return True
            else:
                return False
        elif next_location in rooms:
            # Moving room to room via secret passages
            if ( ( current_location == "Study" and next_location == "Kitchen") or
                    (current_location == "Kitchen" and next_location == "Study")):
                return True

            elif ( ( current_location == "Conservatory" and next_location == "Lounge") or
                   (current_location == "Lounge" and next_location == "Conservatory")):
                return True
            else:
                return False
        else:
            return False
    elif current_location in hallways:
        # if you're in a hall, moving to an adjacent room
        if next_location in rooms and next_location in current_location:
            return True
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    print("is_legal unit test starting")
    print("Legal moves")
    print(is_legal("Hall", "Study Hall"))
    print(is_legal("Study", "Study Hall"))
    print(is_legal("Study Hall", "Study"))
    print(is_legal("Study Hall", "Hall"))
    print(is_legal("Billiard Room", "Billiard Room Ball Room"))
    print(is_legal("Conservatory", "Conservatory Ball Room"))
    print(is_legal("Conservatory", "Lounge"))
    print(is_legal("Lounge", "Conservatory"))
    print(is_legal("Study", "Kitchen"))
    print(is_legal("Kitchen", "Study"))
    print("Illegal moves")
    print(is_legal("Study", "Conservatory"))
    print(is_legal("Billiard Room", "Ball Room"))
    print(is_legal("Hall", "Lounge"))
    print(is_legal("Study Hall", "Hall Lounge"))
    print(is_legal("Billiard Room Dining Room", "Dining Room Kitchen"))