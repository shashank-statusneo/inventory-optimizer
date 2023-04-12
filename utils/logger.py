"""
logging module
"""
import logging


def init_logger(level="ERROR"):
    """
    Initializes a logger
    """
    logger = logging.getLogger("starter-kit")
    logger.setLevel(level)
    channel = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    channel.setFormatter(formatter)
    logger.addHandler(channel)
