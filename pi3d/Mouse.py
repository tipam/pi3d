from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import six
import ctypes

from pi3d.constants import PLATFORM, PLATFORM_ANDROID, PLATFORM_PI, PLATFORM_WINDOWS
if PLATFORM == PLATFORM_WINDOWS:
  import pygame
elif PLATFORM != PLATFORM_PI and PLATFORM != PLATFORM_ANDROID:
  from pyxlib import xlib
  from pyxlib.x import *

from pi3d.util import Log

LOGGER = Log.logger(__name__)

class _nixMouse(threading.Thread):
  """holds Mouse object, see also (the preferred) events methods"""
  BUTTON_1 = 1 << 1
  BUTTON_2 = 1 << 2
  LEFT_BUTTON = 9 # 1001
  RIGHT_BUTTON = 10 # 1010
  MIDDLE_BUTTON = 12 # 1100
  BUTTON_UP = 8 # 1000
  BUTTONS = BUTTON_1 & BUTTON_2
  HEADER = 1 << 3
  XSIGN = 1 << 4
  YSIGN = 1 << 5
  INSTANCE = None

  def __init__(self, mouse='mice', restrict=True, width=1920, height=1200, use_x=False):
    """
    Arguments:
      *mouse*
        /dev/input/ device name
      *restrict*
        stops or allows the mouse x and y values to carry on going beyond:
      *width*
        mouse x limit
      *height*
        mouse y limit
    """
    super(_nixMouse, self).__init__()
    self.fd = open('/dev/input/' + mouse, 'rb')
    self.running = False
    self.buffr = '' if six.PY3 else b''
    self.lock = threading.RLock()
    self.width = width
    self.height = height
    self.restrict = restrict

    #create a pointer to this so Display.destroy can stop the thread
    from pi3d.Display import Display
    Display.INSTANCE.external_mouse = self

    self.use_x = False
    if use_x: # version as argument to __init__
      if PLATFORM != PLATFORM_ANDROID and PLATFORM != PLATFORM_PI:
        self.d = Display.INSTANCE.opengl.d
        self.window = Display.INSTANCE.opengl.window
        self.root = ctypes.c_ulong(0)
        self.child = ctypes.c_ulong(0)
        self.x = ctypes.c_int(0)
        self.y = ctypes.c_int(0)
        self.rootx = ctypes.c_int(0)
        self.rooty = ctypes.c_int(0)
        self.mask = ctypes.c_uint(0)
        self.use_x = True

    self.daemon = True # to kill app rather than waiting for mouse event
    self.reset()

  def reset(self):
    with self.lock:
      self._x = self._y = self._dx = self._dy = 0
    self.button = False
    self._buttons = 0

  def start(self):
    if not self.running:
      self.running = True
      super(_nixMouse, self).start()

  def run(self):
    while self.running:
      self._check_event()
    self.fd.close()

  def position(self):
    if self.use_x:
      xlib.XQueryPointer(self.d, self.window,
                        ctypes.byref(self.root), ctypes.byref(self.child),
                        ctypes.byref(self.rootx), ctypes.byref(self.rooty),
                        ctypes.byref(self.x),ctypes.byref(self.y),
                        self.mask)
      return self.x.value, self.y.value
    else:
      with self.lock:
        return self._x, self._y

  def velocity(self):
    with self.lock:
      return self._dx, self._dy

  def button_status(self):
    '''return the button status - use events system for capturing button
    events more scientifically.
    in _check_event self.buffr returns the following binary:
    L-button 00001001 00000000 00000000
    R-button 00001010 00000000 00000000
    M-button 00001100 00000000 00000000
    buttonUp 00001000 00000000 00000000
    '''
    with self.lock:
      return self._buttons

  def _check_event(self):
    if len(self.buffr) >= 3:
      buttons = [ord(c) for c in self.buffr]
      if buttons[1] == 0 and buttons[2] == 0:
        self._buttons = buttons[0]
      else:
        self._buttons = 0
      buttons = buttons[0]
      self.buffr = self.buffr[1:]
      if (buttons & _nixMouse.HEADER) > 0:
        dx, dy = map(ord, self.buffr[0:2])
        self.buffr = self.buffr[2:]
        self.button = buttons & _nixMouse.BUTTONS
        if (buttons & _nixMouse.XSIGN) > 0:
          dx -= 256
        if (buttons & _nixMouse.YSIGN) > 0:
          dy -= 256

        x = self._x + dx
        y = self._y + dy
        if self.restrict:
          x = min(max(x, 0), self.width - 1)
          y = min(max(y, 0), self.height - 1)

        with self.lock:
          self._x, self._y, self._dx, self._dy = x, y, dx, dy

    else:
      try:
        strn = self.fd.read(3).decode("latin-1")
        self.buffr += strn
      except Exception as e:
        print("exception is: {}".format(e))
        self.stop()
        return

  def stop(self):
    self.running = False

class _winMouse(object):
  """holds Mouse object, see also (the preferred) events methods"""
  BUTTON_1 = 1 << 1
  BUTTON_2 = 1 << 2
  LEFT_BUTTON = 9 # 1001
  RIGHT_BUTTON = 10 # 1010
  MIDDLE_BUTTON = 12 # 1100
  BUTTON_UP = 8 # 1000
  BUTTON_MAP = {1:LEFT_BUTTON, 2:MIDDLE_BUTTON, 3:RIGHT_BUTTON}
  BUTTONS = BUTTON_1 & BUTTON_2
  HEADER = 1 << 3
  XSIGN = 1 << 4
  YSIGN = 1 << 5
  INSTANCE = None

  def __init__(self, restrict=True):
    """
    Arguments:
      *mouse*
        /dev/input/ device name
      *restrict*
        stops or allows the mouse x and y values to carry on going beyond:
      *width*
        mouse x limit
      *height*
        mouse y limit
    """
    self._x = self._y = self._dx = self._dy = 0
    from pi3d.Display import Display
    self.centre = (Display.INSTANCE.width / 2, Display.INSTANCE.height / 2)
    self.restrict = restrict
    if not self.restrict:
      pygame.mouse.set_pos(self.centre)
      pygame.mouse.set_visible(False)

  def reset(self):
    pass
    
  def start(self):
    pass

  def run(self):
    pass

  def _check_event(self):
    pos_list = pygame.event.get(pygame.MOUSEMOTION)
    if len(pos_list) > 0:
      x, y = pos_list[-1].pos # discard all but the last position
      if self.restrict:
        self._dx = x - self._x
        self._dy = -y - self._y # swap to +ve upwards
        self._x = x
        self._y = -y
      else:
        self._dx = x - self.centre[0]
        self._dy = self.centre[1] - y # swap to +ve upwards
        self._x += self._dx
        self._y += self._dy
        pygame.mouse.set_pos(self.centre)
    but_list = pygame.event.get(pygame.MOUSEBUTTONDOWN)
    if len(but_list) > 0:
      self._buttons = BUTTON_MAP[but_list[-1].button] # discard all but last button
    else:  
      but_list = pygame.event.get(pygame.MOUSEBUTTONUP)
      if len(but_list) > 0:
        self._buttons = BUTTON_UP

  def position(self):
    self._check_event()
    return self._x, self._y

  def velocity(self):
    self._check_event()
    return self._dx, self._dy
    
  def button_status(self):
    return self._buttons

  def stop(self):
    pass

def Mouse(*args, **kwds):
  if PLATFORM == PLATFORM_WINDOWS:
    if not _winMouse.INSTANCE:
      _winMouse.INSTANCE = _winMouse(*args, **kwds)
    return _winMouse.INSTANCE
  else:
    if not _nixMouse.INSTANCE:
      _nixMouse.INSTANCE = _nixMouse(*args, **kwds)
    return _nixMouse.INSTANCE
