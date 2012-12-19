import math
import time
import threading
import traceback

from pi3d import *
from pi3d.util import Log
from pi3d.util import Utility
from pi3d.util.DisplayOpenGL import DisplayOpenGL

LOGGER = Log.logger(__name__)

CHECK_IF_DISPLAY_THREAD = True
DISPLAY_THREAD = threading.current_thread()
DISPLAY = None
ALLOW_MULTIPLE_DISPLAYS = False
RAISE_EXCEPTIONS = True

DEFAULT_ASPECT = 60.0
DEFAULT_DEPTH = 24
DEFAULT_NEAR_3D = 0.5
DEFAULT_FAR_3D = 800.0
DEFAULT_NEAR_2D = -1.0
DEFAULT_FAR_2D = 500.0

def is_display_thread():
  return not CHECK_IF_DISPLAY_THREAD or (
    DISPLAY_THREAD is threading.current_thread())

class Display(object):
  def __init__(self, tkwin):
    """Opens up the OpenGL library and prepares a window for display."""
    if not ALLOW_MULTIPLE_DISPLAYS:
      global DISPLAY
      if DISPLAY:
        LOGGER.warning('A second instance of Display was created')
      else:
        DISPLAY = self

    self.tkwin = tkwin

    self.sprites = []
    self.frames_per_second = 0
    self.is_on = True
    self.sprites_to_unload = set()

    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height

    LOGGER.info(STARTUP_MESSAGE)

  def loop(self, loop_function=lambda: None):
    LOGGER.info('starting')
    self.next_time = time.time()

    while self.is_on:
      self.clear()

      self._for_each_sprite(lambda s: s.load_opengl())

      if loop_function():
        break

      t = time.time()
      self._for_each_sprite(lambda s: s.repaint(t))

      self.swapBuffers()

      for sprite in self.sprites_to_unload:
        sprite.unload_opengl()
      self.sprites_to_unload = set()

      if self.frames_per_second:
        self.next_time += 1.0 / self.frames_per_second
        delta = self.next_time - time.time()
        if delta > 0:
          time.sleep(delta)

    self.destroy()
    LOGGER.info('stopped')

  def resize(self, x=0, y=0, w=0, h=0):
    if w <= 0:
      w = display.max_width
    if h <= 0:
      h = display.max_height
    self.win_width = w
    self.win_height = h

    self.left = x
    self.top = y
    self.right = x+w
    self.bottom = y+h
    self.opengl.resize(x, y, w, h)

  def add_sprite(self, sprite, index=None):
    if index is None:
      self.sprites.append(sprite)
    else:
      self.sprites.insert(index, sprite)

  def add_sprites(self, *sprites):
    self.sprites.extend(sprites)

  def remove_sprite(self, sprite):
    self.sprites.remove(sprite)

  def unload_opengl(self, item):
    self.sprites_to_unload.add(item)

  def _for_each_sprite(self, function):
    for s in self.sprites:
      try:
        function(s)
      except:
        LOGGER.error(traceback.format_exc())
        if RAISE_EXCEPTIONS:
          raise

  def stop(self):
    self.is_on = False

  def destroy(self):
    self.opengl.destroy()

  def swapBuffers(self):
    self.opengl.swapBuffers()

  def clear(self):
    # opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def setBackColour(self, r, g, b, alpha):
    call_float(opengles.glClearColor, r, g, b, alpha)
    opengles.glColorMask(1, 1, 1, 1 if alpha < 1.0 else 0)
    #switches off alpha blending with desktop (is there a bug in the driver?)


def create(is_3d=True, x=None, y=None, w=0, h=0, near=None, far=None,
           aspect=DEFAULT_ASPECT, depth=DEFAULT_DEPTH, background=None,
           tk=False, window_title='', window_parent=None):
  if tk:
    from pi3d.util import TkWin
    if not (w and h):
      # TODO: how do we do full-screen in tk?
      LOGGER.error("Can't compute default window size when using tk")
      raise Exception

    tkwin = TkWin(window_parent, window_title, w, h)
    tkwin.update()
    if x is None:
      x = tkwin.winx
    if y is None:
      y = tkwin.winy

  else:
    tkwin = None
    x = x or 0
    y = y or 0

  display = Display(tkwin)
  if w <= 0:
     w = display.max_width - 2 * x
     if w <= 0:
       w = display.max_width
  if h <= 0:
     h = display.max_height - 2 * y
     if h <= 0:
       h = display.max_height
  LOGGER.info('w=%d, h=%d', w, h)
  if near is None:
    near = DEFAULT_NEAR_3D if is_3d else DEFAULT_NEAR_2D
  if far is None:
    far = DEFAULT_FAR_3D if is_3d else DEFAULT_FAR_2D

  display.win_width = w
  display.win_height = h
  display.near = near
  display.far = far

  display.left = x
  display.top = y
  display.right = x + w
  display.bottom = y + h

  display.opengl.create_display(x, y, w, h)

  opengles.glMatrixMode(GL_PROJECTION)
  Utility.load_identity()
  if is_3d:
    hht = near * math.tan(math.radians(aspect / 2.0))
    hwd = hht * w / h
    call_float(opengles.glFrustumf, -hwd, hwd, -hht, hht, near, far)
    opengles.glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
  else:
    call_float(opengles.glOrthof, 0, w, 0, h, near, far)

  opengles.glMatrixMode(GL_MODELVIEW)
  Utility.load_identity()

  if background:
    display.setBackColour(*background)

  return display
