import ctypes

from ctypes import c_int, c_float

from pi3d.constants import *

from pi3d.util.Ctypes import c_ints

class DisplayOpenGL(object):
  def __init__(self):
    b = bcm.bcm_host_init()
    assert b >= 0

    # Get the width and height of the screen
    w = c_int()
    h = c_int()
    s = bcm.graphics_get_display_size(0, ctypes.byref(w), ctypes.byref(h))
    assert s >= 0
    self.width, self.height = w.value, h.value

  def create_display(self, x=0, y=0, w=0, h=0, depth=24):
    self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
    assert self.display != EGL_NO_DISPLAY

    r = openegl.eglInitialize(self.display, 0, 0)
    #assert r == EGL_FALSE

    attribute_list = c_ints((EGL_RED_SIZE, 8,
                             EGL_GREEN_SIZE, 8,
                             EGL_BLUE_SIZE, 8,
                             EGL_DEPTH_SIZE, depth,
                             EGL_ALPHA_SIZE, 8,
                             EGL_BUFFER_SIZE, 32,
                             EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
                             EGL_NONE))
    numconfig = c_int()
    self.config = ctypes.c_void_p()
    r = openegl.eglChooseConfig(self.display,
                                ctypes.byref(attribute_list),
                                ctypes.byref(self.config), 1,
                                ctypes.byref(numconfig))

    context_attribs = c_ints((EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE))
    self.context = openegl.eglCreateContext(self.display, self.config,
                                            EGL_NO_CONTEXT, ctypes.byref(context_attribs) )
    assert self.context != EGL_NO_CONTEXT

    self.create_surface(x, y, w, h)

    opengles.glDepthRangef(c_float(-1.0), c_float(1.0))
    opengles.glClearColor (c_float(0.3), c_float(0.3), c_float(0.7), c_float(1.0))
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

    #Setup default hints
    opengles.glEnable(GL_CULL_FACE)
    opengles.glEnable(GL_NORMALIZE)
    opengles.glEnable(GL_DEPTH_TEST)
    opengles.glCullFace(GL_FRONT)
    opengles.glHint(GL_GENERATE_MIPMAP_HINT, GL_NICEST)

    # Switches off alpha blending problem with desktop - is there a bug in the
    # driver?
    # Thanks to Roland Humphries who sorted this one!!
    opengles.glColorMask(1, 1, 1, 0)

    #opengles.glEnableClientState(GL_VERTEX_ARRAY)
    #opengles.glEnableClientState(GL_NORMAL_ARRAY)
    self.active = True

  def create_surface(self, x=0, y=0, w=0, h=0):
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

    nativewindow = c_ints((self.dispman_element, w, h + 1))
    bcm.vc_dispmanx_update_submit_sync(self.dispman_update)

    nw_p = ctypes.pointer(nativewindow)
    self.nw_p = nw_p

    self.surface = openegl.eglCreateWindowSurface(self.display, self.config, self.nw_p, 0)
    assert self.surface != EGL_NO_SURFACE

    r = openegl.eglMakeCurrent(self.display, self.surface, self.surface,
                               self.context)
    assert r

    #Create viewport
    opengles.glViewport(0, 0, w, h)

  def resize(self, x=0, y=0, w=0, h=0):
    # Destroy current surface and native window
    openegl.eglSwapBuffers(self.display, self.surface)
    openegl.eglDestroySurface(self.display, self.surface)
    bcm.vc_dispmanx_display_close(self.dispman_display)
    bcm.vc_dispmanx_element_remove(self.dispman_update,
                                   self.dispman_element)

    #Now recreate the native window and surface
    self.create_surface(x, y, w, h)


  def destroy(self):
    if self.active:
      openegl.eglSwapBuffers(self.display, self.surface)
      openegl.eglMakeCurrent(self.display, EGL_NO_SURFACE, EGL_NO_SURFACE,
                             EGL_NO_CONTEXT)
      openegl.eglDestroySurface(self.display, self.surface)
      openegl.eglDestroyContext(self.display, self.context)
      openegl.eglTerminate(self.display)
      bcm.vc_dispmanx_display_close(self.dispman_display)
      bcm.vc_dispmanx_element_remove(self.dispman_update, self.dispman_element)
      self.active = False

  def swap_buffers(self):
    #opengles.glFlush()
    #opengles.glFinish()
    #clear_matrices
    openegl.eglSwapBuffers(self.display, self.surface)

