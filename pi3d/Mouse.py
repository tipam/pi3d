from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import six

from pi3d.util import Log

LOGGER = Log.logger(__name__)

class _Mouse(threading.Thread):
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

  def __init__(self, mouse='mice', restrict=True, width=1920, height=1200):
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
    super(_Mouse, self).__init__()
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
      super(_Mouse, self).start()

  def run(self):
    while self.running:
      self._check_event()
    self.fd.close()

  def position(self):
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
      if buttons & _Mouse.HEADER:
        dx, dy = map(ord, self.buffr[0:2])
        self.buffr = self.buffr[2:]
        self.button = buttons & _Mouse.BUTTONS
        if buttons & _Mouse.XSIGN:
          dx -= 256
        if buttons & _Mouse.YSIGN:
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

def Mouse(*args, **kwds):
  if not _Mouse.INSTANCE:
    _Mouse.INSTANCE = _Mouse(*args, **kwds)
  return _Mouse.INSTANCE
