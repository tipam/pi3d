import curses, termios, fcntl, sys, os

USE_CURSES = True

class CursesKeyboard(object):
  def __init__(self):
    self.key = curses.initscr()
    curses.cbreak()
    curses.noecho()
    self.key.keypad(1)
    self.key.nodelay(1)

  def read(self):
    return self.key.getch()

  def close(self):
    curses.nocbreak()
    self.key.keypad(0)
    curses.echo()
    curses.endwin()

  def __del__(self):
    self.close()

# From http://stackoverflow.com/a/6599441/43839
class SysKeyboard(object):
  def __init__(self):
    self.fd = sys.stdin.fileno()
    # save old state
    self.flags_save = fcntl.fcntl(self.fd, fcntl.F_GETFL)
    self.attrs_save = termios.tcgetattr(self.fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(self.attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(self.fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save & ~os.O_NONBLOCK)

  def read(self):
    try:
      return ord(sys.stdin.read(1))
    except KeyboardInterrupt:
      return 0

  def close(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.attrs_save)
    fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save)

  def __del__(self):
    self.close()


def Keyboard(use_curses=USE_CURSES):
  return CursesKeyboard() if use_curses else SysKeyboard()

# DEPRECATED.
def closer(loop):
  """A decorator that checks the keyboard to see if you've quit."""
  mykeys = Keyboard()
  def f():
    if k == 27:
      mykeys.close()
      return True
    return loop()
  return f

# DEPRECATED.
def screenshot(file):
  """A decorator that checks. the keyboard to see if you've quit and also takes
  screenshots."""
  def f(loop):
    from pi3d.util import Screenshot
    mykeys = Keyboard()
    def inner():
      k = mykeys.read()
      if k == 112:
        Screenshot.screenshot(file)
      if k == 27:
        mykeys.close()
        return True
      return loop()
    return inner

  return f
