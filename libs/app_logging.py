import logging

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S")

def use_logging():
    return logging
