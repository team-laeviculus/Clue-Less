import shlex
import queue
import threading
import requests
from tools.command_line_tools import CommandShell
from Networking.client import ClientNetworking
from Logs.Logging import create_logger
import time
import traceback

log = create_logger("ClueLessCLI", "Logs")


class ClueLess(object):
    name = None # Username
    address = None # server address, unused here
    CLUE_CLI_NET = None

    def __init__(self, address, *args):
        """
        @class ClueLess: Main Clueless Client class. Runs all sub-components
        :param args:
        """
        self.address = address
        # Network message queues to be shared between threads
        self.inbound_q = queue.Queue()
        self.outbound_q = queue.Queue()

    def start_cli_tool(self):
        # 1. Get username

        while True:
            try:
                player_name = input("Enter Your Username> ")
                player_name = shlex.split(player_name)
                if player_name and len(player_name) > 1 or not player_name:
                    print(f"Invalid name. please enter a username with no spaces.")
                    pass
                else:
                    self.name = player_name[0]
                    # TODO: Invalid name handling
                    if self.login_to_server(self.name):
                        print(f"Your username was set to {self.name}")
                    else:
                        #TODO
                        pass
                    break
            except Exception as e:
                print(f"An exception occurred in cli tool: {e}")
                traceback.print_exc()

        # 2. Start Client Networking Thread
        #TODO: Update name passed to ClientNetworking
        ClueLess.CLUE_CLI_NET = ClientNetworking(self.address, self.name, self.inbound_q, self.outbound_q)
        ClueLess.CLUE_CLI_NET.set_message_queues(self.inbound_q, self.outbound_q)
        ClueLess.CLUE_CLI_NET.start()
        # 3. Start the CommandShell class
        c = CommandShell()
        c.set_name(self.name)
        c.set_message_queues(self.inbound_q, self.outbound_q)

        # Start the user input loop in another thread
        threading.Thread(target=c.cmdloop).start()

        # Listen for messages from the server
        while True:
            if not self.outbound_q.empty():
                msg = self.outbound_q.get()
                print(f"Message in outbound q: {msg}")
                if "event" in msg and "namespace" in msg:
                    # print(f"Message event is: {msg['event']}. Namespace: {msg['namespace']}")
                    print(f"Message Contents: {msg}")
                    ClueLess.CLUE_CLI_NET.emit_message(msg['event'], msg['data'], namespace=msg['namespace'])#, namespace=msg['namespace'])
                    print(f"Message fired!")
                elif "namespace" in msg:
                    print(f"Sending message [{msg['namespace']}]: {msg['data']}")
                    ClueLess.CLUE_CLI_NET.emit_message('message', msg["data"], namespace=msg["namespace"])
                else:
                    ClueLess.CLUE_CLI_NET.emit_message('message', msg)
            time.sleep(0.1)

    def login_to_server(self, desired_username):
        """
        Send a POST request to server to login with a chosen username
        :param desired_username: A username wanted by player.
        :return: True if success, False if invalid or already registered
        """
        print(f"Name being sent: {desired_username}")
        r = requests.post('http://localhost:5000' + '/players', json={"name": desired_username})
        #r = requests.post(self.address + '/players', json={"name": self.name})
        log.debug(f"Server Response To Login: {r.text}")
        # TODO error handling
        return True

if __name__ == "__main__":
    cliptr = ClueLess("http://127.0.0.1:5000/")
    cliptr.start_cli_tool()
    # Examples:
    # > test foobar
    # > help
