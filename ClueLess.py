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


def init_logger():
    # Sets up a basic logger
    
    logger = logging.getLogger('ClueLess')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("logs/clueless-dev.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger



if __name__ == "__main__":
    # Main method
    log = init_logger()
    log.warning("Hello, World!")
    print("Test2")
    log.error("TESTING TESTING TESTING")