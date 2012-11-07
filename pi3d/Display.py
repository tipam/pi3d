import math
import Image

from pi3d import *
from pi3d import Utility

class Display(object):
  def __init__(self):
    """Opens up the OpenGL library and prepares a window for display."""
    b = bcm.bcm_host_init()

    #Get the width and height of the screen
    width = c_int()
    height = c_int()
    s = bcm.graphics_get_display_size(0, ctypes.byref(width),
                                      ctypes.byref(height))
    assert s >= 0

    self.max_width = width.value
    self.max_height = height.value

    if VERBOSE:
      print STARTUP_MESSAGE % dict(version=VERSION,
                                   width=self.max_width,
                                   height=self.max_height)

  def create_display(self, x=0, y=0, w=0, h=0, depth=24):
    b = bcm.bcm_host_init()
    self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
    assert self.display != EGL_NO_DISPLAY

    r = openegl.eglInitialize(self.display,0,0)
    #assert r == EGL_FALSE

    attribute_list = c_ints((EGL_RED_SIZE, 8,
                             EGL_GREEN_SIZE, 8,
                             EGL_BLUE_SIZE, 8,
                             EGL_ALPHA_SIZE, 8,
                             EGL_DEPTH_SIZE, 24,
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

  def create3D(self, x=0, y=0, w=0, h=0,
               near=1.0, far=800.0, aspect=60.0, depth=24):
    if w <= 0 or h <= 0:
      w = self.max_width
      h = self.max_height

    self.win_width = w
    self.win_height = h
    self.near = near
    self.far = far

    self.left = x
    self.top = y
    self.right = x + w
    self.bottom = y + h

    self.create_display(x, y, w, h, depth)

    #Setup perspective view
    opengles.glMatrixMode(GL_PROJECTION)
    Utility.load_identity()
    hht = near * math.tan(math.radians(aspect / 2.0))
    hwd = hht * w / h
    opengles.glFrustumf(c_float(-hwd), c_float(hwd),
                        c_float(-hht), c_float(hht),
                        c_float(near), c_float(far))
    opengles.glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    opengles.glMatrixMode(GL_MODELVIEW)
    Utility.load_identity()


  def create2D(self, x=0, y=0, w=0, h=0, depth=24, near=-1.0, far=100.0):
    if w <= 0 or h <= 0:
        w = self.max_width
        h = self.max_height

    self.win_width = w
    self.win_height = h

    self.create_display(x, y, w, h, depth)

    opengles.glMatrixMode(GL_PROJECTION)
    Utility.load_identity()
    opengles.glOrthof(c_float(0), c_float(w), c_float(0),
                      c_float(h), c_float(-1), c_float(500))
    opengles.glMatrixMode(GL_MODELVIEW)
    Utility.load_identity()

  def destroy(self):
    if self.active:
        openegl.eglSwapBuffers(self.display, self.surface);
        openegl.eglMakeCurrent(self.display, EGL_NO_SURFACE, EGL_NO_SURFACE,
                               EGL_NO_CONTEXT)
        openegl.eglDestroySurface(self.display, self.surface)
        openegl.eglDestroyContext(self.display, self.context)
        openegl.eglTerminate(self.display)
        bcm.vc_dispmanx_display_close(self.dispman_display)
        bcm.vc_dispmanx_element_remove(self.dispman_update,self.dispman_element)
        self.active = False

  def swapBuffers(self):
    opengles.glFlush()
    opengles.glFinish()
    #clear_matrices
    openegl.eglSwapBuffers(self.display, self.surface)

  def clear(self):
    #opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  def setBackColour(self, r, g, b, a):
    self.backColour=(r, g, b, a)
    opengles.glClearColor(c_float(r), c_float(g), c_float(b), c_float(a))
    if a < 1.0:
      opengles.glColorMask(1, 1, 1, 1)
        #switches off alpha blending with desktop (is there a bug in the driver?)
    else:
        opengles.glColorMask(1, 1, 1, 0)

  def screenshot(self, filestring):
    if VERBOSE:
      print "Taking screenshot to '",filestring,"'"

    size = self.win_height * self.win_width * 3
    img = (ctypes.c_char*size)()
    opengles.glReadPixels(0,0,self.win_width,self.win_height,
                          GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))
    im = Image.frombuffer("RGB",(self.win_width,self.win_height),
                          img, "raw", "RGB", 0,1)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(filestring)


