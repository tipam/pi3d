#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Simple textruring of Sphere objects against a plane. The atmosphere has
blend set to True and so has to be drawn after object behind it to allow them
to show through. Normal map used for moon is just a 'normal' pictures so normals
are calculated strangely and create odd shadows.
"""
from math import sin, cos

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Sphere import Sphere
from pi3d.shape.Plane import Plane

from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50)
DISPLAY.set_background(0,0,0,1)    	# r,g,b,alpha

shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#========================================

# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = Texture("textures/earth_clouds.png",True)
earthimg = Texture("textures/world_map.jpg")
moonimg = Texture("textures/moon.jpg")
starsimg = Texture("textures/stars2.jpg")
watimg = Texture("textures/water.jpg")

mysphere = Sphere(radius=2, slices=24, sides=24,
                  name="earth", z=5.8)
mysphere2 = Sphere(radius=2.05, slices=24, sides=24,
                   name="clouds", z=5.8)
mymoon = Sphere(radius=0.4, slices=16, sides=16, name="moon")
mymoon2 = Sphere(radius=0.1, slices=16, sides=16, name="moon2")
myplane = Plane(w=50, h=50, name="stars", z=30)

# Fetch key presses
mykeys = Keyboard()

rot=0.0
rot1=90.0
rot2=0.0
m1Rad = 4 # radius of moon orbit
m2Rad = 0.55 # radius moon's moon orbit


# Display scene
while DISPLAY.loop_running():
  myplane.rotateIncZ(0.01)
  mysphere.rotateIncY(-0.1)
  mysphere2.rotateIncY(-0.15)

  mymoon.position(mysphere.unif[0] + m1Rad*sin(rot1), mysphere.unif[1] + 0, mysphere.unif[2] - m1Rad*cos(rot1))
  mymoon.rotateIncY(-0.2)

  mymoon2.position(mymoon.unif[0] - m2Rad*sin(rot2), mymoon.unif[1], mymoon.unif[2] + m2Rad*cos(rot2))
  mymoon2.rotateIncY(-5.0)

  mysphere.draw(shader, [earthimg])
  mymoon.draw(shader, [moonimg, moonimg, starsimg], 1.0, 0.0)
  mymoon2.draw(shader, [watimg, watimg, starsimg], 4.0, 0.8)
  myplane.draw(flatsh,[starsimg])
  mysphere2.draw(shader, [cloudimg]) # this has to be last as blend = True

  rot1 += 0.005
  rot2 += 0.021

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot("earthPic.jpg")
    elif k==27:
      mykeys.close()
      DISPLAY.stop()
      break
    else:
      print(k)

  Camera.instance().was_moved = False
