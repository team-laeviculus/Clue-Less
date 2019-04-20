import pprint
import io
import sys
import os
import argparse
import shlex
import cmd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    def do_quit(self, arg):
        '''quit - quit the ClueLess game and exit'''
        sys.exit(0)

def parse_connect(args):
    if not args:
        args = "http://localhost:5000"
    args = shlex.split(args)
    print(f"Connect args after shlex: {args}")
    print(f"Attempting to connect to server: {args[0]}")


if __name__ == "__main__":
    cmd = CommandShell()
    cmd.cmdloop()



