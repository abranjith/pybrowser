import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from functools import lru_cache
from .constants import CONSTANTS
from .common_utils import get_user_home_dir, make_dir

_CURRENT_LOGGER = None
_DEFAULT_LOGGER = CONSTANTS.DEFAULT_LOGGER

def _default_handler(level=logging.DEBUG):
    global _DEFAULT_LOGGER
    MAX_SIZE_BYTES = 1000000
    BACKUP_COUNT = 2
    filename = f"{_DEFAULT_LOGGER}.log"
    final_path = log_path()
    p = os.path.abspath(final_path)
    p = os.path.join(p, filename)
    h = RotatingFileHandler(p, maxBytes=MAX_SIZE_BYTES, backupCount=BACKUP_COUNT)
    h.setLevel(level)
    h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    return h

def log_path():
    default_path = _get_default_path()
    given_path = CONSTANTS.DEFAULT_LOGGER_PATH
    final_path = given_path or default_path
    return final_path

def _get_default_path():
    default_path = CONSTANTS.DIR_PATH or get_user_home_dir()
    #default_path = default_path or os.path.dirname(sys.argv[0])
    default_path = os.path.join(default_path, CONSTANTS.DIR_NAME, "logs")
    make_dir(default_path)
    return default_path

def _logger_has_handler(logger):
    level = logger.getEffectiveLevel()
    current = logger
    while current:
        if any(h.level <= level for h in current.handlers):
            return True
        if not current.propagate:
            break
        current = current.parent
    return False

@lru_cache(maxsize=10)
def get_logger(logger_name=None):
    global _CURRENT_LOGGER, _DEFAULT_LOGGER
    if not logger_name:
        if _CURRENT_LOGGER:
            logger_name = _CURRENT_LOGGER
        else:
            logger_name = _DEFAULT_LOGGER
    logger = logging.getLogger(logger_name)
    _CURRENT_LOGGER = logger_name
    if logger.level == logging.NOTSET:
        logger.setLevel(logging.DEBUG)
    if _logger_has_handler(logger):
        return logger
    h = _default_handler(logger.level)
    logger.addHandler(h)
    return logger
