"""
An interactive test client for manual testing of functionality of the system.
"""

import threading
import traceback
import requests
import time
import queue
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ClueLessGUI import AbstractGUI


class CliObject(object):

    is_running = False

    def __init__(self):
        print("ClueLess Manual Test CLI Tool")
        self.is_running = True
        self.addr = 'http://localhost:5000'
        self.gui_thread_handle = None
        self.msg_queue = queue.Queue()  # Thread safe queue

        # Jank command line parser
        self.dispatch_table = {
            "get_all": lambda: requests.get(self.addr + '/players'),
            "join": lambda name: requests.post(self.addr + '/players', json={"name": name}),
            "leave": lambda name: requests.delete(self.addr + '/players', json={"name": name}),
            "get": lambda name: requests.get(self.addr + '/players/' + name),
            "update": lambda name, update: requests.put(self.addr + '/players/' + name, data=update),
            "gui" : self.create_gui_object
        }

        self.server_commands = {"get_all", "join", "leave", "get", "update"}

    def create_gui_object(self):
        handle = threading.Thread(target=AbstractGUI.thread_method,
                                  name="GUI Thread",
                                  args=(self.msg_queue,)
                                  )
        handle.start()
        return handle

    def send_response_to_thread(self, cmd, response):
        if cmd[0] in self.server_commands:
            r_code = response.status_code
            r_data = response.json()

            client_message = f"[CLIENT]: {' '.join(cmd)}"
            # server_r_string = ""
            # for k, v in r_data.items():
            #     server_r_string = server_r_string + f"{k}: {v}, "
            server_message = [f"[SERVER][{r_code}]: ", r_data]


            message = {"client": client_message, "server": server_message}
            self.msg_queue.put(message)

    def start_listener_loop(self):
        # I should have used argparser for this... oh well, I always like me some spaghetti
        # Its really easy to break this, but it will continue running since exceptions get caught
        # Exceptions that occur in the PyGame window will probably cause that window to crash.

        while self.is_running:
            cmd = input("Enter A Command> ")
            r = None
            print(f"Command Entered: {cmd}\n\r")

            if cmd == "q" or cmd == "quit":
                print("Breaking out of the loop")
                self.is_running = False
                if self.gui_thread_handle:
                    print("You have to manually exit out of the gui object")
                    self.gui_thread_handle.join()
            elif cmd == "h" or cmd == "help":
                print("List of Commands")
                for c in self.dispatch_table.keys():
                    print(c)
            else:
                # HTTP Request messages
                try:
                    parsed = cmd.split(" ")
                    cmd = parsed[0]
                    if cmd in self.dispatch_table:
                        if len(parsed) > 1:
                            if cmd == "update":
                                # This is a super lazy way of doing this and will easily break
                                n = parsed[1]
                                if "=" not in parsed[2]:
                                    print("Update Query Error. Example usage:")
                                    print("update FooBar weapon=banana")
                                    pass
                                else:
                                    double_parsed = parsed[2].split("=")
                                    dat = {double_parsed[0]: double_parsed[1]}
                                    r = self.dispatch_table[cmd](n, dat)
                                    print(f"Server Response: {r.text}")
                            else:
                                r = self.dispatch_table[cmd](parsed[1])
                                print(f"Server Response: {r.text}")
                        else:
                            r = self.dispatch_table[cmd]()
                            if cmd != "gui":
                                print(f"Server Response: {r.text}")
                            else:
                                self.gui_thread_handle = r
                                print("Gui object created. Enter next command\n\r")
                    else:
                        print(f"Error! Unknown Command {cmd}")
                        print("Use command 'h' or 'help' for list of commands")

                    self.send_response_to_thread(parsed, r)

                except Exception as e:
                    # Keep loop running even with bad commands
                    print(f"Error: {e}")
                    traceback.print_exc()

            time.sleep(300.0/1000.0)
            print("\n\r")


if __name__ == "__main__":
    print("Starting Command Line Tools. Make sure server is running!!!")
    cli_obj = CliObject()
    cli_obj.start_listener_loop()
