#############################
#  ClueLess main file. Spawns and controls all sub modules
#
#  Created by Paul Heinen: 3/8/1019
##############################

import logging
import threading
import queue
import pygame
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_logger(name: str):
    # Sets up a basic logger
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(f"logs/{name}-dev.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", datefmt='%Y-%m-%d,%H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger



if __name__ == "__main__":
    # Main method
    log = create_logger("clueless")
    log.warning("Hello, World!")
    print("Test2")
    log.error("TESTING TESTING TESTING")