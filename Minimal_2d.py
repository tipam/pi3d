#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example showing what can be left out. ESC to quit"""
import demo
import pi3d
DISPLAY = pi3d.Display.create(x=150, y=150)
shader = pi3d.Shader("uv_flat")
CAMERA = pi3d.Camera(is_3d=False)
sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader, w=100.0, h=100.0, z=5.0)
mykeys = pi3d.Keyboard()
xloc = 100.0
dx = 2.1
yloc = 100.0
dy = 1.13
while DISPLAY.loop_running():
  sprite.draw()
  sprite.rotateIncZ(1)
  sprite.position(xloc, yloc, 5.0)
  if xloc > 300.0:
    dx = -2.1
  elif xloc < -300.0:
    dx = 2.1
  if yloc > 300.0:
    dy = -1.13
  elif yloc < -300.0:
    dy = 1.13
  xloc += dx
  yloc += dy
  
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
