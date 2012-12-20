import signal
import threading

class Mouse(threading.Thread):
  XSIGN = 1 << 4
  YSIGN = 1 << 5

  def __init__(self, timeout=1):
    super(Mouse, self).__init__()
    self.fd = open('/dev/input/mouse0', 'r')
    self.x = 800
    self.y = 400
    self.finished = False
    self.button = False
    self.running = False

  def start(self):
    self.running = True
    super(Mouse, self).start()

  def run(self):
    buffer = ''
    while self.running:
      if len(buffer) >= 3:
        buttons = buffer[0]
        buffer = buffer[1:]
        if buttons & 8:
          dx, dy = map(ord, buffer[0:2])
          buffer = buffer[2:]
          if buttons & 3:
            self.button = True
            # break  # Stop if mouse button pressed!
          if buttons & Mouse.XSIGN:
            dx -= 256
          if buttons & Mouse.YSIGN:
            dy -= 256

          self.x += dx
          self.y += dy
      else:
        # No way to avoid blocking - we can't use signals if we aren't in the
        # main thread. :-(
        buffer += self.fd.read()

  def stop(self):
    self.running = False

