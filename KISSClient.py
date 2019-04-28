"""
Keep It Simple Stupid....
"""

import cmd
import requests
import sys
import shlex
import time
import traceback

from collections import OrderedDict
from http import HTTPStatus


class Player:
    local_info = {
        "name": None,
        "token": None,
        "game name": None,
        "in_game": False,
        "location": None,
        "request": None
    }


class ServerInfo:
    game_info = {
        "turn": None
    }
    address = "http://127.0.0.1:5000/games"


class LocalGameInfo:
    # Hallways
    HALLWAYS = ["study_hall",
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
                "dining room_kitchen"
                ]

    HALLWAYS_MAP = OrderedDict({k: v for k, v in enumerate(HALLWAYS)})

    ROOMS = [
        'Kitchen',
        'Conservatory',
        'Dining Room',
        'Ballroom',
        'Study',
        'Hall',
        'Lounge',
        'Library',
        'Billard Room',
    ]

    ROOM_MAP = OrderedDict({k: v for k, v in enumerate(ROOMS)})

    def __init__(self):
        pass


class CommandShell(cmd.Cmd):
    # TODO: Decouple Shell functionality into its own class

    intro = "Welcome to ClueLess by Team Laeviculus. Type help or ? for a list of commands\n"
    prompt = "Enter a command> "

    def do_get_players(self, args):
        r = requests.get(ServerInfo.address + "/players", data={})
        if not (r.status_code == HTTPStatus.OK):
            print(f"Error! {r.status_code}")
        else:
            print(f"[{r.status_code}]: Players in Game: {r.text}")

    def do_join(self, args):
        '''join - Join a game'''
        name = input("enter a username: ").split()[0]
        Player.local_info['name'] = name

        r = requests.post(ServerInfo.address + '/players', json=Player.local_info)
        # r = requests.post(self.address + '/players', json={"name": self.name})
        # print(f"Server Response: {r.json()}")
        print(f"Server Response To Login: {r.text}")
        if r.status_code == HTTPStatus.OK:
            data = r.json()
            Player.local_info['location'] = data['location']
            Player.local_info['token'] = data['token']
        # TODO: Socket IO stuff
        # self.ask_player_for_move()
        self.wait_for_my_turn()

    def do_j(self, args):
        self.do_join(args)

    def do_suggest(self, args):
        '''sugest - Suggest player name'''
        for k, v in self.players.items():
            print(f"{k}: {v}")
        name = input("enter player num")
        print(f"You suggested: {self.players[int(name)]}")

    def do_quit(self, arg):
        '''quit - quit the ClueLess game and exit'''
        # Notify server

        sys.exit(0)

    def wait_for_my_turn(self, tick=0.4):
        """
        The loop that listens for other players turns after a player makes a turn
        Breakes when inbound_q has a message saying its my turn
        :param tick: Sleep time between loops in seconds
        :return:
        """
        print(f"Waiting for my turn....")
        while True:
            data = Player.local_info
            data['request'] = 'get_next_turn'
            # r = requests.get(ServerInfo.address, json=data)
            r = requests.get(ServerInfo.address + "/turn")
            if not (r.status_code == HTTPStatus.OK):
                print(f"ERROR WITH REQUEST: {r.status_code}")
            print(f"response: {r}")
            r_data = r.json()
            print(r.text)
            # if "game_stae"
            # print(f"game state: {}")

            # if 'turn' in r_data and r_data['turn'] == Player.local_info['token']:
            # if 'turn' in r_data and r_data['turn']['name'] == Player.local_info['name']:
            if r_data and r_data['turn']['name'] == Player.local_info['name']:
                print("Its my turn!!")
                self.ask_player_for_move()
                # Get Game Board:
                # input()
                # request.put
                # parse response
            time.sleep(tick)

    ###################
    ## stupid parser
    ###################
    def move_to_loc(self, args=None):
        print(f"move {args}")
        # Do some client side validation
        for k, v in LocalGameInfo.ROOM_MAP.items():
            print(f"{k}: {v}")
        room = input("make a choice: ")
        print(f"You Chose: {room}")
        parsed_r = int(room)  # shlex.split(room)
        print(f"PArsed: {parsed_r}")

        if room and int(room) in LocalGameInfo.ROOM_MAP:
            print(f"You Chose: {LocalGameInfo.ROOM_MAP[parsed_r]}")
            return {
                "move_to_location": LocalGameInfo.ROOM_MAP[parsed_r]
            }
        return None

    def make_suggestion(self, args=None):
        print(f"suggest: {args}")
        return True

    def make_accuse(self, args=None):
        print(f"accuse: {args}")
        return True

    def ask_player_for_move(self):
        put_request = None
        moves = OrderedDict({
            1: "Move To a Location",
            2: "Make a Suggestion",
            3: "Make an Accusation"
        })

        print("Choose A Move To Make")
        for k, v in moves.items():
            print(f"{k}: {v}")

        response = input("Choose A Move To Make> ")
        print(f"REsponse: {response}")
        if response is 'q' or response is 'quit':
            sys.exit()
        else:
            try:
                parsed_r = shlex.split(response)
                num_r = int(parsed_r[0])
                print(f"Num: {num_r}")
                if num_r in moves:
                    if num_r == 1:
                        move_choice = self.move_to_loc(num_r)
                        req = dict(Player.local_info)
                        req['request'] = move_choice
                        r = requests.post(ServerInfo.address + "/turn", json=req)
                        print(f"Server Reply: {r.text}")
                        if not (r.status_code == HTTPStatus.OK):
                            self.move_to_loc(num_r)
                        else:
                            Player.local_info = move_choice
                            self.wait_for_my_turn()

                    elif num_r == 2:
                        self.make_suggestion()
                    else:
                        self.make_accuse()

            except:
                print(f"Error! Invalid response {parsed_r}")
                # self.ask_player_for_move()
                traceback.print_exc()
        req = dict(Player.local_info)
        req['request'] = put_request
        r = requests.put('http://127.0.0.1:5000' + '/games', json=req)
        print(f'server reply: {r.text}')


c = CommandShell()
# c.ask_player_for_move()
c.cmdloop()
