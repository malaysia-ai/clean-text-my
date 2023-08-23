import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = ""


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name="clean_text_my"):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger

logger_name="clean_text_my"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
logger.addHandler(get_console_handler())
logger.propagate = False

# TODO make user can override the confige
