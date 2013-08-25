#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Peter Hess' converted shader for pi3d dynamic texturing """
import demo
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50)
shader = pi3d.Shader("star")
tex = pi3d.Texture("textures/PATRN.PNG")
box = pi3d.Cuboid(x=0, y=0, z=2.2)
box.set_draw_details(shader,[tex])
tm = 0.0
dt = 0.01
sc = 0.0
ds = 0.001

mykeys = pi3d.Keyboard()
while DISPLAY.loop_running():
  box.set_custom_data(48, [tm, sc, -0.5 * sc])
  """Three custom unif values used by star shader to animate image"""
  tm += dt
  sc = (sc + ds) % 10.0
  box.rotateIncX(0.01)
  box.rotateIncY(0.071)
  box.draw()

  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
