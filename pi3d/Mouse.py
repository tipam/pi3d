import signal
import threading

from pi3d.util import Log

LOGGER = Log.logger(__name__)

class Mouse(threading.Thread):
  XSIGN = 1 << 4
  YSIGN = 1 << 5

  def __init__(self, timeout=0):
    super(Mouse, self).__init__()
    self.timeout = timeout
    self.fd = open('/dev/input/mouse0', 'r')
    self.x = 800
    self.y = 400
    self.finished = False
    self.button = False
    self.running = False
    self.buffer = ''

  def start(self):
    if self.timeout:
      LOGGER.error("Can't use a timeout unless mouse is on main thread")
      assert self.timeout

    self.running = True
    super(Mouse, self).start()

  def run(self):
    buffer = ''
    while self.running:
      self.loop()

  def loop(self):
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
      if self.timeout:
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(self.timeout)

      self.buffer += self.fd.read()
      if self.timeout:
        signal.alarm(0)

      return False

  def stop(self):
    self.running = False

  def signal_handler(self):
    self.stop()
