#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
import math, random, time, traceback, os
import sys
import demo
import pi3d
# use tab for backspace and carriage return for delete
CHARS = {'KEY_SPACE':' ', 'KEY_BACKSPACE':'\t', 'KEY_DELETE':'\r',
        'KEY_ENTER':'\n', 'KEY_COMMA':',', 'KEY_DOT':'.'}

def cbx(*args):
  if radio.clicked:
    menu1.show()
  else:
    menu1.hide()

def cb(*args):
  print(args)

class scroll_cb(object):
  def __init__(self, callback, delta):
    self.callback = callback
    self.delta = delta

  def roty(self, *args):
    print(args)
    slideval = args[0] * self.delta
    self.callback(slideval)
  
class jogger(object):
  "jogger class"
  def __init__(self, gui, label, x, y, callback, delta) :
    self.callback = callback
    self.delta = delta
    self.x = x
    self.y = y
    self.butP = pi3d.Button(gui, "l.gif", x, y, label=label,
                                        shortcut='d', callback=self.rotp)
    self.butM = pi3d.Button(gui, "r.gif", x + 32, y, shortcut='l',
                                        callback=self.rotm)

  def rotp(self, *args):
    self.callback(self.delta)

  def rotm(self, *args):
    self.callback(-self.delta)

DISPLAY = pi3d.Display.create(w=640, h=480, frames_per_second=30)
DISPLAY.set_background(0.8,0.8,0.8,1.0) # r,g,b,alpha

shader = pi3d.Shader("uv_reflect")
font = pi3d.Font("fonts/FreeSans.ttf", color=(0,0,0,255), font_size=20)
gui = pi3d.Gui(font)
ww, hh = DISPLAY.width / 2.0, DISPLAY.height / 2.0

img = pi3d.Texture("textures/rock1.jpg")
model = pi3d.Cuboid(z=5.0)
model.set_draw_details(shader, [img])

radio = pi3d.Radio(gui, ww -20, hh - 32,
                label="unhides menu!", label_pos="left", callback=cbx)
xi = -ww
yi = hh
for b in ['tool_estop.gif', 'tool_power.gif', 'tool_open.gif',
          'tool_reload.gif', 'tool_run.gif', 'tool_step.gif',
          'tool_pause.gif', 'tool_stop.gif', 'tool_blockdelete.gif',
          'tool_optpause.gif', 'tool_zoomin.gif', 'tool_zoomout.gif',
          'tool_axis_z.gif', 'tool_axis_z2.gif', 'tool_axis_x.gif',
          'tool_axis_y.gif', 'tool_axis_p.gif', 'tool_rotate.gif',
          'tool_clear.gif']:
  g = pi3d.Button(gui, b, xi, yi, shortcut='d', callback=cb)
  xi = xi + 32


button = pi3d.Button(gui, ["tool_run.gif", "tool_pause.gif"], ww - 40,
                -hh + 40, callback=cb, shortcut='q')
scr_cb = scroll_cb(model.rotateToY, -360) #convoluted way of avoiding global!
scrollbar = pi3d.Scrollbar(gui, -ww + 20, -hh + 20, 200, start_val=50,
                label="slide me", label_pos='above', callback=scr_cb.roty)

jog1 = jogger(gui, 'X', ww - 64, hh - 64, model.translateX, -0.1)
jog2 = jogger(gui, 'Y', ww - 64, hh - 96, model.translateY, 0.1)
jog3 = jogger(gui, 'Z', ww - 64, hh - 128, model.translateZ, 0.1)
jog4 = jogger(gui, 'Zt', ww - 64, hh - 160, model.rotateIncZ, 7)

mi1 = pi3d.MenuItem(gui,"File")
mi2 = pi3d.MenuItem(gui,"Edit")
mi3 = pi3d.MenuItem(gui,"Window")
mi11 = pi3d.MenuItem(gui, "Open")
mi12 = pi3d.MenuItem(gui, "Close")
mi111 = pi3d.MenuItem(gui, "x1", callback=cb)
mi112 = pi3d.MenuItem(gui, "x2", callback=cb)
mi121 = pi3d.MenuItem(gui, "v3", callback=cb)
mi122 = pi3d.MenuItem(gui, "v4", callback=cb)

menu1 = pi3d.Menu(parent_item=None, menuitems=[mi1, mi2, mi3],
          x=-ww, y=hh-32, visible=True)
menu2 = pi3d.Menu(parent_item=mi1, menuitems=[mi11, mi12], horiz=False, position='below')
menu3 = pi3d.Menu(parent_item=mi11, menuitems=[mi111, mi112], horiz=False, position='right')
menu4 = pi3d.Menu(parent_item=mi12, menuitems=[mi121, mi122], horiz=False, position='right')

textbox = pi3d.TextBox(gui, "type here", 100, -180, callback=cb, label='TextBox (KEY t to edit)',
                        shortcut='t')

mx, my = 0, 0
inputs = pi3d.InputEvents()
inputs.get_mouse_movement()
while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  inputs.do_input_events()
  imx, imy, mv, mh, butt = inputs.get_mouse_movement()
  mx += imx
  my -= imy
  model.draw()
  gui.draw(mx, my)
  if inputs.key_state("BTN_MOUSE"):
    gui.check(mx, my)
  kk = inputs.get_keys()
  if kk:
    sh = False
    this_key = None
    for k in kk:
      if 'SHIFT' in k:
        sh = True 
      if len(k) == 5:
        this_key = k[4]
      elif k in CHARS:
        this_key = CHARS[k]
    if this_key:
      if not sh:
        this_key = this_key.lower()
      gui.checkkey(this_key)

inputs.release()
DISPLAY.destroy()
