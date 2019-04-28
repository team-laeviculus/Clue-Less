import pprint
import io
import sys
import os
import argparse
import shlex
import cmd
import requests
import time
import json
from Networking.client import ClientSession, ClientNetworkHelper


# noinspection PyUnusedLocal
class CommandShell(cmd.Cmd):
    '''
    @class CommandShell: The command line ClueLess Game.

    To add a command, simple create a function below called: `do_<command_name>`.
    The command can take either 0,1, or many arguments. The action of the argument
    can be added in the function for the argument, or as a separate callback function.
    Note: Please add the docustring comment so the help function works

    You need to parse the argument first. To make things easy, just do: `args = shlex.split(args)`
    and for single arg functions, get the argument with `arg[0]`. If something might cause an exception,
    you need to add exception handling in the function or callback, otherwise the program will crash.


    Example Usage:

    Enter a command> help connect
    connect - connect to a server on address:port, if none provided localhost:5000 will be used

    Enter a command> connect localhost:5000
    Attempting to connect to server: localhost:5000
    ...


    '''

    intro = "Welcome to ClueLess by Team Laeviculus. Type help or ? for a list of commands\n"
    prompt = "Enter a command> "

    players = {
        1: "miss alice",
        2: "prof whatever"
    }

    weapons = {
        1: "knife",
        2: "gun"
    }

    name = None


    def do_connect(self, server_address):

        '''connect - connect to a server on address:port, if none provided localhost:5000 will be used'''
        # TODO
        parse_connect(server_address)

    def do_get_games(self):
        '''get_games - performs a GET request to server for a list of active games'''

        # TODO
        print("Getting the server list...")

    def do_join_game(self, game_name):
        '''join_game - attempts to join a game name passed by player. Validates to ensure the game actually exists'''
        # TODO: Check name in list of games returned from a get_games() call
        # TODO: Tell the server you want to join the game
        # TODO: Handle successful join request
        # TODO: Handle failed join request

        print(f"Attempting to join game: {game_name}")

    def do_join(self, args):
        r = requests.post('http://localhost:5000' + '/games', json={"playername": self.name})
        # r = requests.post(self.address + '/players', json={"name": self.name})
        ClientSession.CLIENT_SESSION_INFO = r.json()
        print(f"Server Response To Login: {r.text}")
        # TODO: Socket IO stuff
        data_contents = {
                "name": self.name,
                "message": "Put me in the game",
                "game_joined": ClientSession.CLIENT_SESSION_INFO['game_joined']
        }
        payload = ClientNetworkHelper.create_message_for_server(event="new player joined", data=data_contents)
        self.send_message(payload)
        self.wait_for_my_turn()

    def do_suggest(self, args):
        '''sugest - Suggest player name'''
        for k,v in self.players.items():
            print(f"{k}: {v}")
        name = input("enter player num")
        print(f"You suggested: {self.players[int(name)]}")

    def do_get_status(self, args):
        print("Latest server status...")
        if not self.inbound_q.empty():
            print(f"Queue Item: {self.inbound_q.get()}")

    def do_get_session(self, args):
        '''get_session - displays the CLIENT_SESSION_INFO '''
        if ClientSession.CLIENT_SESSION_INFO:
            print(f"client session info: {ClientSession.CLIENT_SESSION_INFO}")
        else:
            print(f"Session is empty")
    def do_quit(self, arg):
        '''quit - quit the ClueLess game and exit'''
        # Notify server

        sys.exit(0)

    def do_send(self, args):
        '''send - send a message to the server with event tag "message"'''
        data = {f"{self.name}": args}
        print(f"Sending: {data}")
        self.send_message(data)

    def do_send_namespace(self, args: str):
        args = args.split()
        print(f"Namespace send data: {args}")
        if len(args) >= 1:
            namespace = args[0]
            msg = args[1:]
            data = {
                "namespace": namespace,
                "data": msg
            }
            print(f"Sending: {data}")
            self.outbound_q.put(data)
        else:
            print("Invalid send namespace message")

    def do_get_q(self, args):
        if not self.inbound_q.empty():
            while not self.inbound_q.empty():
                print(f"QUEUE ITEMN: {self.inbound_q.get()}")


    #### WEBSOCKET SERVER INTERACTION


    def send_message(self, data: dict):
        print("[send_message] adding item to outbound q")
        self.outbound_q.put(data)

    def wait_for_my_turn(self, tick=0.1):
        """
        The loop that listens for other players turns after a player makes a turn
        Breakes when inbound_q has a message saying its my turn
        :param tick: Sleep time between loops in seconds
        :return:
        """
        print(f"Waiting for my turn....")
        while True:
            if not self.inbound_q.empty():
                data = self.inbound_q.get()
                print(f"I Got a Message! {data}")
            if ClientSession.CLIENT_SESSION_INFO['server_player_info']['my_turn'] is True:
                # TODO: Server never updates player when its not their turn (this can be done client side)
                print("Its your turn")
                # TODO: Some logic
                break
            time.sleep(tick)
        # Update local player telling them to wait for next turn
        print("Done with my turn. Waiting Again...")
        ClientSession.CLIENT_SESSION_INFO['server_player_info']['my_turn'] = False

        # start loop again
        self.wait_for_my_turn()


    def handle_inbound_message(self, message):
        """
        Parse inbound messages that dont have a callback
        :param message:
        :return:
        """





    @staticmethod
    def set_name(name):
        CommandShell.name = name

    def set_message_queues(self, inbound, outbound):

        self.inbound_q = inbound
        print(f"Inbound Message Queue Set: {inbound}")
        self.outbound_q = outbound
        print(f"Outbound Message Queue Set: {outbound}")




def parse_connect(args):
    if not args:
        args = "http://localhost:5000"
    args = shlex.split(args)
    print(f"Connect args after shlex: {args}")
    print(f"Attempting to connect to server: {args[0]}")


def start_shell():
    cmd = CommandShell()
    cmd.cmdloop()



if __name__ == "__main__":
    cmd = CommandShell()
    cmd.cmdloop()

