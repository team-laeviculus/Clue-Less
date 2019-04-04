import logging
"""
Logging utility class
"""


def create_logger(name: str):
    """
    create_logger: Creates a logger
    :param name: The name of a logger (string)
    :return: A custom logger
    """


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