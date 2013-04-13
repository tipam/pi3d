from __future__ import absolute_import, division, print_function, unicode_literals

"""

TYPICAL USAGE.

At the top of your file, you have

  LOGGER = Log.logger(__name__)

and then later on you would say things like:

  LOGGER.debug('stuff here')
  LOGGER.info('Some information about %s', some_name)
  LOGGER.error('You died with error code %d, message %s', error_code, msg)

(Note that the values for the format string, like "some_name", "error_code" or
"msg" are passed in as arguments - that's so you never even construct the
message if it isn't going to be displayed.)


REDIRECTING OR FILTERING LOGGING.

You can control logging by change one of the following module variables -
which for the moment you have to do by editing this file.


LOG_LEVEL controls which level messages are logged.

Possible choices are DEBUG, INFO, WARNING, ERROR, CRITICAL. If the LOG_LEVEL
is DEBUG then you see all log messages - if the LOG_LEVEL is CRITICAL then you
see only critical messages.

The default value for LOG_LEVEL is INFO, so you see everything except debug
messages.


LOG_FILE is empty by default.  If it's non-empty, then the log information is
redirected to that file.  Note that the logging system will silently overwrite
whatever's at that location, so make sure it isn't anything important...


LOG_FORMAT controls what information is in the output messages.  The default is

   '%(asctime)s %(levelname)s: %(name)s: %(message)s'

which amounts to

  time LEVEL: filename: Your Message Here.

"""

import logging
import logging.config
import os
import os.path
import sys

# To get debug messages, set LOG_LEVEL to be 'DEBUG'.
#
# Possible levels are:
#   DEBUG
#   INFO
#   WARNING
#   ERROR
#   CRITICAL

LOG_LEVEL = 'INFO'

LOG_FILE = ''

LOG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

logging.basicConfig(
  level=getattr(logging, LOG_LEVEL),
  format=LOG_FORMAT)

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
LOGGER.debug('Log level is %s', LOG_LEVEL)

