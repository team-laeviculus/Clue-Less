"""
Keep It Simple Stupid....
"""

import cmd
import requests
import sys
import time

class Player:
    local_info = {
        "name": None,
        "token": None,
        "game name": None,
        "in_game": False,
        "request": None
    }

class ServerInfo:
    game_info = {
        "turn": None
    }
    address = "http://127.0.0.1:5000/games"


class CommandShell(cmd.Cmd):

    intro = "Welcome to ClueLess by Team Laeviculus. Type help or ? for a list of commands\n"
    prompt = "Enter a command> "



    def do_join(self, args):
        '''join - Join a game'''
        name = input("enter a username: ").split()[0]
        Player.local_info['name'] = name

        r = requests.post('http://127.0.0.1:5000' + '/games', json=Player.local_info)
        # r = requests.post(self.address + '/players', json={"name": self.name})
        # print(f"Server Response: {r.json()}")
        print(f"Server Response To Login: {r.text}")
        # TODO: Socket IO stuff
        self.wait_for_my_turn()

    def do_j(self, args):
        self.do_join(args)

    def do_suggest(self, args):
        '''sugest - Suggest player name'''
        for k,v in self.players.items():
            print(f"{k}: {v}")
        name = input("enter player num")
        print(f"You suggested: {self.players[int(name)]}")

    def do_quit(self, arg):
        '''quit - quit the ClueLess game and exit'''
        # Notify server

        sys.exit(0)


    def wait_for_my_turn(self, tick=0.1):
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
            r = requests.get(ServerInfo.address, data)
            print(f"response: {r}")
            r_data = r.json()
            print(r.text)
            # if "game_stae"
            # print(f"game state: {}")

            if 'turn' in r_data and r_data['turn'] == Player.local_info['token']:
                print("Its my turn!!")
                # input()
                # request.put
                # parse response
            time.sleep(tick)

c = CommandShell()
c.cmdloop()