#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Simple textruring of Sphere objects against a plane. The atmosphere has
blend set to True and so has to be drawn after object behind it to allow them
to show through. Normal map used for moon is just a 'normal' pictures so normals
are calculated strangely and create odd shadows.
Uses the import pi3d method to load *everything*
"""
from math import sin, cos
import demo
import pi3d
# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50)
DISPLAY.set_background(0,0,0,1)    	# r,g,b,alpha
shader = pi3d.Shader("shaders/uv_reflect")
flatsh = pi3d.Shader("shaders/uv_flat")
#========================================
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = pi3d.Texture("textures/earth_clouds.png",True)
earthimg = pi3d.Texture("textures/world_map.jpg")
moonimg = pi3d.Texture("textures/moon.jpg")
starsimg = pi3d.Texture("textures/stars2.jpg")
watimg = pi3d.Texture("textures/water.jpg")
moonbmp = pi3d.Texture("textures/moon_nm.jpg")
# Load shapes
mysphere = pi3d.Sphere(radius=2, slices=24, sides=24,
                  name="earth", z=5.8)
mysphere2 = pi3d.Sphere(radius=2.05, slices=24, sides=24,
                   name="clouds", z=5.8)
mymoon = pi3d.Sphere(radius=0.4, slices=16, sides=16, name="moon")
mymoon2 = pi3d.Sphere(radius=0.15, slices=16, sides=16, name="moon2")
myplane = pi3d.Plane(w=50, h=50, name="stars", z=30)
# Fetch key presses
mykeys = pi3d.Keyboard()

rot=0.0
rot1=90.0
rot2=0.0
m1Rad = 4 # radius of moon orbit
m2Rad = 0.6 # radius moon's moon orbit

# Display scene
while DISPLAY.loop_running():
  myplane.rotateIncZ(0.01)
  mysphere.rotateIncY(-0.1)
  mysphere2.rotateIncY(-0.14)
  mymoon.position(mysphere.x() + m1Rad*sin(rot1), mysphere.y(), 
                mysphere.z() - m1Rad*cos(rot1))
  mymoon.rotateIncY(-0.1)
  mymoon2.position(mymoon.x() - m2Rad*sin(rot2), mymoon.y(),
                mymoon.z() + m2Rad*cos(rot2))
  mymoon2.rotateIncZ(-0.61)

  mysphere.draw(shader, [earthimg])
  mymoon.draw(shader, [moonimg, moonbmp], 6.0, 0.0)
  mymoon2.draw(shader, [watimg, moonbmp, starsimg], 3.0, 0.8)
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

