from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)

"""

import logging
import logging.config
import os
import os.path
import sys

LOG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
LOG_LEVEL_STR = 'INFO'
LOG_FILE = ''

LOG_LEVEL = getattr(logging, LOG_LEVEL_STR)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

def parent_makedirs(file):
  path = os.path.dirname(os.path.expanduser(path))
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
      pass
    else:
      raise

if LOG_FILE:
  MakeDirs.parent_makedirs(LOG_FILE)
  HANDLER = logging.FileHandler(LOG_FILE)
else:
  HANDLER = None

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  if HANDLER and HANDLER not in log.handlers:
    log.addHandler(HANDLER)

  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', LOG_LEVEL_STR)

