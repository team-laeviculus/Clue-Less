import logging
import os
import pathlib
"""
Logging utility class
"""

file_path = pathlib.Path(__file__).parent
def create_logger(name: str, path: str = None):
    """
    create_logger: Creates a logger
    :param name: The name of a logger (string)
    :return: A custom logger
    """

    # Sets up a basic logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # log files are located in the current working directory (Logs)

    # if path:
    #     file_path = path

    print(f"LOGGING CWD: {os.getcwd()}")
    fh = logging.FileHandler(f"{file_path}/{name}-dev.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def create_background_logger(name: str, path: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f"{path}/{name}-dev.log")
    print(f"{fh}")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

# server_logger = None
# Create a Global Server Logger
server_logger = None
def create_server_logger():
    global server_logger
    if not server_logger:
        server_logger = create_logger("server", file_path)
    return server_logger

# server_logger = create_logger("server", "../Logs")