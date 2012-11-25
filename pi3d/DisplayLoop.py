import threading
import time
import traceback

from pi3d.util import Log
from pi3d.Keyboard import Keyboard

LOGGER = Log.logger(__name__)
RAISE_EXCEPTIONS = True

class DisplayLoop(object):
  def __init__(self, display,
               frames_per_second=0,
               check_if_close_requested=None,
               sprites=None):
    self.sprites = sprites or []
    self.main_display = display
    self.frames_per_second = frames_per_second
    self.check_if_close_requested = check_if_close_requested
    self.is_on = True
    self.display_thread = None
    self.to_unload = set()

  def stop(self):
    self.is_on = False

  def loop(self):
    LOGGER.info('starting')
    self.next_time = time.time()

    display_phases = (self._load_opengl, self.main_display.clear, self._repaint,
                      self.main_display.swapBuffers, self._unload_opengl,
                      self._sleep)
    i = 0
    while self._is_running():
      display_phases[i]()
      i = (i + 1) % len(display_phases)

    self.main_display.destroy()
    LOGGER.info('stopped')

  def add_sprite(self, sprite, position=None):
    if position is None:
      position = len(self.sprites)
    self.sprites.insert(position, sprite)

  def add_sprites(self, *sprites):
    self.sprites.extend(sprites)

  def remove_sprite(self, sprite):
    self.sprites.remove(sprite)

  def unload_opengl(self, item):
    self.to_unload.add(item)

  def _load_opengl(self):
    self._for_each_sprite(lambda s: s.load_opengl())

  def _repaint(self):
    t = time.time()
    self._for_each_sprite(lambda s: s.repaint(t))

  def _unload_opengl(self):
    for x in self.to_unload:
      x.unload_opengl()
    self.to_unload = set()

  def _sleep(self):
    if self.frames_per_second:
      self.next_time += 1.0 / self.frames_per_second
      delta = self.next_time - time.time()
      if delta > 0:
        time.sleep(delta)

  def _is_running(self):
    return self.is_on and not (self.check_if_close_requested and
                               self.check_if_close_requested(self))

  def _for_each_sprite(self, function):
    for s in self.sprites:
      try:
        function(s)
      except:
        LOGGER.error(traceback.format_exc())
        if RAISE_EXCEPTIONS:
          raise
    # TODO: do we need locking here in case self.sprites is updated in another
    # thread?  It's no big deal if we display a sprite for one frame after it's
    # been removed...
