import threading
import time
import traceback

from pi3d.util import Log
from pi3d.Keyboard import Keyboard

LOGGER = Log.logger(__name__)
MAIN_THREAD = threading.current_thread()

class DisplayLoop(object):
  def __init__(self, display,
               raise_exceptions=True,
               frames_per_second=0,
               check_for_close=None,
               sprites=None,
               check_if_display_thread=True):
    self.sprites = sprites or []
    self.display = display
    self.raise_exceptions = raise_exceptions
    self.frames_per_second = frames_per_second
    self.check_for_close = check_for_close
    self.is_on = True
    self.display_thread = None
    self.check_if_display_thread = check_if_display_thread

  def stop(self):
    self.is_on = False

  def loop(self):
    LOGGER.info('starting')
    self.next_time = time.time()

    display_phases = (self._load_opengl, self.display.clear, self._repaint,
                      self.display.swapBuffers, self._sleep)
    i = 0
    while self._is_running():
      display_phases[i]()
      i = (i + 1) % len(display_phases)

    self.display.destroy()
    LOGGER.info('stopped')

  def add_sprite(self, sprite, position=None):
    if position is None:
      position = len(self.sprites)
    self.sprites.insert(position, sprite)

  def remove_sprite(self, sprite):
    self.sprites.remove(sprite)

  def is_display_thread(self):
    return (not self.check_if_display_thread or
            threading.current_thread() is MAIN_THREAD)

  def _for_each_sprite(self, function):
    # TODO: do we need locking here in case self.sprites is updated in another
    # thread?  It's no big deal if we display a sprite for one frame after it's
    # been removed...
    for i, s in enumerate(self.sprites):
      try:
        function(s)
      except:
        LOGGER.error(traceback.format_exc())
        if self.raise_exceptions:
          raise

  def _load_opengl(self):
    self._for_each_sprite(lambda s: s.load_opengl(self.display))

  def _repaint(self):
    t = time.time()
    self._for_each_sprite(lambda s: s.repaint(self.display, t))

  def _sleep(self):
    if self.frames_per_second:
      self.next_time += 1.0 / self.frames_per_second
      delta = self.next_time - time.time()
      if delta > 0:
        time.sleep(delta)

  def _is_running(self):
    return self.is_on and (self.check_for_close and not
                           self.check_for_close(self))
