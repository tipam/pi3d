from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import logging
import os
import os.path


class Log(object):
  def __init__(self, name=None, level='WARNING', file=None, format=None):
    '''
    The typical usage of the Log module has a single LOGGER per Python file.

    At the top of the file is typically:

      LOGGER = pi3d.Log(level='INFO', file='error.log')

    and then later on you can do things like:

      * LOGGER.debug('stuff here')
      * LOGGER.info('Some information about %s', some_name)
      * LOGGER.error('Not everything was displayed, sorry!')
      * LOGGER.error('You died with error code %d, message %s', error_code, msg)
      * LOGGER.critical('Your machine is about to explode.  Leave the building.')

    (Note that the values for the format string, like "some_name", "error_code" or
    "msg" are passed in as arguments - that's so you never even construct the
    message if it isn't going to be displayed.)

    ***N.B. if name is not passed as an argument then this will set the root
    logger properties (and all the pi3d module logging will also be logged,
    which is what you usually want.)***

    The level, file, format arguments are passed on to set_logs() see below.
    '''
    self.logger = logging.getLogger(name) # NB overriding default None will stop module logging!

    self.debug = self.logger.debug # to reference methods to those of the logger instance
    self.info = self.logger.info
    self.warning = self.logger.warning
    self.error = self.logger.error
    self.critical = self.logger.critical

    # pi3d only adds one handler for each instance of Log. self.HANDLER holds a 
    # reference to it so that can be changed by subsequent calls to set_logs()
    self.HANDLER = None
    self.set_logs(level, file, format)

  def set_logs(self, level=None, file=None, format=None):
    '''
    You can redirect, filter or reformat your logging by calling Log.set_logs().
    Log.set_logs() has three optional parameters:

      level:
        can be one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
        Everything that's the current log level or greater is displayed -
        for example, if your current log level is 'WARNING', then you'll display
        all warning, error, or critical messages. If this argument is not
        supplied then the level will not change from previously set.

      file:
         is the name of a file to which to redirect messages. If this argument
         is not supplied or is set to None then logging to file will stop
         if previously set, and will be directed to terminal.

      format:
         controls what information is in the output messages.  The default is
           `'%(asctime)s %(levelname)s: %(name)s: %(message)s'`
         which results in output looking like this:
          `time LEVEL: filename: Your Message Here.`'''

    if level is not None:
      self.logger.setLevel(level.upper())

    hdlrs = self.logger.handlers # shortcut
    if self.HANDLER is not None: # this is one created by pi3d previously
      if self.HANDLER not in hdlrs:  # error if it's been deleted by external actions
        self.HANDLER = None # shouldn't really get here but see above
      
    if file: # make new FileHandler
      file_handler = logging.FileHandler(file)
      if self.HANDLER is not None:
        self.logger.removeHandler(self.HANDLER)
      self.logger.addHandler(file_handler)
      self.HANDLER = file_handler
    else: # check if FileHandler previously and remove so logging to screen
      if type(self.HANDLER) == logging.FileHandler:
        self.logger.removeHandler(self.HANDLER)
        self.HANDLER = None

    if self.HANDLER is None: # need to make a new StreamHandler
      self.HANDLER = logging.StreamHandler()
      self.logger.addHandler(self.HANDLER)

    if format is None:
      format = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
    self.HANDLER.setFormatter(logging.Formatter(format))
