import os

from pi3d import *
from six_mod.moves import tkinter

class TkWin(tkinter.Tk):
  """
  *TkWin* encapsulates a Tk window and keeps track of the mouse and keyboard.

  """
  def __init__(self, parent, title, width, height, bg='#000000'):
    """
    Arguments:

    *parent*
      Parent Tk window or Null for none.
    *title*
      Title for window.
    *width, height*
      Dimensions of window.
    """
    display = os.environ.get('DISPLAY', None)
    if not display:
      os.environ['DISPLAY'] = ':0'

    tkinter.Tk.__init__(self, parent)

    def mouseclick_callback(event):
      if not self.resized:
        self.ev = 'click'
        self.x = event.x
        self.y = event.y

    def mousemove_callback(event):
      if not self.resized:
        self.ev = 'move'
        self.x = event.x
        self.y = event.y

    def mousewheel_callback(event):
      if not self.resized:
        self.ev = 'wheel'
        self.num = event.num
        self.delta = event.delta

    def drag_callback(event):
      if not self.resized:
        self.ev = 'drag'
        self.x = event.x
        self.y = event.y
        mouserot = event.x

    def resize_callback(event):
      self.ev = 'resized'
      self.winx = self.winfo_x()
      self.winy = self.winfo_y()
      self.width = event.width
      self.height = event.height
      self.resized = True

    def key_callback(event):
      if not self.resized:
        self.ev = 'key'
        self.key = event.keysym
        self.char = event.char

    tkinter.Tk.bind(self, '<Button-1>', mouseclick_callback)
    tkinter.Tk.bind(self, '<B1-Motion>', drag_callback)
    tkinter.Tk.bind(self, '<Motion>', mousemove_callback)
    tkinter.Tk.bind(self, '<MouseWheel>', mousewheel_callback)
    tkinter.Tk.bind(self, '<Configure>', resize_callback)
    tkinter.Tk.bind_all(self, '<Key>', key_callback)
    tkinter.Tk.geometry(self, str(width) + 'x' + str(height))
    tkinter.Tk.configure(self, bg=bg)

    self.title(title)
    self.ev = ''
    self.resized = False

