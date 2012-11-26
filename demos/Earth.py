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

from pi3d.Display import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.context.Light import Light

from pi3d.shape.Sphere import Sphere
from pi3d.shape.Plane import Plane

from pi3d.util import Draw
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
display = Display()
display.create3D(0,0)   	# x,y,width,height defaults to full screen if w,h ommitted
display.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = Texture("textures/earth_clouds.png",True)
earthimg = Texture("textures/world_map.jpg")
moonimg = Texture("textures/moon.jpg")
starsimg = Texture("textures/stars2.jpg")
watimg = Texture("textures/water.jpg")

mysphere = Sphere(2,24,24,0.0,"earth",0,0,-5.8)
mysphere2 = Sphere(2.05,24,24,0.0,"clouds",0,0,-5.8)
mymoon = Sphere(0.4,16,16,0.0,"moon",0,0,0)
mymoon2 = Sphere(0.1,16,16,0.0,"moon2",0,0,0)
myplane = Plane(50,50, "stars", 0,0,-10)

# Fetch key presses
mykeys = Keyboard()

rot=0.0
rot1=90.0
rot2=0.0
m1Rad = 4 # radius of moon orbit
m2Rad = 0.55 # radius moon's moon orbit


#create a light
mylight = Light(0,5,5,5,"sun",10,0,6, .1,.1,.2, 0)
mylight.on()

# Display scene
while 1:
  display.clear()

  myplane.draw(starsimg)
  myplane.rotateIncZ(0.01)

  mysphere.draw(earthimg)
  mysphere.rotateIncY(0.1)
  mysphere2.draw(cloudimg)
  mysphere2.rotateIncY(.15)

  mymoon.draw(moonimg)
  mymoon.position(mysphere.x+m1Rad*sin(rot1),mysphere.y+0,mysphere.z-m1Rad*cos(rot1))
  mymoon.rotateIncY(0.2)

  mymoon2.draw(watimg)
  mymoon2.position(mymoon.x+m2Rad*sin(rot2),mymoon.y+0,mymoon.z-m2Rad*cos(rot2))
  mymoon2.rotateIncY(3)

  rot1 -= 0.005
  rot2 -= 0.021

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot("earthPic.jpg")
    elif k==27:
      mykeys.close()
      display.destroy()
      break
    else:
      print k

  display.swapBuffers()
