import math
import threading

import Image

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
  def __init__(self, **kwds):
    """Opens up the OpenGL library and prepares a window for display."""
    super(Display, self).__init__(**kwds)
    _set_global_display(self)
    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height

    LOGGER.info(STARTUP_MESSAGE % {'version': VERSION,
                                   'width': self.max_width,
                                   'height': self.max_height})

  def create_display(self, x=0, y=0, w=0, h=0):
    self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
    assert self.display != EGL_NO_DISPLAY

    r = openegl.eglInitialize(self.display, 0, 0)
    #assert r == EGL_FALSE

    attribute_list = c_ints((EGL_RED_SIZE, 8,
                             EGL_GREEN_SIZE, 8,
                             EGL_BLUE_SIZE, 8,
                             EGL_DEPTH_SIZE, 24,  # TOD: use self.depth?
                             EGL_ALPHA_SIZE, 8,
                             EGL_BUFFER_SIZE, 32,
                             EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
                             EGL_NONE))
    numconfig = c_int()
    config = ctypes.c_void_p()
    r = openegl.eglChooseConfig(self.display,
                                ctypes.byref(attribute_list),
                                ctypes.byref(config), 1,
                                ctypes.byref(numconfig))

    context_attribs = c_ints((EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE))
    self.context = openegl.eglCreateContext(self.display, config,
                                            EGL_NO_CONTEXT, 0)
    #ctypes.byref(context_attribs) )
    assert self.context != EGL_NO_CONTEXT

    #Set the viewport position and size

    dst_rect = c_ints((x, y, w, h))
    src_rect = c_ints((x, y, w << 16, h << 16))

    self.dispman_display = bcm.vc_dispmanx_display_open(0) #LCD setting
    self.dispman_update = bcm.vc_dispmanx_update_start(0)
    self.dispman_element = bcm.vc_dispmanx_element_add(
      self.dispman_update,
      self.dispman_display,
      0, ctypes.byref(dst_rect),
      0, ctypes.byref(src_rect),
      DISPMANX_PROTECTION_NONE,
      0, 0, 0)

    nativewindow = c_ints((self.dispman_element, w, h + 1));
    bcm.vc_dispmanx_update_submit_sync(self.dispman_update)

    nw_p = ctypes.pointer(nativewindow)
    self.nw_p = nw_p

    self.surface = openegl.eglCreateWindowSurface(self.display, config, nw_p, 0)
    assert self.surface != EGL_NO_SURFACE

    r = openegl.eglMakeCurrent(self.display, self.surface, self.surface,
                               self.context)
    assert r

    #Create viewport
    opengles.glViewport(0, 0, w, h)

    #Setup default hints
    opengles.glEnable(GL_CULL_FACE)
    #opengles.glShadeModel(GL_FLAT)
    opengles.glEnable(GL_NORMALIZE)
    opengles.glEnable(GL_DEPTH_TEST)

    # Switches off alpha blending problem with desktop - is there a bug in the
    # driver?
    # Thanks to Roland Humphries who sorted this one!!
    opengles.glColorMask(1, 1, 1, 0)

    opengles.glEnableClientState(GL_VERTEX_ARRAY)
    opengles.glEnableClientState(GL_NORMAL_ARRAY)

    self.active = True

  def create(self, is_3d=True, x=0, y=0, w=0, h=0,
             near=None, far=None, aspect=60.0, depth=24):
    if w <= 0:
       w = self.max_width
    if h <= 0:
       h = self.max_height
    if near is None:
      near = 1.0 if is_3d else -1.0
    if far is None:
      far = 800.0 if is_3d else 100.0

    self.win_width = w
    self.win_height = h
    self.near = near
    self.far = far

    self.left = x
    self.top = y
    self.right = x + w
    self.bottom = y + h

    self.create_display(x, y, w, h)

    opengles.glMatrixMode(GL_PROJECTION)
    Utility.load_identity()
    if is_3d:
      hht = near * math.tan(math.radians(aspect / 2.0))
      hwd = hht * w / h
      call_float(opengles.glFrustumf, -hwd, hwd, -hht, hht, near, far)
      opengles.glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    else:
      call_float(opengles.glOrthof, 0, w, 0, h, -1, 500)

    opengles.glMatrixMode(GL_MODELVIEW)
    Utility.load_identity()


  def create3D(self, x=0, y=0, w=0, h=0,
               near=1.0, far=800.0, aspect=60.0, depth=24):
    self.create(is_3d=True, x=x, y=y, w=w, h=h, near=near, far=far,
                aspect=aspect, depth=depth)

  def create2D(self, x=0, y=0, w=0, h=0, depth=24, near=-1.0, far=100.0):
    self.create(is_3d=False, x=x, y=y, w=w, h=h, near=near, far=far,
                depth=depth)


  def destroy(self):
    if self.active:
      openegl.eglSwapBuffers(self.display, self.surface);
      openegl.eglMakeCurrent(self.display, EGL_NO_SURFACE, EGL_NO_SURFACE,
                             EGL_NO_CONTEXT)
      openegl.eglDestroySurface(self.display, self.surface)
      openegl.eglDestroyContext(self.display, self.context)
      openegl.eglTerminate(self.display)
      bcm.vc_dispmanx_display_close(self.dispman_display)
      bcm.vc_dispmanx_element_remove(self.dispman_update, self.dispman_element)
      self.active = False

  def swapBuffers(self):
    opengles.glFlush()
    opengles.glFinish()
    #clear_matrices
    openegl.eglSwapBuffers(self.display, self.surface)

  def clear(self):
    # opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def setBackColour(self, r, g, b, a):
    call_float(opengles.glClearColor, r, g, b, a)
    opengles.glColorMask(1, 1, 1, 1 if a < 1.0 else 0)
    #switches off alpha blending with desktop (is there a bug in the driver?)

  def screenshot(self, filestring):
    LOGGER.info('Taking screenshot of "%s"', filestring)

    size = self.win_height * self.win_width * 3
    img = c_chars(size)
    opengles.glReadPixels(0, 0, self.win_width, self.win_height,
                          GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))
    im = Image.frombuffer('RGB', (self.win_width, self.win_height),
                          img, 'raw', 'RGB', 0,1)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(filestring)

