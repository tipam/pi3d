from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.util import Log

LOGGER = Log.logger(__name__)

class Loadable(object):
  def __init__(self):
    self.disk_loaded = False
    self.opengl_loaded = False

  def load_disk(self):
    if not self.disk_loaded:
      self._load_disk()
      self.disk_loaded = True

  def load_opengl(self, display):
    self.load_disk()
    if not self.opengl_loaded:
      if display.is_display_thread():
        self._load_opengl(display)
        self.opengl_loaded = True
      else:
        LOGGER.error('load_opengl must be called on main thread for %s', self)

  def _load_disk(self):
    """Override this to load assets from disk."""
    pass

  def _load_opengl(self, display):
    """Override this to load assets into Open GL."""
    pass
