import time
import traceback

from pi3d.util import Log
from pi3d.Keyboard import Keyboard

LOGGER = Log.logger(__name__)

class DisplayLoop(object):
  def __init__(self, display,
               raise_exceptions=True,
               frames_per_second=0,
               check_for_close=None,
               sprites=None):
    self.sprites = sprites or []
    self.display = display
    self.raise_exceptions = raise_exceptions
    self.frames_per_second = frames_per_second
    self.check_for_close = check_for_close
    self.is_on = True

  def stop(self):
    self.is_on = False

  def loop(self):
    LOGGER.info('starting')
    self.next_time = time.time()
    while self._is_running():
      # We run our update loop in three separate parts so that we can get
      # the most acccurate values for time in the last two parts.
      self._for_each_sprite(lambda i, s: s.load())

      self.display.clear()

      if self.is_on:
        t = time.time()
        self._for_each_sprite(lambda i, s: s.update(self, i, t))
        self.display.swapBuffers()

      if self.is_on and self.frames_per_second:
        self._sleep()

    self.display.destroy()
    LOGGER.info('stopped')

  def add_sprite(self, sprite, position=None):
    if position is None:
      position = len(self.sprites)
    self.sprites.insert(position, sprite)

  def remove_sprite(self, sprite):
    self.sprites.remove(sprite)

  def _for_each_sprite(self, function):
    # TODO: do we need locking here in case self.sprites is updated in another
    # thread?  It's no big deal if we display a sprite for one frame after it's
    # been removed...
    for i, s in enumerate(self.sprites):
      try:
        function(i, s)
      except:
        LOGGER.error(traceback.format_exc())
        if self.raise_exceptions:
          raise

  def _sleep(self):
    self.next_time += 1.0 / self.frames_per_second
    delta = self.next_time - time.time()
    if delta > 0:
      time.sleep(delta)

  def _is_running(self):
    return self.is_on and (self.check_for_close and not
                           self.check_for_close(self))
