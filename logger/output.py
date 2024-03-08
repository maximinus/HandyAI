import sys
import logging

DEFAULT_LOGGER_NAME = 'HandyLogger'


def setup_logger(name):
    # Create a custom logger
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)

    # Set the log level
    logger.setLevel(logging.DEBUG)

    # Create handlers
    stdout_handler = logging.StreamHandler(sys.stdout)

    # Create formatters and add it to handlers
    stdout_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_format)

    # Add handlers to the logger
    logger.addHandler(stdout_handler)
    return logger


logger = setup_logger()
