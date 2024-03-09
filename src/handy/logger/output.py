import sys
import logging

DEFAULT_LOGGER_NAME = 'HandyLogger'


def setup_logger(name=DEFAULT_LOGGER_NAME):
    # Create a custom logger
    default_logger = logging.getLogger(name)

    # Set the log level
    default_logger.setLevel(logging.DEBUG)

    # Create handlers
    stdout_handler = logging.StreamHandler(sys.stdout)

    # Create formatters and add it to handlers
    stdout_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_format)

    # Add handlers to the logger
    default_logger.addHandler(stdout_handler)
    return default_logger


logger = setup_logger()
