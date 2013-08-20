from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import logging
import os
import os.path

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

def parent_makedirs(file):
  path = os.path.dirname(os.path.expanduser(file))
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
      pass
    else:
      raise

def set_logs(level=None, file=None, format=None):
  """

  You can redirect, filter or reformat your logging by calling Log.set_logs().
  Log.set_logs() has three optional parameters:

    level:
      can be one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
      Everything that's the current log level or greater is displayed -
      for example, if your current log level is 'WARNING', then you'll display
      all warning, error, or critical messages.

    file:
       is the name of a file to which to redirect messages.

    format:
       controls what information is in the output messages.  The default is
         `'%(asctime)s %(levelname)s: %(name)s: %(message)s'`
       which results in output looking like this:
        `time LEVEL: filename: Your Message Here.`"""

  global HANDLER, LOG_LEVEL, LOG_FILE, LOG_FORMAT
  LOG_LEVEL = (level or LOG_LEVEL).upper()
  LOG_FILE = file or LOG_FILE
  LOG_FORMAT = format or LOG_FORMAT

  logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT)

  if LOG_FILE:
    parent_makedirs(LOG_FILE)
    HANDLER = logging.FileHandler(LOG_FILE)
  else:
    HANDLER = None

set_logs()

def logger(name=None):
  """
  The typical usage of the Log module has a single LOGGER per Python file.

  At the top of the file is typically:

    LOGGER = Log.logger(__name__)

  and then later on you can do things like:

    * LOGGER.debug('stuff here')
    * LOGGER.info('Some information about %s', some_name)
    * LOGGER.error('Not everything was displayed, sorry!')
    * LOGGER.error('You died with error code %d, message %s', error_code, msg)
    * LOGGER.critical('Your machine is about to explode.  Leave the building.')

  (Note that the values for the format string, like "some_name", "error_code" or
  "msg" are passed in as arguments - that's so you never even construct the
  message if it isn't going to be displayed.)
  """

  log = logging.getLogger(name or 'logging')
  if HANDLER and HANDLER not in log.handlers:
    log.addHandler(HANDLER)

  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', LOG_LEVEL)
