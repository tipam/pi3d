from __future__ import absolute_import, division, print_function, unicode_literals

from ctypes import c_float, byref

import time
import threading
import traceback
import platform
import logging

import pi3d
from pi3d.util.DisplayOpenGL import DisplayOpenGL
from pi3d.constants import (openegl, opengles, PLATFORM, PLATFORM_ANDROID,
          PLATFORM_PI, PLATFORM_WINDOWS, STARTUP_MESSAGE, DISPLAY_CONFIG_DEFAULT,
          GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GLclampf, GLboolean, GLsizei)
if PLATFORM == PLATFORM_WINDOWS:
  import pygame
elif PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID:
  from pyxlib.x import KeyPress, KeyRelease, ClientMessage, ResizeRequest
  from pyxlib import xlib

LOGGER = logging.getLogger(__name__)

ALLOW_MULTIPLE_DISPLAYS = False
RAISE_EXCEPTIONS = True
MARK_CAMERA_CLEAN_ON_EACH_LOOP = True

DEFAULT_FOV = 45.0
DEFAULT_DEPTH = 24
DEFAULT_SAMPLES = 0
DEFAULT_NEAR = 1.0
DEFAULT_FAR = 1000.0
WIDTH = 0
HEIGHT = 0

if PLATFORM == PLATFORM_ANDROID:
  from kivy.app import App
  from kivy.uix.floatlayout import FloatLayout
  from kivy.clock import Clock

  class Pi3dScreen(FloatLayout):
    def __init__(self, *args, **kwargs):
      super(Pi3dScreen, self).__init__()
      self.TAP_TM = 0.15
      self.TAP_GAP = 1.0
      self.moved = False
      self.tapped = False
      self.double_tapped = False
      self.last_down = 0.0
      self.last_last_down = 0.0
      self.touch = None
      self.previous_touch = None

    def update(self, dt):
      pass

    def on_touch_down(self, touch):
      touch.ud['down'] = True #needed for keeping track of 'other' touch location
      self.last_last_down = self.last_down
      self.last_down = time.time()
      self.previous_touch = self.touch
      self.touch = touch

    def on_touch_move(self, touch):
      self.moved = True
      self.touch = touch

    def on_touch_up(self, touch):
      tm_now = time.time()
      if (tm_now - self.last_down) < self.TAP_TM: #this was a tap
        if (tm_now - self.last_last_down) < self.TAP_GAP : #and near enough to be double
          self.double_tapped = True
          self.tapped = False
        else:
          self.tapped = True
          self.double_tapped = False
      touch.ud['down'] = False

  class Pi3dApp(App):
    frames_per_second = 60.0
    def set_loop(self, loop_function):
      self.loop_function = loop_function

    def build(self):
      self.screen = Pi3dScreen()
      Clock.schedule_interval(self.loop_function, 1.0 / self.frames_per_second)
      return self.screen

class Display(object):
  """This is the central control object of the pi3d system and an instance
  must be created before some of the other class methods are called.
  """
  INSTANCE = None
  """The current unique instance of Display."""

  def __init__(self, tkwin=None, use_pygame=False):
    """
    Constructs a raw Display.  Use pi3d.Display.create to create an initialized
    Display.

    *tkwin*
      An optional Tk window.
    *use_pygame*
      Flag to opt for pygame

    """
    if Display.INSTANCE is not None:
      assert ALLOW_MULTIPLE_DISPLAYS
      LOGGER.warning('A second instance of Display was created')
    else:
      Display.INSTANCE = self

    self.tkwin = tkwin
    if PLATFORM == PLATFORM_PI:
      use_pygame = False
    elif use_pygame or PLATFORM == PLATFORM_WINDOWS:
      try:
        import pygame
        use_pygame = True # for Windows
      except ImportError:
        LOGGER.warning('Do you need to install pygame?')
        use_pygame = False

    pi3d.USE_PYGAME = use_pygame

    self.sprites = []
    self.sprites_to_load = set()
    self.sprites_to_unload = set()

    self.tidy_needed = False
    self.textures_dict = {}
    self.vbufs_dict = {}
    self.ebufs_dict = {}
    self.last_shader = None
    self.last_textures = [None for _ in range(8)] # 8 is max no. texture2D on broadcom GPU
    self.external_mouse = None
    self.offscreen_tex = False # used in Buffer.draw() to force reload of textures

    if (PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID and
        not pi3d.USE_PYGAME):
      self.event_list = []
      self.ev = xlib.XEvent()
    elif PLATFORM == PLATFORM_ANDROID:
      self.android = Pi3dApp()

    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height
    self.first_time = True
    self.is_running = True
    self.lock = threading.RLock()
    self.was_resized = False

    LOGGER.debug(STARTUP_MESSAGE)

  def loop_running(self):
    """*loop_running* is the main event loop for the Display.

    Most pi3d code will look something like this::

      DISPLAY = Display.create()

      # Initialize objects and variables here.
      # ...

      while DISPLAY.loop_running():
        # Update the frame, using DISPLAY.time for the current time.
        # ...

        # Check for quit, then call DISPLAY.stop.
        if some_quit_condition():
          DISPLAY.stop()

    ``Display.loop_running()`` **must** be called on the main Python thread,
    or else white screens and program crashes are likely.

    The Display loop can run in two different modes - *free* or *framed*.

    If ``DISPLAY.frames_per_second`` is empty or 0 then the loop runs *free* - when
    it finishes one frame, it immediately starts working on the next frame.

    If ``Display.frames_per_second`` is a positive number then the Display is
    *framed* - when the Display finishes one frame before the next frame_time,
    it waits till the next frame starts.

    A free Display gives the highest frame rate, but it will also consume more
    CPU, to the detriment of other threads or other programs.  There is also
    the significant drawback that the framerate will fluctuate as the numbers of
    CPU cycles consumed per loop, resulting in jerky motion and animations.

    A framed Display has a consistent if smaller number of frames, and also
    allows for potentially much smoother motion and animation.  The ability to
    throttle down the number of frames to conserve CPU cycles is essential
    for programs with other important threads like audio.

    ``Display.frames_per_second`` can be set at construction in
    ``Display.create`` or changed on-the-fly during the execution of the
    program.  If ``Display.frames_per_second`` is set too high, the Display
    doesn't attempt to "catch up" but simply runs freely.

    """
    if self.is_running:
      if self.first_time:
        self.time = time.time()
        self.first_time = False
      else:
        self._loop_end()  # Finish the previous loop.
      self._loop_begin()
    else:
      self._loop_end()
      self.destroy()

    return self.is_running

  def resize(self, x=0, y=0, w=0, h=0):
    """Reshape the window with the given coordinates."""
    if w <= 0:
      w = self.max_width
    if h <= 0:
      h = self.max_height
    self.width = w
    self.height = h

    self.left = x
    self.top = y
    self.right = x + w
    self.bottom = y + h
    self.opengl.resize(x, y, w, h, self.layer)
    self.was_resized = True

  def change_layer(self, layer=0):
    self.layer = layer
    self.opengl.change_layer(layer)

  def add_sprites(self, *sprites):
    """Add one or more sprites to this Display."""
    with self.lock:
      self.sprites_to_load.update(sprites)

  def remove_sprites(self, *sprites):
    """Remove one or more sprites from this Display."""
    with self.lock:
      self.sprites_to_unload.update(sprites)

  def stop(self):
    """Stop the Display."""
    self.is_running = False

  def destroy(self):
    """Destroy the current Display and reset Display.INSTANCE."""
    self._tidy()
    self.stop()
    try:
      self.opengl.destroy(self)
    except:
      pass
    if self.external_mouse:
      try:
        self.external_mouse.stop()
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
    Display.INSTANCE = None
    if pi3d.USE_PYGAME:
      try:
        import pygame # NB seems to be needed on some setups (64 bit anaconda windows!)
        pygame.quit()
      except:
        pass

  def clear(self):
    """Clear the Display."""
    # opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
    opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  def set_background(self, r, g, b, alpha):
    """Set the Display background. **NB the actual drawing of the background
    happens during the rendering of the framebuffer by the shader so if no
    draw() is done by anything during each Display loop the screen will
    remain black** If you want to see just the background you will have to
    draw() something out of view (i.e. behind) the Camera.

    *r, g, b*
      Color values for the display
    *alpha*
      Opacity of the color.  An alpha of 0 means a transparent background,
      an alpha of 1 means full opaque.
    """
    if alpha < 1.0 and (not self.opengl.use_glx) and (not PLATFORM == PLATFORM_PI):
      LOGGER.warning("create Display with (...use_glx=True) for transparent background on x11 window. libGLX needs to be available")
    opengles.glClearColor(GLclampf(r), GLclampf(g), GLclampf(b), GLclampf(alpha))
    opengles.glColorMask(GLboolean(1), GLboolean(1), GLboolean(1), GLboolean(alpha < 1.0))
    # Switches off alpha blending with desktop (is there a bug in the driver?)

  def mouse_position(self):
    """The current mouse position as a tuple."""
    # TODO: add: Now deprecated in favor of pi3d.events
    if self.mouse:
      return self.mouse.position()
    elif self.tkwin:
      return self.tkwin.winfo_pointerxy()
    else:
      return -1, -1

  def _loop_begin(self):
    # TODO(rec):  check if the window was resized and resize it, removing
    # code from MegaStation to here.
    if pi3d.USE_PYGAME:
      import pygame # although done in __init__ ...python namespaces aarg!!!
      if pygame.event.get(pygame.QUIT):
        self.destroy()
    elif PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID:
      n = xlib.XEventsQueued(self.opengl.d, xlib.QueuedAfterFlush)
      for _ in range(n):
          xlib.XNextEvent(self.opengl.d, self.ev)
          if self.ev.type == KeyPress or self.ev.type == KeyRelease:
              self.event_list.append(self.ev)
          elif self.ev.type == ClientMessage:
            if (self.ev.xclient.data.l[0] == self.opengl.WM_DELETE_WINDOW.value):
              self.destroy()
          elif self.ev.type == ResizeRequest:
            (self.width, self.height) = (self.ev.xresizerequest.width,
                                         self.ev.xresizerequest.height)
            opengles.glViewport(0, 0, self.width, self.height)
            self.was_resized = True
    self.clear()
    with self.lock:
      self.sprites_to_load, to_load = set(), self.sprites_to_load
      self.sprites.extend(to_load)
    self._for_each_sprite(lambda s: s.load_opengl(), to_load)

    if MARK_CAMERA_CLEAN_ON_EACH_LOOP:
      from pi3d.Camera import Camera
      #camera = Camera.instance()
      #if camera is not None:
      #  camera.was_moved = False
      cameras = Camera.all_instances()
      if cameras is not None:
        for camera in cameras:
          camera.was_moved = False

    if self.tidy_needed:
      self._tidy()

  def _tidy(self):
    to_del = []
    for i in self.textures_dict:
      tex = self.textures_dict[i]
      if tex[1] == 1:
        opengles.glDeleteTextures(GLsizei(1), byref(tex[0]))
        to_del.append(i)
    for i in to_del:
      del self.textures_dict[i]
    to_del = []
    for i in self.vbufs_dict:
      vbuf = self.vbufs_dict[i]
      if vbuf[1] == 1:
        opengles.glDeleteBuffers(GLsizei(1), byref(vbuf[0]))
        to_del.append(i)
    for i in to_del:
      del self.vbufs_dict[i]
    to_del = []
    for i in self.ebufs_dict:
      ebuf = self.ebufs_dict[i]
      if ebuf[1] == 1:
        opengles.glDeleteBuffers(GLsizei(1), byref(ebuf[0]))
        to_del.append(i)
    for i in to_del:
      del self.ebufs_dict[i]
    self.tidy_needed = False

  def _loop_end(self):
    if pi3d.USE_PYGAME:
      import pygame
      pygame.event.clear()
      
    with self.lock:
      self.sprites_to_unload, to_unload = set(), self.sprites_to_unload
      if to_unload:
        self.sprites = [s for s in self.sprites if s not in to_unload]

    t = time.time()
    self._for_each_sprite(lambda s: s.repaint(t))

    self.swap_buffers()

    for sprite in to_unload:
      sprite.unload_opengl()

    if self.frames_per_second:
      delta = 1.0 / self.frames_per_second - (time.time() - self.time)
      if delta > 0:
        time.sleep(delta)

    self.time = time.time()

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

  def __del__(self):
    try:
      self.destroy()
    except:
      pass # often something has already been deleted leading to various None objects

  def swap_buffers(self):
    self.opengl.swap_buffers()


def create(x=None, y=None, w=None, h=None, near=None, far=None,
           fov=DEFAULT_FOV, depth=DEFAULT_DEPTH, background=None,
           tk=False, window_title='', window_parent=None, mouse=False,
           frames_per_second=None, samples=DEFAULT_SAMPLES, use_pygame=False, layer=0, 
           display_config=DISPLAY_CONFIG_DEFAULT, use_glx=False):
  """
  Creates a pi3d Display.

  *x*
    Left x coordinate of the display.  If None, defaults to the x coordinate of
    the tkwindow parent, if any.
  *y*
    Top y coordinate of the display.  If None, defaults to the y coordinate of
    the tkwindow parent, if any.
  *w*
    Width of the display.  If None, full the width of the screen.
  *h*
    Height of the display.  If None, full the height of the screen.
  *near*
    This will be used for the default instance of Camera *near* plane
  *far*
    This will be used for the default instance of Camera *far* plane
  *fov*
    Used to define the Camera lens field of view
  *depth*
    The bit depth of the display - must be 8, 16 or 24.
  *background*
    r,g,b,alpha (opacity)
  *tk*
    Do we use the tk windowing system?
  *window_title*
    A window title for tk windows only.
  *window_parent*
    An optional tk parent window.
  *mouse*
    Automatically create a Mouse.
  *frames_per_second*
    Maximum frames per second to render (None means "free running").
  *samples*
    EGL_SAMPLES default 0, set to 4 for improved anti-aliasing
  *use_pygame*
    To use pygame for display surface, mouse and keyboard - as per windows
    This almost certainly would conflict if attempting to use in combination
    with tk=True. Default False
  *layer*
    display layer height - used by dispmanx on Raspberry Pi only. -128 will move the
    pi3d window behind the X11 desktop
  *display_config*
    Configuration of display - See pi3d.constants for DISPLAY_CONFIG options
  """
  if tk: #NB this happens before Display created so use_pygame will not work on linux
    if PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID:
      #just use python-xlib same as non-tk but need dummy behaviour
      from pi3d.Keyboard import Keyboard
      class DummyTkWin(object):
        def __init__(self):
          self.tkKeyboard = Keyboard()
          self.ev = ""
          self.key = ""
          self.winx, self.winy = 0, 0
          self.width, self.height = 1920, 1180
          self.event_list = []

        def update(self):
          if PLATFORM == PLATFORM_WINDOWS or pi3d.USE_PYGAME: #uses pygame UI
            k = self.tkKeyboard.read()
            if k == -1:
              self.key = ""
              self.ev = ""
            else:
              if k == 27:
                self.key = "Escape"
              else:
                self.key = chr(k)
              self.ev = "key"
          else:
            self.key = self.tkKeyboard.read_code()
            if self.key == "":
              self.ev = ""
            else:
              self.ev = "key"

      tkwin = DummyTkWin()
      x = x or 0
      y = y or 0

    else:
      from pi3d.util import TkWin
      if not (w and h):
        # TODO: how do we do full-screen in tk?
        #LOGGER.error('Can't compute default window size when using tk')
        #raise Exception
        # ... just force full screen - TK will automatically fit itself into the screen
        w = 1920
        h = 1180
      if background is not None:
        bg_i = [int(i * 255) for i in background]
        bg = '#{:02X}{:02X}{:02X}'.format(bg_i[0], bg_i[1], bg_i[2])
      else:
        bg = '#000000'
      tkwin = TkWin.TkWin(window_parent, window_title, w, h, bg)
      tkwin.update()
      w = tkwin.winfo_width()
      h = tkwin.winfo_height()
      if x is None:
        x = tkwin.winx
      if y is None:
        y = tkwin.winy

  else:
    tkwin = None
    x = x or 0
    y = y or 0

  display = Display(tkwin, use_pygame)
  if (w or 0) <= 0:
    w = display.max_width - 2 * x
    if w <= 0:
      w = display.max_width
  if (h or 0) <= 0:
    h = display.max_height - 2 * y
    if h <= 0:
      h = display.max_height

  LOGGER.debug('Display size is w=%d, h=%d', w, h)

  display.frames_per_second = frames_per_second or 0

  if near is None:
    near = DEFAULT_NEAR
  if far is None:
    far = DEFAULT_FAR

  display.width = w
  display.height = h
  display.near = near
  display.far = far
  display.fov = fov

  display.left = x
  display.top = y
  display.right = x + w
  display.bottom = y + h
  display.layer = layer

  display.opengl.create_display(x, y, w, h, depth=depth, samples=samples, layer=layer,
                            display_config=display_config, window_title=window_title, use_glx=use_glx)
  if PLATFORM == PLATFORM_ANDROID:
    display.width = display.right = display.max_width = display.opengl.width #not available until after create_display
    display.height = display.bottom = display.max_height = display.opengl.height
    display.top = display.bottom = 0
    if frames_per_second:
      display.android.frames_per_second = frames_per_second
      display.frames_per_second = 0 #to avoid clash between two systems!

  display.mouse = None

  if mouse:
    from pi3d.Mouse import Mouse
    display.mouse = Mouse(width=w, height=h, restrict=False)
    display.mouse.start()

  if background is not None:
    display.set_background(*background)

  return display
