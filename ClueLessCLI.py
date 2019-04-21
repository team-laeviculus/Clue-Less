
import shlex
import queue
import threading
from tools.command_line_tools import CommandShell
from Networking.client import ClientNetworking
import time



class ClueLess(object):

    name = None
    address = None

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
                    print(f"Your username was set to {self.name}")
                    break
            except Exception as e:
                print(f"An exception occurred in cli tool: {e}")

        # 2. Start Client Networking Thread
        cli_net = ClientNetworking('http://127.0.0.1:5000/', 'test_name', self.inbound_q, self.outbound_q)
        cli_net.set_message_queues(self.inbound_q, self.outbound_q)
        cli_net.start()
        # 3. Start the CommandShell class
        c = CommandShell()
        c.set_name(self.name)
        c.set_message_queues(self.inbound_q, self.outbound_q)
        threading.Thread(target=c.cmdloop).start()
        print("Do I run???????????????????")
        while True:
            if not self.outbound_q.empty():
                msg = self.outbound_q.get()
                if "namespace" in msg:
                    print(f"Sending message [{msg['namespace']}]: {msg['data']}")
                    cli_net.emit_message('message', msg["data"], namespace=msg["namespace"])
                else:
                    cli_net.emit_message('message', self.outbound_q.get())
            time.sleep(0.1)

if __name__ == "__main__":
    cliptr = ClueLess("localhost:5000")
    cliptr.start_cli_tool()
    # Examples:
    # > test foobar
    # > help