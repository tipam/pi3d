import signal
import threading

from pi3d.util import Log

LOGGER = Log.logger(__name__)
MOUSE = None

class NativeMouse(threading.Thread):
  XSIGN = 1 << 4
  YSIGN = 1 << 5

  def __init__(self):
    super(NativeMouse, self).__init__()
    self.fd = open('/dev/input/mouse0', 'r')
    self.x = 800
    self.y = 400
    self.finished = False
    self.button = False
    self.running = False
    self.buffer = ''

  def start(self):
    if not self.running:
      self.running = True
      super(NativeMouse, self).start()

  def run(self):
    buffer = ''
    while self.running:
      self.check_event()

  def check_event(self, timeout=0):
    if len(self.buffer) >= 3:
      buttons = self.buffer[0]
      self.buffer = self.buffer[1:]
      if buttons & 8:
        dx, dy = map(ord, self.buffer[0:2])
        self.buffer = self.buffer[2:]
        if buttons & 3:
          self.button = True
          # break  # Stop if mouse button pressed!
        if buttons & Mouse.XSIGN:
          dx -= 256
        if buttons & Mouse.YSIGN:
          dy -= 256

        self.x += dx
        self.y += dy
        return True

    else:
      if timeout:
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(timeout)

      self.buffer += self.fd.read()
      if timeout:
        signal.alarm(0)

      return False

  def stop(self):
    self.running = False

  def signal_handler(self):
    self.stop()


def Mouse():
  global MOUSE
  if not MOUSE:
    MOUSE = NativeMouse()
  return MOUSE

