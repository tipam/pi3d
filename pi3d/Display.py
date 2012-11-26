import math
import threading

from pi3d import *
from pi3d.util import Log
from pi3d.util import Utility
from pi3d.DisplayLoop import DisplayLoop
from pi3d.DisplayOpenGL import DisplayOpenGL

LOGGER = Log.logger(__name__)

CHECK_IF_DISPLAY_THREAD = True
DISPLAY_THREAD = threading.current_thread()
DISPLAY = None
ALLOW_MULTIPLE_DISPLAYS = False

DEFAULT_ASPECT = 60.0
DEFAULT_DEPTH = 24
DEFAULT_NEAR_3D = 1.0
DEFAULT_FAR_3D = 800.0
DEFAULT_NEAR_2D = -1.0
DEFAULT_FAR_2D = 500.0

def is_display_thread():
  return not CHECK_IF_DISPLAY_THREAD or (
    DISPLAY_THREAD is threading.current_thread())

def _set_global_display(display):
  if not ALLOW_MULTIPLE_DISPLAYS:
    global DISPLAY
    if DISPLAY:
      LOGGER.warning('A second instance of Display was created')
    else:
      DISPLAY = display

class Display(DisplayLoop):
  def __init__(self):
    """Opens up the OpenGL library and prepares a window for display."""
    super(Display, self).__init__()
    _set_global_display(self)
    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height

    LOGGER.info(STARTUP_MESSAGE % {'version': VERSION,
                                   'width': self.max_width,
                                   'height': self.max_height})

    self.active = True

  def create(self, is_3d=True, x=0, y=0, w=0, h=0,
             near=None, far=None, aspect=DEFAULT_ASPECT, depth=DEFAULT_DEPTH):
    if w <= 0:
       w = self.max_width
    if h <= 0:
       h = self.max_height
    if near is None:
      near = DEFAULT_NEAR_3D if is_3d else DEFAULT_NEAR_2D
    if far is None:
      far = DEFAULT_FAR_3D if is_3d else DEFAULT_FAR_2D

    self.win_width = w
    self.win_height = h
    self.near = near
    self.far = far

    self.left = x
    self.top = y
    self.right = x + w
    self.bottom = y + h

    self.opengl.create_display(x, y, w, h)

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

  def create3D(self, x=0, y=0, w=0, h=0,
               near=DEFAULT_NEAR_3D, far=DEFAULT_FAR_3D,
               aspect=DEFAULT_ASPECT, depth=DEFAULT_DEPTH):
    self.create(is_3d=True, x=x, y=y, w=w, h=h, near=near, far=far,
                aspect=aspect, depth=depth)

  def destroy(self):
    self.opengl.destroy()

  def swapBuffers(self):
    self.opengl.swapBuffers()

  def clear(self):
    # opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def setBackColour(self, r, g, b, a):
    call_float(opengles.glClearColor, r, g, b, a)
    opengles.glColorMask(1, 1, 1, 1 if a < 1.0 else 0)
    #switches off alpha blending with desktop (is there a bug in the driver?)

def create(**kwds):
  display = Display()
  display.create(**kwds)
  return display
