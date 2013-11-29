#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
import math, random, time, traceback, os
import sys
import demo
import pi3d

def cbx(*args):
  if radio.clicked:
    menu1.show()
  else:
    menu1.hide()

def cb(*args):
  print(args)

DISPLAY = pi3d.Display.create(w=640, h=480, frames_per_second=30)
DISPLAY.set_background(0.8,0.8,0.8,1.0) # r,g,b,alpha

font = pi3d.Font("fonts/FreeSans.ttf", color=(0,0,0,255), font_size=20)
gui = pi3d.Gui(font)
ww, hh = DISPLAY.width / 2.0, DISPLAY.height / 2.0
radio = pi3d.Radio(gui, ww -20, hh - 10,
                label="This unhides the menu!", label_pos="left", callback=cbx)
button = pi3d.Button(gui, ["tool_run.gif", "tool_pause.gif"], ww - 40,
                -hh + 40, callback=cb, shortcut='q')
scrollbar = pi3d.Scrollbar(gui, -ww + 20, -hh + 20, 200, start_val=50,
                label="slide me", label_pos='above', callback=cb)

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
          x=-DISPLAY.width/2, y=DISPLAY.height/2, visible=True)
menu2 = pi3d.Menu(parent_item=mi1, menuitems=[mi11, mi12], horiz=False, position='below')
menu3 = pi3d.Menu(parent_item=mi11, menuitems=[mi111, mi112], horiz=False, position='right')
menu4 = pi3d.Menu(parent_item=mi12, menuitems=[mi121, mi122], horiz=False, position='right')

textbox = pi3d.TextBox(gui, "this is\na textbox\nover lines", 100, 100, callback=cb)

mx, my = 0, 0
inputs = pi3d.InputEvents()
inputs.get_mouse_movement()
while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  inputs.do_input_events()
  imx, imy, mv, mh, butt = inputs.get_mouse_movement()
  mx += imx
  my -= imy
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
      elif k == 'KEY_SPACE':
        this_key = ' '
      elif k == 'KEY_BACKSPACE':
        this_key = '\t' # use tab for backspace
      elif k == 'KEY_DELETE':
        this_key = '\r' # use car ret for delete
      elif k == 'KEY_ENTER':
        this_key = '\n'
    if this_key:
      if not sh:
        this_key = this_key.lower()
      gui.checkkey(this_key)

inputs.release()
DISPLAY.destroy()
