import curses

class Key():
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

