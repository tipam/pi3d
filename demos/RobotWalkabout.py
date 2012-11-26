# Robot walkabout example using pi3d module
# =========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 20Jul12
#
# Demonstrates offset camera to view an avatar moving about a map.  Also includes tiled mapping on landscape
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

import math

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Fog import Fog
from pi3d.context.Light import Light

from pi3d.shape.Cuboid import Cuboid
from pi3d.shape.Cylinder import Cylinder
from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Sphere import Sphere

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50, w=-100, h=-100, near=0.5)
DISPLAY.setBackColour(0.4,0.8,0.8,1)    	# r,g,b,alpha

# Load textures
tree2img = Texture("textures/tree2.png")
tree1img = Texture("textures/tree1.png")
grassimg = Texture("textures/grass.png")
hb2img = Texture("textures/hornbeam2.png")

#load environment cube
ectex = loadECfiles("textures/ecubes","sbox_interstellar")
myecube = EnvironmentCube(900.0,"FACES")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = Texture("textures/mars_colour.png")
mymap = ElevationMap("textures/mars_height.png",mapwidth,mapdepth,mapheight,128,128) #testislands.jpg

#create robot
metalimg = Texture("textures/metalhull.jpg")
robot_head= Sphere(2.0,12,12,0.5,"",0,3,0)
robot_body = Cylinder(2.0,4,12,"",0,1,0)
robot_leg = Cuboid(0.7,4.0,1.0,"",0,0.8,0)

robot = MergeShape()
robot.add(robot_head)
robot.add(robot_body)
robot.add(robot_leg, -2.1,0,0)
robot.add(robot_leg, 2.1,0,0)

#create space station
ssphere = Sphere(10,16,16)
scorrid = Cylinder(4,22,12)

station = MergeShape("",0,mymap.calcHeight(0,0),0, 0,0,0, 4,4,4)
station.add(ssphere, -20,0,-20)
station.add(ssphere, 20,0,-20)
station.add(ssphere, 20,0,20)
station.add(ssphere, -20,0,20)
station.add(scorrid, -20,0,0, 90,0,0)
station.add(scorrid, 0,0,20, 90,90,0)
station.add(scorrid, 0,0,-20, 90,90,0)

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()
mtrx = Matrix()

omx=mymouse.x
omy=mymouse.y

myfog = Fog(0.002,(0.3,0.8,0.6,0.5))
mylight = Light(0,1,1,1,"",10,10,10, .9,.7,.6)

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  mtrx.identity()
  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt<-1: sf=1.0/-tilt
  else: sf=1.0
  mtrx.translate(0,-10*sf-5.0,-40*sf)   #zoom camera out so we can see our robot
  mtrx.rotate(tilt, 0, 0)		#Robot still affected by scene tilt

  #draw robot
  mylight.on()
  robot.drawAll(metalimg)
  mylight.off()

  mtrx.rotate(0, rot, 0)		#rotate rest of scene around robot
  mtrx.translate(xm,ym,zm)	#translate rest of scene relative to robot position

  myecube.draw(ectex,xm,ym,zm)#Draw environment cube
  myfog.on()
  mymap.draw(mountimg1)		#Draw the landscape
  station.drawAll(metalimg)
  myfog.off()

  mx=mymouse.x
  my=mymouse.y

  #if mx>DISPLAY.left and mx<DISPLAY.right and my>DISPLAY.top and my<DISPLAY.bottom:
  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:    #key W
      xm-=math.sin(math.radians(rot))
      zm+=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==115:  #kry S
      xm+=math.sin(math.radians(rot))
      zm-=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==39:   #key '
      tilt -= 2.0
      print tilt
    elif k==47:   #key /
      tilt += 2.0
    elif k==97:   #key A
        rot -= 2
    elif k==100:  #key D
        rot += 2
    elif k==112:  #key P
        screenshot("walkaboutRobot.jpg")
    elif k==27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
        print k

  DISPLAY.swapBuffers()
