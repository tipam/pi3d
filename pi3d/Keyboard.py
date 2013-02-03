import curses, termios, fcntl, sys, os

USE_CURSES = True

"""Non-blocking keyboard which requires curses and only works on the current
terminal window or session.
"""
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
    try:
      self.close()
    except:
      pass


"""Blocking keyboard which doesn't require curses and gets any keyboard inputs
regardless of which window is in front.
From http://stackoverflow.com/a/6599441/43839
"""
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
      return ord(sys.stdin.read())
    except KeyboardInterrupt:
      return 0

  def close(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.attrs_save)
    fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save)

  def __del__(self):
    try:
      self.close()
    except:
      pass


def Keyboard(use_curses=USE_CURSES):
  return CursesKeyboard() if use_curses else SysKeyboard()

