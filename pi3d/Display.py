from ctypes import c_int
from ctypes import c_float

import Image

import pi3d

from pi3d.pi3dCommon import *
from pi3d import Constants

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

    if Constants.VERBOSE:
      print Constants.STARTUP_MESSAGE % dict(version=Constants.__version__,
                                             width=self.max_width,
                                             height=self.max_height)

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

    create_display(self, x, y, w, h, depth)

    #Setup perspective view
    opengles.glMatrixMode(GL_PROJECTION)
    pi3d.load_identity()
    hht = near * math.tan(aspect / 2.0 / 180.0 * 3.1415926)
    hwd = hht * w / h
    opengles.glFrustumf(c_float(-hwd), c_float(hwd), c_float(-hht), c_float(hht), c_float(near), c_float(far))
    opengles.glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    opengles.glMatrixMode(GL_MODELVIEW)
    pi3d.load_identity()


  def create2D(self, x=0, y=0, w=0, h=0, depth=24, near=-1.0, far=100.0):
    if w <= 0 or h <= 0:
        w = self.max_width
        h = self.max_height

    self.win_width = w
    self.win_height = h

    create_display(self,x,y,w,h,depth)

    opengles.glMatrixMode(GL_PROJECTION)
    pi3d.load_identity()
    opengles.glOrthof(c_float(0), c_float(w), c_float(0), c_float(h), c_float(-1), c_float(500))
    opengles.glMatrixMode(GL_MODELVIEW)
    pi3d.load_identity()

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
    if Constants.VERBOSE:
      print "Taking screenshot to '",filestring,"'"

    size = self.win_height * self.win_width * 3
    img = (ctypes.c_char*size)()
    opengles.glReadPixels(0,0,self.win_width,self.win_height,
                          GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))
    im = Image.frombuffer("RGB",(self.win_width,self.win_height),
                          img, "raw", "RGB", 0,1)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(filestring)


