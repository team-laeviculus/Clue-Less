"""
An interactive test client for manual testing of functionality of the system.
"""

import threading
import multiprocessing
import argparse
import traceback
import requests



class CliObject(object):

    is_running = False

    def __init__(self):
        print("ClueLess Manual Test CLI Tool")
        self.is_running = True
        self.addr = 'http://localhost:5000'

        # Jank command line parser
        self.dispatch_table = {
            "get_all": lambda: requests.get(self.addr + '/players'),
            "join": lambda name: requests.post(self.addr + '/players', json={"name": name}),
            "leave": lambda name: requests.delete(self.addr + '/players', json={"name": name}),
            "get": lambda name: requests.get(self.addr + '/players/' + name),
            "update": lambda name, update: requests.put(self.addr + '/players/' + name, data=update)
        }

    def start_listener_loop(self):
        cmd = ""
        while self.is_running:
            cmd = input("Enter A Command> ")
            print(f"Command Entered: {cmd}\n\r")

            if cmd == "q" or cmd == "quit":
                print("Breaking out of the loop")
                self.is_running = False
            elif cmd == "h" or cmd == "help":
                print("List of Commands")
                for c in self.dispatch_table.keys():
                    print(c)
            else:
                try:
                    parsed = cmd.split(" ")
                    cmd = parsed[0]
                    if cmd in self.dispatch_table:
                        if len(parsed) > 1:
                            if cmd == "update":
                                # This is a super lazy way of doing this and will easily break
                                n = parsed[1]
                                double_parsed = parsed[2].split("=")
                                dat = {double_parsed[0]: double_parsed[1]}
                                r = self.dispatch_table[cmd](n, dat)
                                print(f"Server Response: {r.text}")
                            else:
                                r = self.dispatch_table[cmd](parsed[1])
                                print(f"Server Response: {r.text}")
                        else:
                            r = self.dispatch_table[cmd]()
                            print(f"Server Response: {r.text}")
                    else:
                        print(f"Error! Unknown Command {cmd}")
                        print("Use command 'h' or 'help' for list of commands")

                except Exception as e:
                    # Keep loop running even with bad commands
                    print(f"Error: {e}")
                    traceback.print_exc()



if __name__ == "__main__":
    print("Starting Command Line Tools. Make sure server is running!!!")
    cli_obj = CliObject()
    cli_obj.start_listener_loop()
