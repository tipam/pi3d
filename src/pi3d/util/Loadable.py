from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import logging

from pi3d import Display

LOGGER = logging.getLogger(__name__)

CHECK_IF_DISPLAY_THREAD = True
DISPLAY_THREAD = threading.current_thread()

def is_display_thread():
  return not CHECK_IF_DISPLAY_THREAD or (
    DISPLAY_THREAD is threading.current_thread())

class Loadable(object):
  def __init__(self):
    LOGGER.debug('__init__: %s', self)
    self.disk_loaded = False
    self.opengl_loaded = False

  def __del__(self):
    try:
      if not self.unload_opengl(False):  # Why does this sometimes fail?
        Display.display.unload_opengl(self)
      LOGGER.debug('__del__: %s', self)
    except:
      # Many legit reasons why this might fail, particularly during shutdown.
      # LOGGER may have been tidied away by shutdown
      pass

  def load_disk(self):
    if not self.disk_loaded:
      self._load_disk()
      self.disk_loaded = True

  def load_opengl(self):
    self.load_disk()
    if not self.opengl_loaded:
      if is_display_thread():
        self._load_opengl()
        self.opengl_loaded = True
      else:
        LOGGER.error('load_opengl must be called on main thread for %s', self)

  def unload_opengl(self, report_error=True):
    if not self.opengl_loaded:
      return True

    try:
      if is_display_thread():
        self._unload_opengl()
        self.opengl_loaded = False
        return True
      elif report_error:
        LOGGER.error('unload_opengl must be called on main thread for %s', self)
        return False
    except:
      pass  # Throws exception if called during shutdown.

  def _load_disk(self):
    """Override this to load assets from disk."""
    pass

  def _load_opengl(self):
    """Override this to load assets into Open GL."""
    pass

  def _unload_opengl(self):
    """Override this to unload assets from Open GL."""
    pass
