import sys

from pi3d import Keyboard

USE_CURSES = len(sys.argv) == 1 or sys.argv[1] == 'yes' or sys.argv[1] == 'true'

if USE_CURSES:
  print 'Using curses keyboard'
else:
  print 'Using system keyboard'

keyboard = Keyboard.Keyboard(use_curses=USE_CURSES)

while True:
  ch = keyboard.read()
  if ch > 0:
    print(ch, chr(ch))
    if ch == 17:
      break
