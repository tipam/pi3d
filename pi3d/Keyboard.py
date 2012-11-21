import curses

class Keyboard():
  def __init__(self):
    self.key = curses.initscr()
    curses.cbreak()
    curses.noecho()
    self.key.keypad(1)
    self.key.nodelay(1)

  def read(self):
    return (self.key.getch())

  def close(self):
    curses.nocbreak()
    self.key.keypad(0)
    curses.echo()
    curses.endwin()


def make_closer(screenshot=''):
  mykeys = Keyboard()
  def closer(display_loop):
    k = mykeys.read()
    if k == 112 and screenshot:
      display_loop.display.screenshot(screenshot)
    if k == 27:
      mykeys.close()
      return True

  return closer
