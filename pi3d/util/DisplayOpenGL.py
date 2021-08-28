import ctypes
import platform
import time

from ctypes import c_int, c_uint, c_float, byref, POINTER, c_char_p
from six_mod.moves import xrange

import pi3d
from pi3d.constants import (bcm, openegl, opengles,
    GLfloat, GLint, GLuint, GLboolean, GLsizei,
    DISPLAY_CONFIG_DEFAULT, DISPLAY_CONFIG_FULLSCREEN, DISPLAY_CONFIG_HIDE_CURSOR,
    DISPLAY_CONFIG_MAXIMIZED, DISPLAY_CONFIG_NO_FRAME, DISPLAY_CONFIG_NO_RESIZE,
    DISPMANX_FLAGS_ALPHA_PREMULT, DISPMANX_PROTECTION_NONE, EGLConfig,
    EGLDisplay, EGL_ALPHA_SIZE, EGL_BLUE_SIZE, EGL_BUFFER_SIZE,
    EGL_CONTEXT_CLIENT_VERSION, EGL_DEFAULT_DISPLAY, EGL_DEPTH_SIZE,
    EGL_DRAW, EGL_GREEN_SIZE, EGL_HEIGHT, EGL_NONE, EGL_NO_CONTEXT,
    EGL_NO_DISPLAY, EGL_NO_SURFACE, EGL_RED_SIZE, EGL_SAMPLES,
    EGL_STENCIL_SIZE, EGL_SURFACE_TYPE, EGL_WIDTH, EGL_WINDOW_BIT,
    EGLint, GL_BACK, GL_CULL_FACE, GL_CW, GL_DEPTH_TEST, GL_FRAMEBUFFER,
    GL_GENERATE_MIPMAP_HINT, GL_LESS, GL_NICEST, GL_ONE_MINUS_SRC_ALPHA,
    GL_POINT_SPRITE, GL_PROGRAM_POINT_SIZE, GL_SRC_ALPHA, GL_VERSION, GL_MAX_TEXTURE_SIZE,
    PLATFORM, PLATFORM_ANDROID, PLATFORM_PI, PLATFORM_WINDOWS)

if not (pi3d.USE_PYGAME or PLATFORM in (PLATFORM_ANDROID, PLATFORM_PI, PLATFORM_WINDOWS)):
  from pyxlib import xlib
  from pyxlib.x import (AllocNone, ButtonPressMask, ButtonReleaseMask, CWBackPixmap,
    CWBorderPixel, CWColormap, CWEventMask, EnterWindowMask, ExposureMask,
    KeyPressMask, KeyReleaseMask, LeaveWindowMask, OwnerGrabButtonMask,
    ResizeRedirectMask, StructureNotifyMask)


  from pyxlib import glx
  X_WINDOW = True
else:
  X_WINDOW = False # use this for verifications involveing xlib and glx

from pi3d.util.Ctypes import c_ints

if pi3d.USE_PYGAME:
  import pygame
  from pygame.constants import FULLSCREEN

class DisplayOpenGL(object):
  def __init__(self):
    self.d = None # display if x11 window or pygame used
    self.gl_id = b"GL" # default. Needed for converting shaders
    if PLATFORM == PLATFORM_ANDROID:
      self.width, self.height = 320, 480 # put in some non-zero place-holders
    elif PLATFORM == PLATFORM_PI:
      b = bcm.bcm_host_init()
      #assert b >= 0 ## this assertion can fail with the pi camera running too

      # Get the width and height of the screen
      w = c_int()
      h = c_int()
      s = bcm.graphics_get_display_size(0, byref(w), byref(h))
      assert s >= 0
      self.width, self.height = w.value, h.value
    elif pi3d.USE_PYGAME:
      import pygame
      pygame.init()
      self.d = pygame.display.set_mode((0, 0), 
                      pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.OPENGL)
      info = pygame.display.Info()
      self.width, self.height = info.current_w, info.current_h

    else: # use libX11
      #import subprocess # default name using XOpenDisplay(None) doesn't work on RPi4
      import os
      display_name = None #previous to RPi4 this worked but now problems..
      for f in os.listdir('/tmp/.X11-unix'):
        display_name = b':' + f[1:].encode('utf-8')
        #if display_name == b':0':
        #  break # use X0 if this exist, else use last in list (which might work!)
        self.d = xlib.XOpenDisplay(display_name) # return NULL from X function or address if sucessful
        if self.d: 
          self.screen = xlib.XDefaultScreenOfDisplay(self.d)
          self.width, self.height = xlib.XWidthOfScreen(self.screen), xlib.XHeightOfScreen(self.screen)
          break # as soon as first valid display found. TODO mulitple displays?
      if not self.d: 
        print('************************\nX11 needs to be running\n************************')
        assert False, 'Couldnt open DISPLAY {}'.format(display_name)


  def create_display(self, x=0, y=0, w=0, h=0, depth=24, samples=4, layer=0,
                     display_config=DISPLAY_CONFIG_DEFAULT, window_title='', use_glx=False):
    self.use_glx = use_glx and (X_WINDOW and hasattr(glx, 'glXChooseFBConfig')) # only use glx if x11 window and glx available
    self.display_config = display_config
    self.window_title = window_title.encode()
    if not self.use_glx:
      self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
      assert self.display != EGL_NO_DISPLAY and self.display is not None
      for smpl in [samples, 0]: # try with samples first but ANGLE dll can't cope so drop to 0 for windows
        r = openegl.eglInitialize(self.display, None, None)
        attribute_list = (EGLint * 19)(EGL_RED_SIZE, 8,
                                EGL_GREEN_SIZE, 8,
                                EGL_BLUE_SIZE, 8,
                                EGL_DEPTH_SIZE, depth,
                                EGL_ALPHA_SIZE, 8,
                                EGL_BUFFER_SIZE, 32,
                                EGL_SAMPLES, smpl,
                                EGL_STENCIL_SIZE, 8,
                                EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
                                EGL_NONE)
        numconfig = EGLint(0)
        poss_configs = (EGLConfig * 5)(*(EGLConfig() for _ in range(5)))

        r = openegl.eglChooseConfig(self.display,
                                    attribute_list,
                                    poss_configs, EGLint(len(poss_configs)),
                                    byref(numconfig))
        
        context_attribs = (EGLint * 3)(EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE)
        if numconfig.value > 0:
          self.config = poss_configs[0]
          self.context = openegl.eglCreateContext(self.display, self.config,
                                                  EGL_NO_CONTEXT, context_attribs)
          if self.context != EGL_NO_CONTEXT:
            break
      assert self.context != EGL_NO_CONTEXT and self.context is not None

    self.create_surface(x, y, w, h, layer)
    opengles.glDepthRangef(GLfloat(0.0), GLfloat(1.0))
    opengles.glClearColor (GLfloat(0.3), GLfloat(0.3), GLfloat(0.7), GLfloat(1.0))
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, GLuint(0))

    # get GL v GLES and version num for shader translation
    version = opengles.glGetString(GL_VERSION)
    version = ctypes.cast(version, c_char_p).value
    if b"ES" in version:
      for s in version.split():
        if b'.' in s:
          self.gl_id = b"GLES" + s.split(b'.')[0]
          break

    #Setup default hints
    opengles.glEnable(GL_CULL_FACE)
    opengles.glCullFace(GL_BACK)
    opengles.glFrontFace(GL_CW)
    opengles.glEnable(GL_DEPTH_TEST)
    if b"GLES" not in self.gl_id:
      if b"2" in self.gl_id:
        opengles.glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
      else:
        opengles.glEnable(GL_PROGRAM_POINT_SIZE) # only in > GL3
      opengles.glEnable(GL_POINT_SPRITE)
    opengles.glDepthFunc(GL_LESS)
    opengles.glDepthMask(GLboolean(True))
    opengles.glHint(GL_GENERATE_MIPMAP_HINT, GL_NICEST)
    opengles.glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, 
                                       1, GL_ONE_MINUS_SRC_ALPHA)
    opengles.glColorMask(GLboolean(True), GLboolean(True), GLboolean(True), GLboolean(False))
    #opengles.glEnableClientState(GL_VERTEX_ARRAY)
    #opengles.glEnableClientState(GL_NORMAL_ARRAY)
    self.max_texture_size = GLint(0)
    opengles.glGetIntegerv(GL_MAX_TEXTURE_SIZE, byref(self.max_texture_size))

    self.active = True

  def create_surface(self, x=0, y=0, w=0, h=0, layer=0):
    #Set the viewport position and size
    dst_rect = c_ints((x, y, w, h))
    src_rect = c_ints((x, y, w << 16, h << 16))

    if PLATFORM == PLATFORM_ANDROID:
      self.surface = openegl.eglGetCurrentSurface(EGL_DRAW)
      # Get the width and height of the screen - TODO, this system returns 100x100
      time.sleep(0.2) #give it a chance to find out the dimensions
      w = c_int()
      h = c_int()
      openegl.eglQuerySurface(self.display, self.surface, EGL_WIDTH, byref(w))
      openegl.eglQuerySurface(self.display, self.surface, EGL_HEIGHT, byref(h))
      self.width, self.height = w.value, h.value
    elif PLATFORM == PLATFORM_PI:
      self.dispman_display = bcm.vc_dispmanx_display_open(0) #LCD setting
      self.dispman_update = bcm.vc_dispmanx_update_start(0)
      alpha = c_ints((DISPMANX_FLAGS_ALPHA_PREMULT, 0, 0))
      self.dispman_element = bcm.vc_dispmanx_element_add(
        self.dispman_update,
        self.dispman_display,
        layer, dst_rect,
        0, src_rect,
        DISPMANX_PROTECTION_NONE,
        alpha, 0, 0)

      nativewindow = (GLint * 3)(self.dispman_element, w, h + 1)
      bcm.vc_dispmanx_update_submit_sync(self.dispman_update)

      self.nw_p = ctypes.pointer(nativewindow)
      ### NB changing the argtypes to allow passing of bcm native window is
      ### deeply unsatisfactory. But xlib defines Window as c_ulong and ctypes
      ### isn't happy about a pointer being cast to an int
      openegl.eglCreateWindowSurface.argtypes = [EGLDisplay, EGLConfig,
          POINTER((GLint * 3)), EGLint]
      self.surface = openegl.eglCreateWindowSurface(self.display, self.config, self.nw_p, 0)

    elif pi3d.USE_PYGAME:
      import pygame
      flags = pygame.OPENGL
      wsize = (w, h)
      if w == self.width and h == self.height: # i.e. full screen
        flags = pygame.FULLSCREEN | pygame.OPENGL
        wsize = (0, 0)
      if self.display_config & DISPLAY_CONFIG_NO_RESIZE:
        flags |= pygame.RESIZABLE
      if self.display_config & DISPLAY_CONFIG_NO_FRAME:
        flags |= pygame.NOFRAME
      if self.display_config & DISPLAY_CONFIG_FULLSCREEN:
        flags |= pygame.FULLSCREEN
      elif self.display_config & DISPLAY_CONFIG_MAXIMIZED:
        flags |= pygame.FULLSCREEN
        wsize = (0, 0)

      self.width, self.height = w, h
      self.d = pygame.display.set_mode(wsize, flags)
      self.window = pygame.display.get_wm_info()["window"]
      self.surface = openegl.eglCreateWindowSurface(self.display, self.config, self.window, 0)

    else: # work on basis it's X11
      # Set some WM info
      self.root = xlib.XRootWindowOfScreen(self.screen)
      if self.use_glx: # For drawing on X window with transparent background
        numfbconfigs = c_int()
        VisData = c_ints((
          glx.GLX_RENDER_TYPE, glx.GLX_RGBA_BIT,
          glx.GLX_DRAWABLE_TYPE, glx.GLX_WINDOW_BIT,
          glx.GLX_DOUBLEBUFFER, True,
          glx.GLX_RED_SIZE, 8,
          glx.GLX_GREEN_SIZE, 8,
          glx.GLX_BLUE_SIZE, 8,
          glx.GLX_ALPHA_SIZE, 8,
          glx.GLX_DEPTH_SIZE, 16,
          0))
        glx_screen = xlib.XDefaultScreen(self.d)
        fbconfigs = glx.glXChooseFBConfig(self.d, glx_screen, VisData, byref(numfbconfigs))
        fbconfig = 0
        for i in range(numfbconfigs.value):
          visual = glx.glXGetVisualFromFBConfig(self.d, fbconfigs[i]).contents
          if not visual:
            continue
          pict_format = glx.XRenderFindVisualFormat(self.d, visual.visual).contents
          if not pict_format:
            continue

          fbconfig = fbconfigs[i]
          if pict_format.direct.alphaMask > 0:
            break

        if not fbconfig:
          print("No matching FB config found")
        #/* Create a colormap - only needed on some X clients, eg. IRIX */
        cmap = xlib.XCreateColormap(self.d, self.root, visual.visual, AllocNone)
        attr = xlib.XSetWindowAttributes()
        attr.colormap = cmap
        attr.background_pixmap = 0
        attr.border_pixmap = 0
        attr.border_pixel = 0
        attr.event_mask = (StructureNotifyMask | EnterWindowMask | LeaveWindowMask | ExposureMask |
                           ButtonPressMask | ButtonReleaseMask | OwnerGrabButtonMask | KeyPressMask | KeyReleaseMask)
        attr_mask = (#  CWBackPixmap|
          CWColormap | CWBorderPixel | CWEventMask)
        self.window = xlib.XCreateWindow(self.d, self.root, x, y, w, h, 0,
          visual.depth, 1, visual.visual, attr_mask, byref(attr))
      else: # normal EGL created context
        self.window = xlib.XCreateSimpleWindow(self.d, self.root, x, y, w, h, 1, 0, 0)

      s = ctypes.create_string_buffer(b'WM_DELETE_WINDOW')
      self.WM_DELETE_WINDOW = ctypes.c_ulong(xlib.XInternAtom(self.d, s, 0))

      # set window title
      title = ctypes.c_char_p(self.window_title)
      title_length = ctypes.c_int(len(self.window_title))
      wm_name_atom = ctypes.c_ulong(xlib.XInternAtom(self.d, ctypes.create_string_buffer(b'WM_NAME'), 0))
      string_atom = ctypes.c_ulong(xlib.XInternAtom(self.d, ctypes.create_string_buffer(b'STRING'), 0))
      xlib.XChangeProperty(self.d, self.window, wm_name_atom, string_atom, 8, xlib.PropModeReplace, title, title_length)

      if (w == self.width and h == self.height) or (self.display_config & DISPLAY_CONFIG_FULLSCREEN):
        # set full-screen. Messy c function calls!
        wm_state = ctypes.c_ulong(xlib.XInternAtom(self.d, b'_NET_WM_STATE', 0))
        fullscreen = ctypes.c_ulong(xlib.XInternAtom(self.d, b'_NET_WM_STATE_FULLSCREEN', 0))  
        fullscreen = ctypes.cast(ctypes.pointer(fullscreen), ctypes.c_char_p)
        XA_ATOM = 4
        xlib.XChangeProperty(self.d, self.window, wm_state, XA_ATOM, 32, xlib.PropModeReplace, fullscreen, 1)

      self.width, self.height = w, h

      if self.display_config & DISPLAY_CONFIG_HIDE_CURSOR:
        black = xlib.XColor()
        black.red = 0
        black.green = 0
        black.blue = 0
        noData = ctypes.c_char_p(bytes([0, 0, 0, 0, 0, 0, 0, 0]))
        bitmapNoData = xlib.XCreateBitmapFromData(self.d, self.window, noData, 8, 8)
        invisibleCursor = xlib.XCreatePixmapCursor(self.d, bitmapNoData, bitmapNoData, 
                                                black, black, 0, 0)
        xlib.XDefineCursor(self.d, self.window, invisibleCursor)

      #TODO add functions to xlib for these window manager libx11 functions
      #self.window.set_wm_name('pi3d xlib window')
      #self.window.set_wm_icon_name('pi3d')
      #self.window.set_wm_class('draw', 'XlibExample')

      xlib.XSetWMProtocols(self.d, self.window, self.WM_DELETE_WINDOW, 1)
      #self.window.set_wm_hints(flags = Xutil.StateHint,
      #                         initial_state = Xutil.NormalState)

      #self.window.set_wm_normal_hints(flags = (Xutil.PPosition | Xutil.PSize
      #                                         | Xutil.PMinSize),
      #                                min_width = 20,
      #                                min_height = 20)

      xlib.XSelectInput(self.d, self.window, KeyPressMask | KeyReleaseMask | ResizeRedirectMask)
      xlib.XMapWindow(self.d, self.window)
      #xlib.XMoveWindow(self.d, self.window, x, y) #TODO this has to happen later. Works after rendering first frame. Check when
      if self.use_glx:
        dummy = c_int()
        if not glx.glXQueryExtension(self.d, byref(dummy), byref(dummy)):
          print("OpenGL not supported by X server\n")
        dummy_glx_context = ctypes.cast(0, glx.GLXContext)
        self.render_context = glx.glXCreateNewContext(self.d, fbconfig, glx.GLX_RGBA_TYPE, dummy_glx_context, True)
        if not self.render_context:
          print("Failed to create a GL context\n")
        if not glx.glXMakeContextCurrent(self.d, self.window, self.window, self.render_context):
          print("glXMakeCurrent failed for window\n")
      else:
        self.surface = openegl.eglCreateWindowSurface(self.display, self.config, self.window, 0)

    if not self.use_glx:
      assert self.surface != EGL_NO_SURFACE and self.surface is not None
      r = openegl.eglMakeCurrent(self.display, self.surface, self.surface,
                                self.context)
      assert r

    #Create viewport
    opengles.glViewport(GLint(0), GLint(0), GLsizei(w), GLsizei(h))

  def resize(self, x=0, y=0, w=0, h=0, layer=0):
    # Destroy current surface and native window
    if self.use_glx:
      glx.glXSwapBuffers(self.d, self.window)
    else:
      openegl.eglSwapBuffers(self.display, self.surface)
    if PLATFORM == PLATFORM_PI:
      openegl.eglDestroySurface(self.display, self.surface)

      self.dispman_update = bcm.vc_dispmanx_update_start(0)
      bcm.vc_dispmanx_element_remove(self.dispman_update,
                                     self.dispman_element)
      bcm.vc_dispmanx_update_submit_sync(self.dispman_update)
      bcm.vc_dispmanx_display_close(self.dispman_display)

      #Now recreate the native window and surface
      self.create_surface(x, y, w, h, layer)
    elif PLATFORM == PLATFORM_ANDROID:
      pass #TODO something here
    elif X_WINDOW:
      xlib.XMoveResizeWindow(self.d, self.window, x, y, w, h)

  def change_layer(self, layer=0):
    if PLATFORM == PLATFORM_PI:
      self.dispman_update = bcm.vc_dispmanx_update_start(0)
      bcm.vc_dispmanx_element_change_layer(self.dispman_update,
                                     self.dispman_element, layer)
      bcm.vc_dispmanx_update_submit_sync(self.dispman_update)


  def destroy(self, display=None):
    if self.active:
      ###### brute force tidying experiment TODO find nicer way ########
      if display:

        func_list = [[opengles.glIsBuffer, opengles.glDeleteBuffers,
            display.vbufs_dict.update(display.ebufs_dict)], # merge two dictionaries with update()
            [opengles.glIsTexture, opengles.glDeleteTextures,
            display.textures_dict],
            [opengles.glIsProgram, opengles.glDeleteProgram, 0],
            [opengles.glIsShader, opengles.glDeleteShader, 0]]

        i_ct = (ctypes.c_int * 1)(0) #convoluted 0
        for fi, func in enumerate(func_list):
          streak_start = 0
          if func[2]: # list to work through
            for i in func[2]:
              if func[0](func[2][i][0]) == 1: #check if i exists as a name
                try:
                  func[1](1, byref(func[2][i][0]))
                except:
                  pass # TODO find why this might fail (maybe race condition)
          else: # just do sequential numbers
            for i in range(1, 10000): # name 0 not to be deleted
              if func[0](i) == 1: #check if i exists as a name
                if fi < 2: # buffers or textures needs number to delete
                  i_ct[0] = i # pass as pointer to array of uint
                  try:
                    func[1](1, byref(i_ct))
                  except:
                    pass # TODO not sure why this silently fails and prevents the rest of the tidy up
                else: # program and shader just one arg
                  try:
                    func[1](i)
                  except:
                    pass # TODO see above
                streak_start = i
              elif i > (streak_start + 100):
                break
      ##################################################################
      openegl.eglSwapBuffers(self.display, self.surface)
      openegl.eglMakeCurrent(self.display, EGL_NO_SURFACE, EGL_NO_SURFACE,
                             EGL_NO_CONTEXT)
      openegl.eglDestroySurface(self.display, self.surface)
      openegl.eglDestroyContext(self.display, self.context)
      openegl.eglTerminate(self.display)
      if PLATFORM == PLATFORM_PI:
        self.dispman_update = bcm.vc_dispmanx_update_start(0)
        bcm.vc_dispmanx_element_remove(self.dispman_update, self.dispman_element)
        bcm.vc_dispmanx_update_submit_sync(self.dispman_update)
        bcm.vc_dispmanx_display_close(self.dispman_display)

      self.active = False
      if pi3d.USE_PYGAME:
        import pygame
        pygame.display.quit()
      elif PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID:
        xlib.XCloseDisplay(self.d)

  def swap_buffers(self):
    #opengles.glFlush()
    #opengles.glFinish()
    if self.use_glx:
      glx.glXSwapBuffers(self.d, self.window)
    else:
      openegl.eglSwapBuffers(self.display, self.surface)
