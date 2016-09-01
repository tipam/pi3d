from __future__ import absolute_import, division, print_function, unicode_literals

import sys, os, time

import pi3d

DTK = 0.05 #minimum time between key strokes
DTM = 0.15 #minimum time between mouse clicks

class Gui(object):
  def __init__(self, font, show_pointer=True):
    """hold information on all widgets and the pointer, creates a 2D Camera
    and uv_flat shader. Needs to have a Font object passed to it keeps track
    of when the last mouse click or key stroke to avoid double counting.
    Arguments

      *font*
        pi3d.Font object

    A Gui instance has to be passed to each gui widget (Button, Menu etc)
    as it is created to allow resources to the used and for checking.
    """
    self.shader = pi3d.Shader("uv_flat")
    dummycam = pi3d.Camera.instance() # in case this is prior to one being created 
    self.camera = pi3d.Camera(is_3d=False)
    self.widgets = []
    self.font = font
    self.font.blend = True
    self.focus = None
    self.show_pointer = show_pointer
    for p in sys.path:
      icon_path = p + '/pi3d/util/icons/'
      if os.path.exists(icon_path):
        self.icon_path = icon_path
        break
    if self.show_pointer:
      tex = pi3d.Texture(self.icon_path + "pointer.png", blend=True, mipmap=False)
      self.pointer = pi3d.Sprite(camera=self.camera, w=tex.ix, h=tex.iy, z=0.5)
      self.pointer.set_draw_details(self.shader, [tex])
      self.p_dx, self.p_dy = tex.ix/2.0, -tex.iy/2.0
    self.next_tm = time.time() + DTM

  def draw(self, x, y):
    """draw all visible widges and pointer at x, y
    """
    for w in self.widgets:
      if w.visible:
        w.draw()
    if self.show_pointer:
      self.pointer.position(x + self.p_dx, y + self.p_dy, 0.5)
      self.pointer.draw()

  def check(self, x, y):
    tm = time.time()
    if tm < self.next_tm:
      return
    self.next_tm = tm + DTM
    for w in self.widgets:
      if w.visible and w.check(x, y):
        self.focus = w
        break

  def checkkey(self, k):
    tm = time.time()
    if tm < self.next_tm:
      return
    self.next_tm = tm + DTK
    if type(self.focus) is TextBox:
      self.focus._click(k)
    else:
      for w in self.widgets:
        if w.visible and w.checkkey(k):
          self.focus = w
          break

class Widget(object):
  def __init__(self, gui, shapes, x, y, callback=None, label=None,
               label_pos='left', shortcut=None):
    """contains functionality of buttons and is inherited by other gui
    components. Arguments:

      *gui*
        Gui object parent to this widget
      *shapes*
        drawable object such as Sprite or String, or list of two to toggle
      *x,y*
        location of top left corner of this widget
      *label*
        string to use as label
      *label_pos*
        position of label 'left', 'right', 'above', 'below'
      *shortcut*
        shortcut key to have same effect as clicking wit mouse???
    """
    if not (type(shapes) is list or type(shapes) is tuple):
      self.shapes = [shapes]
    else:
      self.shapes = shapes
    self.toggle = len(self.shapes) > 1 #this widget can toggle between two
    self.clicked = False
    self.callback = callback
    self.shortcut = shortcut
    self.label_pos = label_pos
    if label is not None:
      self.labelobj = pi3d.String(font=gui.font, string=label, is_3d=False,
                              camera=gui.camera, justify='L')
      self.labelobj.set_shader(gui.shader)
    else:
      self.labelobj = None
    self.relocate(x, y)
    if not (self in gui.widgets): #because TextBox re-runs Widget.__init__
      gui.widgets.append(self)
    self.visible = True

  def relocate(self, x, y):
    if len(self.shapes[0].buf[0].array_buffer) > 0:
      b = self.shapes[0].get_bounds()
    else:
      b = [x, y, 1.0, x, y, 1.0]
    self.bounds = [x, y - b[4] + b[1], x + b[3] - b[0], y]
    for s in self.shapes:
      s.position(x - b[0], y - b[4], 1.0)
    if self.labelobj is not None:
      b = self.labelobj.get_bounds()
      if self.label_pos == 'above':
        self.labelobj.position((x + self.bounds[2] - b[3] - b[0]) / 2.0,
                              y - b[1], 1.0)
      elif self.label_pos == 'below':
        self.labelobj.position((x + self.bounds[2] - b[3] - b[0]) / 2.0,
                              self.bounds[1] - b[4], 1.0)
      elif self.label_pos == 'right':
        self.labelobj.position(self.bounds[2] + b[0] - 5.0,
                  (y + self.bounds[1] - b[1] - b[4]) / 2.0, 1.0)
      else:
        self.labelobj.position(x - b[3] - 5.0,
                  (y + self.bounds[1] - b[1] - b[4]) / 2.0, 1.0)      

  def draw(self):
    if self.toggle and self.clicked:
      self.shapes[1].draw()
    else:
      self.shapes[0].draw()
    for s in self.shapes[2:]:
      s.draw()
    if self.labelobj:
      self.labelobj.draw()

  def check(self, x, y):
    if x > self.bounds[0] and x < self.bounds[2] and y > self.bounds[1] and y < self.bounds[3]:
      self._click(x, y)
      return True
    return False

  def checkkey(self, k):
    if k == self.shortcut:
      self._click(k)
      return True
    return False

  def _click(self, *args):
    if self.toggle:
      self.clicked = not self.clicked
    if self.callback:
      self.callback(args)

class Button(Widget):
  def __init__(self, gui, imgs, x, y, callback=None, label=None,
               label_pos='left', shortcut=None):
    """This inherits pretty much everything it needs from Widget, it just
    takes a list of images rather than Shapes. Otherwise same Arguments.

      *imgs*
        list of strings. If these exist as files using the path and file
        name then those will be used. Otherwise the pi3d/util/icons path
        will be prepended
    """
    if not (type(imgs) is list or type(imgs) is tuple):
      imgs = [imgs]
    shapes = []
    for i in imgs:
      if not os.path.isfile(i):
        i = gui.icon_path + i
      tex = pi3d.Texture(i, blend=True, mipmap=False)
      shape = pi3d.Sprite(camera=gui.camera, w=tex.ix, h=tex.iy, z=2.0)
      shape.set_draw_details(gui.shader, [tex])
      shapes.append(shape)
    super(Button, self).__init__(gui, shapes, x, y, callback=callback,
                  label=label, label_pos=label_pos, shortcut=shortcut)

class Radio(Button):
  def __init__(self, gui, x, y, callback=None, label=None,
               label_pos='left', shortcut=None):
    """This is a toggle button with two checkbox images. Same Arguments
    as Widget but missing the list of Shapes completely.
    """
    super(Radio, self).__init__(gui, ['cba0.gif', 'cba1.gif'], x, y,
        callback=callback, label=label, label_pos=label_pos, shortcut=shortcut)

class Scrollbar(Widget):
  def __init__(self, gui, x, y, width, start_val=None, callback=None, label=None,
               label_pos='left', shortcut=None):
    """This consists of four Shapes but the first one is duplicated so
    the Widget.draw() method can be used unchanged. The images are hard
    coded so no list of Shapes or images needs to be supplied however
    arguments additional to those for Widget are

      *width*
        width of the scroll (excluding buttons on either end)
      *start_val*
        proportion of the way across i.e. if width = 200 then start_val
        of 150 would be three quarters

    NB the callback is called with *args equal to the position of the slider
    so the function needs to be defined with this in mind i.e.
    ``def cb(*args):`` args will then be available as a tuple (0.343,)
    """
    imgs = ["scroll.gif", "scroll.gif", "scroll_lh.gif", "scroll_rh.gif",
            "scroll_thumb.gif"]
    shapes = []
    end_w = 0
    for i, im in enumerate(imgs):
      tex = pi3d.Texture(gui.icon_path + im, blend=True, mipmap=False)
      w = tex.ix if i > 0 else width
      if i == 2:
        end_w = tex.ix #offsets for end buttons
      if i == 4:
        thumb_w = tex.ix / 2.0 #offset for thumb
      shape = pi3d.Sprite(camera=gui.camera, w=w, h=tex.iy, z=2.0)
      shape.set_draw_details(gui.shader, [tex])
      shapes.append(shape)
    super(Scrollbar, self).__init__(gui, shapes, x, y, callback=callback,
            label=label, label_pos=label_pos, shortcut=shortcut)
    self.toggle = False
    self.t_stop = [self.bounds[0] + thumb_w, self.bounds[2] - thumb_w]
    if start_val is None:
      start_val = width / 2.0
    self.thumbpos = start_val / width * (self.t_stop[1] - self.t_stop[0])
    self.shapes[4].positionX(self.t_stop[0] + self.thumbpos)
    self.shapes[4].translateZ(-0.1)
    self.shapes[2].translateX((-width - end_w) / 2.0)
    self.shapes[3].translateX((width + end_w) / 2.0)
    self.bounds[0] -= end_w
    self.bounds[2] += end_w
    if self.labelobj is not None:
      if label_pos == 'left':
        self.labelobj.translateX(-end_w)
      elif label_pos == 'right':
        self.labelobj.translateX(end_w)
        
  def _click(self, *args):
    thumb_x = self.t_stop[0] + self.thumbpos
    if len(args) == 2:
      x, y = args
      if x < thumb_x and thumb_x > self.t_stop[0]:
        self.thumbpos -= (thumb_x - x) / 2.0
      if x > thumb_x and thumb_x < self.t_stop[1]:
        self.thumbpos += (x - thumb_x) / 2.0
      if self.thumbpos < 0:
        self.thumbpos = 0
      if self.thumbpos > (self.t_stop[1] - self.t_stop[0]):
        self.thumbpos = (self.t_stop[1] - self.t_stop[0])
      self.shapes[4].positionX(self.t_stop[0] + self.thumbpos)
      
    if self.callback:
      self.callback((thumb_x - self.t_stop[0])/(self.t_stop[1] - self.t_stop[0]))

class MenuItem(Widget):
  def __init__(self, gui, text, callback=None, shortcut=None):
    """These are the clickable Widgets of the menu system. Instead of a
    list of Shapes they have a string argument, there is no label or
    label_pos and the x and y values are obtained from the position and
    orientation of the parent Menu.

      *text*
        string used to construct a pi3d.String
        
    """
    menu_text = pi3d.String(font=gui.font, string=text, is_3d=False,
                              camera=gui.camera, justify='L')
    menu_text.set_shader(gui.shader)
    super(MenuItem, self).__init__(gui, [menu_text], 0, 0,
        callback=callback, shortcut=shortcut)
    self.child_menu = None
    self.own_menu = None

  def _click(self, *args):
    for item in self.own_menu.menuitems:
      if item != self and item.child_menu:
        item.child_menu.hide()
    if self.child_menu:
      if self.child_menu.visible:
        self.child_menu.hide()
      else:
        self.child_menu.show()
    super(MenuItem, self)._click(args)

class Menu(object):
  def __init__(self, parent_item=None, menuitems=[], x=0, y=0, horiz=True,
                position='right', visible=True):
    """Container for MenuItems, forming either a horizontal or vertical
    bar. Arguments

      *parent_item*
        a MenuItem that will make this Menu visible when clicked
      *menuitems*
        a list of MenuItems to be displayed in this Menu
      *x*
        x location will be overwritten unless parent_item == None
      *y*
        similarly the y location
      *horiz*
        set True (default) for horizontal layout on the menu bar, False
        for vertical listing
      *position*
        relative to the MenuItem that gives rise to this Menu when clicked
        'right' or any other text interpreted as below
      *visible*
        when an alternative branch of the menu tree is selected or the
        parent_item is re-clicked this menu is hidden, along with all
        its children recursively. They are set to visible = False and
        not drawn and not checked for mouse clicks.
        
    """
    self.visible = visible
    self.parent_item = parent_item
    if parent_item is not None:
      parent_item.child_menu = self
      if position == 'right':
        self.x = parent_item.bounds[2] + 5
        self.y = parent_item.bounds[3]
      else:
        self.x = parent_item.bounds[0]
        self.y = parent_item.bounds[1]
    else:
      self.x = x
      self.y = y
    i_x = self.x
    i_y = self.y
    for item in menuitems:
      item.own_menu = self
      item.relocate(i_x, i_y)
      item.visible = visible
      if horiz:
        i_x = item.bounds[2] + 5
      else:
        i_y = item.bounds[1]
    self.menuitems = menuitems
    if parent_item != None:
      self.hide()

  def hide(self):
    self.visible = False
    for i in self.menuitems:
      i.visible = False
      if i.child_menu:
        i.child_menu.hide()

  def show(self):
    self.visible = True
    for i in self.menuitems:
      i.visible = True

class TextBox(Widget):
  def __init__(self, gui, txt, x, y, callback=None, label=None,
               label_pos='left', shortcut=None):
    self.gui = gui
    self.txt = txt
    self.x = x
    self.y = y
    self.callback = callback
    self.label = label
    self.label_pos = label_pos
    self.shortcut = shortcut
    self.cursor = len(txt)
    tex = pi3d.Texture(gui.icon_path + 'tool_stop.gif', blend=True, mipmap=False)
    self.cursor_shape = pi3d.Sprite(camera=gui.camera, w=tex.ix/10.0,
                          h=tex.iy, z=1.1)
    self.cursor_shape.set_draw_details(gui.shader, [tex])
    self.recreate()

  def recreate(self):
    self.c_lookup = [] #mapping between clicked char and char in string
    for i, l in enumerate(self.txt):
      if l != '\n':
        self.c_lookup.append(i)
    textbox = pi3d.String(font=self.gui.font, string=self.txt, is_3d=False,
                              camera=self.gui.camera, justify='L', z=1.0)
    textbox.set_shader(self.gui.shader)
    super(TextBox, self).__init__(self.gui, [textbox], self.x, self.y,
                        callback=self.callback, label=self.label,
                        label_pos=self.label_pos, shortcut=self.shortcut)

  def _get_charindex(self, x, y):
    """Find the x,y location of each letter's bottom left and top right
    vertices to return a character index of the click x,y
    """
    verts = self.shapes[0].buf[0].array_buffer[:,0:3]
    x = x - self.x + verts[2][0]
    y = y - self.y + verts[0][1]
    nv = len(verts)
    for i in range(0, nv, 4):
      vtr = verts[i] # top right
      vbl = verts[i + 2] # bottom left
      if x >= vbl[0] and x < vtr[0] and y >= vbl[1] and y < vtr[1]:
        i = int(i / 4)
        c_i = self.c_lookup[i]
        if c_i == (len(self.txt) - 1) or self.c_lookup[i + 1] > c_i + 1:
          if (vtr[0] - x) < (x - vbl[0]):
            c_i += 1
        return c_i
    return len(self.txt)

  def _get_cursor_loc(self, i):
    verts = self.shapes[0].buf[0].array_buffer[:,0:3]
    maxi = int(len(verts) / 4 - 1)
    if maxi < 0:
      return self.x, self.y
    if i > maxi:
      x = self.x - verts[2][0] + verts[maxi * 4][0]
      y = self.y - verts[0][1] + (verts[maxi * 4][1] + verts[maxi * 4 + 2][1]) / 2.0
    else:
      x = self.x - verts[2][0] + verts[i * 4 + 2][0]
      y = self.y - verts[0][1] + (verts[i * 4][1] + verts[i * 4 + 2][1]) / 2.0
    return x, y

  def checkkey(self, k):
    """have to use a slightly different version without the _click() call
    """
    if k == self.shortcut:
      return True
    return False

  def _click(self, *args):
    if len(args) == 2: #mouse click
      x, y = args
      self.cursor = self._get_charindex(x, y)
    else: #keyboard input
      k = args[0]
      if k == '\t': #backspace use tab char
        if self.cursor > 0:
          self.txt = self.txt[:(self.cursor - 1)] + self.txt[self.cursor:]
          self.cursor -= 1
      elif k == '\r': #delete use car ret char
        self.txt = self.txt[:self.cursor] + self.txt[(self.cursor + 1):]
      else:
        self.txt = self.txt[:self.cursor] + k + self.txt[(self.cursor):]
        self.cursor += 1
      self.recreate()
    super(TextBox, self)._click()

  def draw(self):
    if self.gui.focus == self:
      x, y = self._get_cursor_loc(self.cursor)
      self.cursor_shape.position(x, y, 1.1)
      self.cursor_shape.draw()
    super(TextBox, self).draw()
