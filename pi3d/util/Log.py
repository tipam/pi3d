"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)

"""

import logging
import logging.config
import sys

from pi3d.util import MakeDirs

LOG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
LOG_LEVEL = logging.INFO

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

LOG_FILE = None

def _get_handler():
  if LOG_FILE:
    MakeDirs.parent_makedirs(LOGFILE)
    handler = logging.FileHandler(f)
    return handler

HANDLER = _get_handler()

def logger(name=None):
  log = logging.getLogger(name or 'logger')
  if HANDLER and HANDLER not in log.handlers:
    log.addHandler(HANDLER)

  return log
