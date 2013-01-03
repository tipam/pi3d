# Earth and example shapes using pi3d module
# ==========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.03 - 20Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#
from math import sin, cos

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Sphere import Sphere
from pi3d.shape.Plane import Plane

from pi3d.util import Draw
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50)
DISPLAY.set_background(0,0,0,1)    	# r,g,b,alpha
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
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

mysphere = Sphere(camera, light, 2,24,24,0.0,"earth",0,0, 5.8)
mysphere2 = Sphere(camera, light, 2.05,24,24,0.0,"clouds",0,0, 5.8)
mymoon = Sphere(camera, light, 0.4,16,16,0.0,"moon",0,0,0)
mymoon2 = Sphere(camera, light, 0.1,16,16,0.0,"moon2",0,0,0)
myplane = Plane(camera, light, 50,50, "stars", 0,0, 10)

# Fetch key presses
mykeys = Keyboard()

rot=0.0
rot1=90.0
rot2=0.0
m1Rad = 4 # radius of moon orbit
m2Rad = 0.55 # radius moon's moon orbit


# Display scene
while 1:
  DISPLAY.clear()

  myplane.draw(flatsh,[starsimg], 0.0, -1.0)
  myplane.rotateIncZ(0.01)

  mysphere.draw(shader, [earthimg])
  mysphere.rotateIncY(-0.1)
  mysphere2.draw(shader, [cloudimg])
  mysphere2.rotateIncY(-0.15)

  mymoon.draw(shader, [moonimg, moonimg, starsimg], 1.0, 0.0)
  mymoon.position(mysphere.unif[0] + m1Rad*sin(rot1), mysphere.unif[1] + 0, mysphere.unif[2] - m1Rad*cos(rot1))
  mymoon.rotateIncY(-0.2)

  mymoon2.draw(shader, [watimg, watimg, starsimg], 4.0, 0.8)
  mymoon2.position(mymoon.unif[0] - m2Rad*sin(rot2), mymoon.unif[1], mymoon.unif[2] + m2Rad*cos(rot2))
  mymoon2.rotateIncY(-5.0)

  rot1 += 0.005
  rot2 += 0.021

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot("earthPic.jpg")
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print k

  camera.was_moved = False

  DISPLAY.swapBuffers()
