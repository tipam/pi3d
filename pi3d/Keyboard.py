import curses

from pi3d.util import Screenshot

class Keyboard(object):
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

def closer(loop):
  """A decorator that checks the keyboard to see if you've quit."""
  mykeys = Keyboard()
  def f():
    if k == 27:
      mykeys.close()
      return True
    return loop()
  return f

def screenshot(file):
  """A decorator that checks. the keyboard to see if you've quit and also takes
  screenshots."""
  def f(loop):
    mykeys = Keyboard()
    def inner():
      k = mykeys.read()
      if k == 112:
        screenshot(file)
      if k == 27:
        mykeys.close()
        return True
      return loop()
    return inner

  return f
