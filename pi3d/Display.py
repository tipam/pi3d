import math
import time
import threading
import traceback

from pi3d import *
from pi3d.util.Locker import Locker
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
WIDTH = 0
HEIGHT = 0

def is_display_thread():
  return not CHECK_IF_DISPLAY_THREAD or (
    DISPLAY_THREAD is threading.current_thread())

class Display(object):
  def __init__(self, tkwin):
    """Opens up the OpenGL library and prepares a window for display."""
    global DISPLAY
    if DISPLAY:
      assert ALLOW_MULTIPLE_DISPLAYS
      LOGGER.warning('A second instance of Display was created')
    else:
      DISPLAY = self

    self.tkwin = tkwin

    self.sprites = []
    self.sprites_to_load = set()
    self.sprites_to_unload = set()

    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height
    self.internal_loop = False
    self.external_loop = False
    self.is_running = True
    self.lock = threading.RLock()

    LOGGER.info(STARTUP_MESSAGE)

  def loop(self, loop_function=None):
    LOGGER.debug('starting')
    self.time = time.time()
    assert not self.external_loop, "Use only one of loop and loop_running"

    self.internal_loop = True
    while self.is_running:
      self._loop_begin()
      if loop_function and loop_function():
        self.stop()
      else:
        self._loop_end()

    self.destroy()
    LOGGER.debug('stopped')

  def loop_running(self):
    if self.is_running:
      assert not self.internal_loop, "Use only one of loop and loop_running"
      if self.external_loop:
        self._loop_end()
      else:
        self.time = time.time()
        self.external_loop = True  # First time.
      self._loop_begin()

    else:
      self._loop_end()
      self.destroy()

    return self.is_running

  def resize(self, x=0, y=0, w=0, h=0):
    if w <= 0:
      w = display.max_width
    if h <= 0:
      h = display.max_height
    self.width = w
    self.height = h

    self.left = x
    self.top = y
    self.right = x + w
    self.bottom = y + h
    self.opengl.resize(x, y, w, h)

  def add_sprites(self, *sprites):
    with Locker(self.lock):
      self.sprites_to_load.update(sprites)

  def remove_sprites(self, *sprites):
    with Locker(self.lock):
      self.sprites_to_unload.update(sprites)

  def _loop_begin(self):
    # TODO(rec):  check if the window was resized and resize it, removing
    # code from MegaStation to here.
    self.clear()
    with Locker(self.lock):
      self.sprites_to_load, to_load = set(), self.sprites_to_load
      self.sprites.extend(to_load)
    self._for_each_sprite(lambda s: s.load_opengl(), to_load)

  def _loop_end(self):
    with Locker(self.lock):
      self.sprites_to_unload, to_unload = set(), self.sprites_to_unload
      if to_unload:
        self.sprites = (s for s in self.sprites if s in to_unload)

    t = time.time()
    self._for_each_sprite(lambda s: s.repaint(t))

    self.swapBuffers()

    for sprite in to_unload:
      sprite.unload_opengl()

    if getattr(self, 'frames_per_second', 0):
      self.time += 1.0 / self.frames_per_second
      delta = self.time - time.time()
      if delta > 0:
        time.sleep(delta)

  def _for_each_sprite(self, function, sprites=None):
    if sprites is None:
      sprites = self.sprites
    for s in sprites:
      try:
        function(s)
      except:
        LOGGER.error(traceback.format_exc())
        if RAISE_EXCEPTIONS:
          raise

  def stop(self):
    self.is_running = False

  def __del__(self):
    self.destroy()

  def destroy(self):
    try:
      self.opengl.destroy()
    except:
      pass
    try:
      self.mouse.stop()
    except:
      pass
    try:
      self.tkwin.destroy()
    except:
      pass

  def swapBuffers(self):
    self.opengl.swapBuffers()

  def clear(self):
    # opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def set_background(self, r, g, b, alpha):
    call_float(opengles.glClearColor, r, g, b, alpha)
    opengles.glColorMask(1, 1, 1, 1 if alpha < 1.0 else 0)
    #switches off alpha blending with desktop (is there a bug in the driver?)

  def mouse_position(self):
    if self.mouse:
      return self.mouse.position()
    elif self.tkwin:
      return self.tkwin.winfo_pointerxy()
    else:
      return -1, -1


def create(is_3d=True, x=None, y=None, w=0, h=0, near=None, far=None,
           aspect=DEFAULT_ASPECT, depth=DEFAULT_DEPTH, background=None,
           tk=False, window_title='', window_parent=None, mouse=False):
  if tk:
    from pi3d.util import TkWin
    if not (w and h):
      # TODO: how do we do full-screen in tk?
      LOGGER.error("Can't compute default window size when using tk")
      raise Exception

    tkwin = TkWin.TkWin(window_parent, window_title, w, h)
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
  LOGGER.debug('Display size is w=%d, h=%d', w, h)

  if near is None:
    near = DEFAULT_NEAR_3D if is_3d else DEFAULT_NEAR_2D
  if far is None:
    far = DEFAULT_FAR_3D if is_3d else DEFAULT_FAR_2D

  display.width = w
  display.height = h
  display.near = near
  display.far = far

  display.left = x
  display.top = y
  display.right = x + w
  display.bottom = y + h

  display.opengl.create_display(x, y, w, h)
  display.mouse = None

  if mouse:
    from pi3d.Mouse import Mouse
    display.mouse = Mouse(width=w, height=h)
    display.mouse.start()

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
    display.set_background(*background)

  return display
