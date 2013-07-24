#from pi3d.Display import Display
from pyxlib import x


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
            
class Keyboard(object):
  def __init__(self, use_curses=None):
    from pi3d.Display import Display
    self.display = Display.INSTANCE
    self.key_num = 0
    self.key_code = ""

  def _update_event(self):
    if not self.display: #Because DummyTkWin Keyboard instance created before Display!
      from pi3d.Display import Display
      self.display = Display.INSTANCE
    n = len(self.display.event_list)
    for i, e in enumerate(self.display.event_list):
      if e.type == x.KeyPress or e.type == x.KeyRelease: #TODO not sure why KeyRelease needed!
        self.display.event_list.pop(i)
        self.key_num = KEYBOARD[e.xkey.keycode][0]
        self.key_code = KEYBOARD[e.xkey.keycode][1]
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
