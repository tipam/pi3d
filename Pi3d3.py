#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Peter Hess' converted shader for pi3d dynamic texturing """
import demo
import pi3d

DISPLAY = pi3d.Display.create(x=100, y=100)
shader = pi3d.Shader("star")
tex = pi3d.Texture("textures/PATRN.PNG")
#box = pi3d.Cuboid(x=0, y=0, z=2.2)
box = pi3d.Cuboid(w=100, h=100, d=100, x=0, y=0, z=100.0)
box.set_draw_details(shader,[tex])
tm = 0.0
dt = 0.01
sc = 0.0
ds = 0.001

mykeys = pi3d.Keyboard()
ASPECT = DISPLAY.width / DISPLAY.height
camera1 = pi3d.Camera((0,0,0), (0,0,-0.1), (1, 1000, 45, ASPECT), is_3d=True)
camera2 = pi3d.Camera(is_3d=False)
while DISPLAY.loop_running():
  box.set_custom_data(48, [tm, sc, -0.5 * sc])
  """Three custom unif values used by star shader to animate image"""
  tm += dt
  sc = (sc + ds) % 10.0
  box.rotateIncX(0.1)
  box.rotateIncY(0.71)
  box.position(-50.0, 50.0, 400.0)
  box.draw(camera=camera1)
  box.position(0.0, 0.0, 100.0)
  box.draw(camera=camera2)
  

  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
