from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib, pi3d

if pi3d.USE_PYGAME:
  import pygame
elif pi3d.PLATFORM != pi3d.PLATFORM_PI and pi3d.PLATFORM != pi3d.PLATFORM_ANDROID:
  from pyxlib import x

USE_CURSES = True

"""Non-blocking keyboard which requires curses and only works on the current
terminal window or session.
"""
class CursesKeyboard(object):
  def __init__(self):
    import curses
    self.key = curses.initscr()
    curses.cbreak()
    curses.noecho()
    self.key.keypad(1)
    self.key.nodelay(1)

  def read(self):
    return self.key.getch()

  def read_code(self):
    c = self.key.getch()
    if c > -1:
      return chr(c)
    return ""

  def close(self):
    import curses
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
    import termios, fcntl, sys, os
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

  def read_code(self):
    return ""

  def close(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.attrs_save)
    fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save)

  def __del__(self):
    try:
      self.close()
    except:
      pass

"""Keyboard using x11 functionality
"""
class x11Keyboard(object):
  KEYBOARD = [[0, ""], [0, ""], [0, ""], [0, ""], [0, ""],
            [0, ""], [0, ""], [0, ""], [0, ""], [27, "Escape"],
            [49, "1"], [50, "2"], [51, "3"], [52, "4"], [53, "5"],
            [54, "6"], [55, "7"], [56, "8"], [57, "9"], [48, "0"],
            [45, "-"], [61, "="], [8, "BackSpace"], [9, "Tab"], [113, "q"],
            [119, "w"], [101, "e"], [114, "r"], [116, "t"], [121, "y"],
            [117, "u"], [105, "i"], [111, "o"], [112, "p"], [91, "["],
            [93, "]"], [13, "Return"], [0, "Control_L"], [97, "a"], [115, "s"],
            [100, "d"], [102, "f"], [103, "g"], [104, "h"], [106, "j"],
            [107, "k"], [108, "l"], [59, ";"], [39, "'"], [96, "`"],
            [0, "Shift_L"], [35, "#"], [122, "z"], [120, "x"], [99, "c"],
            [118, "v"], [98, "b"], [110, "n"], [109, "m"], [44, ","],
            [46, "."], [47, "/"], [0, "Shift_R"], [0, ""], [0, "Alt_L"],
            [32, "space"], [0, "Caps"], [145, "F1"], [146, "F2"], [147, "F3"],
            [148, "F4"], [149, "F5"], [150, "F6"], [151, "F7"], [152, "F8"],
            [153, "F9"], [154, "F10"], [0, "Num_Lock"], [0, ""], [0, ""],
            [0, ""], [0, ""], [0, ""], [0, ""], [0, ""],
            [0, ""], [0, ""], [0, ""], [0, ""], [0, ""],
            [0, ""], [0, ""], [0, ""], [0, ""], [92, "\\"],
            [155, "F11"], [156, "F12"], [0, ""], [0, ""], [0, ""],
            [0, ""], [0, ""], [0, ""], [0, ""], [13, "KP_Enter"],
            [0, "Control_R"], [0, ""], [0, ""], [0, "Alt_R"], [0, ""],
            [129, "Home"], [134, "Up"], [130, "Page_Up"], [136, "Left"], [137, "Right"],
            [132, "End"], [135, "Down"], [133, "Page_Down"], [128, "Insert"], [131, "DEL"]]

  def __init__(self):
    from pi3d.Display import Display
    self.display = Display.INSTANCE
    self.key_num = 0
    self.key_code = ""

  def _update_event(self):
    if self.display is None: #Because DummyTkWin Keyboard instance created before Display!
      from pi3d.Display import Display
      self.display = Display.INSTANCE
    while len(self.display.event_list) > 0:
      e = self.display.event_list.pop(0)
      if e.type == x.KeyPress and e.xkey.keycode < len(self.KEYBOARD):
        self.key_num = self.KEYBOARD[e.xkey.keycode][0]
        self.key_code = self.KEYBOARD[e.xkey.keycode][1]
        return True
    return False

  def read(self):
    if self._update_event():
      return self.key_num
    else:
      return -1

  def read_code(self):
    if self._update_event():
      return self.key_code
    else:
      return ""

  def close(self):
    pass

  def __del__(self):
    try:
      self.close()
    except:
      pass

"""Android keyboard - TODO all of this
"""
class AndroidKeyboard(object):
  def __init__(self):
    pass

  def read(self):
    return -1

  def read_code(self):
    return ""

  def close(self):
    pass

  def __del__(self):
    try:
      self.close()
    except:
      passwindows

"""Windows keyboard - uses pygame
"""
class PygameKeyboard(object):
  """ In this case KEYBOARD maps pygame codes to the X11 codes used above
  """
  KEYBOARD = {282:[145, "F1"], 283:[146, "F2"], 284:[147, "F3"],
            285:[148, "F4"], 286:[149, "F5"], 287:[150, "F6"], 288:[151, "F7"],
            289:[152, "F8"], 290:[153, "F9"], 291:[154, "F10"], 60:[92, "\\"],
            292:[155, "F11"], 293:[156, "F12"], 271:[13, "KP_Enter"],
            305:[0, "Control_R"], 306:[0, "Control_L"], 308:[0, "Alt_L"],
            307:[0, "Alt_R"], 278:[129, "Home"], 273:[134, "Up"],
            280:[130, "Page_Up"], 276:[136, "Left"], 275:[137, "Right"],
            279:[132, "End"], 274:[135, "Down"], 281:[133, "Page_Down"],
            277:[128, "Insert"], 127:[131, "DEL"], 304:[0,"Shift_L"],
            303:[0,"Shift_R"], 301:[0,"Caps"], 13:[0,"Return"], 8:[0,"BackSpace"]}
  def __init__(self):
    self.key_list = []
    import pygame
    pygame.init() # shoudn't matter re-doing this. Some demos have Keyboard before Display
    pygame.key.set_repeat(500, 25)
    self.key_num = 0
    self.key_code = ""

  def read(self):
    import pygame
    pygame.event.get(pygame.KEYUP) # discard these TODO use them in some way?
    self.key_list.extend(pygame.event.get(pygame.KEYDOWN))
    if len(self.key_list) > 0:
      key = self.key_list[0].key
      if key in self.KEYBOARD:
        self.key_code = self.KEYBOARD[key][1]
        key = self.KEYBOARD[key][0]
      elif key < 256:
        self.key_code = chr(key) # have to assume ascii code conversion will do
      else:
        self.key_code = ""
      self.key_list = self.key_list[1:]
      return key
    return -1

  def read_code(self):
    key = self.read()
    if key == -1:
      return ""
    else:
      return self.key_code

  def close(self):
    pass

  def __del__(self):
    try:
      self.close()
    except:
      pass


def Keyboard(use_curses=USE_CURSES):
  '''Wrapper for the various keyboards appropriate to the PLATFORM

  argument:

    *use_curses*
      default True, use CursesKeyboard on raspberry pi rather than
      SysKeyboard
  '''
  if pi3d.PLATFORM == pi3d.PLATFORM_ANDROID:
    return AndroidKeyboard()
  #elif PLATFORM == PLATFORM_WINDOWS:
  elif pi3d.USE_PYGAME:
    return PygameKeyboard()
  elif pi3d.PLATFORM != pi3d.PLATFORM_PI:
    return x11Keyboard()
  else:
    return CursesKeyboard() if use_curses else SysKeyboard()


@contextlib.contextmanager
def KeyboardContext(use_curses=USE_CURSES):
    """ Using a context manager alows curses to restore the terminal to its
    initial tidy state even if the program is quitted using Ctrl+c.
    Typical usage::

        with KeyboardContext() as keys:
          while DISPLAY.loop_running():
            sprite.draw()
            if keys.read() == 27:
              break
    """
    keyboard = Keyboard(use_curses=use_curses)
    yield keyboard
    keyboard.close()
