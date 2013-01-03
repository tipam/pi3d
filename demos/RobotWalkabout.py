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

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

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
DISPLAY = Display.create(x=50, y=50, w=-100, h=-100)
DISPLAY.set_background(0.4,0.8,0.8,1)    	# r,g,b,alpha
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.width/1000.0, DISPLAY.height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#############################

# Load textures
reflcn = Texture("textures/stars.jpg")

#load environment cube
ectex = loadECfiles("textures/ecubes","sbox_interstellar")
myecube = EnvironmentCube(camera, light, 900.0,"FACES")
myecube.set_draw_details(flatsh,ectex)

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = Texture("textures/mars_colour.png")
bumpimg = Texture("textures/mudnormal.jpg")
mymap = ElevationMap(camera=camera, light=light, mapfile="textures/mars_height.png",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=128, divy=128) #testislands.jpg
mymap.buf[0].set_draw_details(shader,[mountimg1, bumpimg],128.0, 0.0)
mymap.set_fog((0.3,0.15,0.1,1.0), 300.0)


#create robot
metalimg = Texture("textures/metalhull.jpg")
robot_head= Sphere(camera, light, 2.0,12,12,0.5,"",0,3,0)
robot_body = Cylinder(camera, light, 2.0,4,12,"",0,1,0)
robot_leg = Cuboid(camera, light, 0.7,4.0,1.0,"",0,0.8,0)

robot = MergeShape(camera, light)
robot.add(robot_head.buf[0])
robot.add(robot_body.buf[0])
robot.add(robot_leg.buf[0], -2.1,0,0)
robot.add(robot_leg.buf[0], 2.1,0,0)
robot.buf[0].set_draw_details(shader, [metalimg, metalimg, reflcn], 1.0, 0.5)

#create space station
ssphere = Sphere(camera, light, 10,16,16)
scorrid = Cylinder(camera, light, 4,22,12)

station = MergeShape(camera, light, "",0,mymap.calcHeight(0,0),0, 0,0,0, 4,4,4)
station.add(ssphere.buf[0], -20,0,-20)
station.add(ssphere.buf[0], 20,0,-20)
station.add(ssphere.buf[0], 20,0,20)
station.add(ssphere.buf[0], -20,0,20)
station.add(scorrid.buf[0], -20,0,0, 90,0,0)
station.add(scorrid.buf[0], 0,0,20, 90,90,0)
station.add(scorrid.buf[0], 0,0,-20, 90,90,0)
station.buf[0].set_draw_details(shader, [metalimg, metalimg], 2.0)

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= (mymap.calcHeight(xm,zm)+avhgt)

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

omx, omy = mymouse.position()

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  camera.reset()
  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt < -1: sf = 6 - 5.5/abs(tilt)
  else: sf = 0.5
  xoff, yoff, zoff = sf*math.sin(math.radians(rot)), abs(1.25*sf*math.sin(math.radians(tilt))) + 3.0, -sf*math.cos(math.radians(rot))
  camera.rotate(tilt, rot, 0)           #Tank still affected by scene tilt
  camera.translate((xm + xoff, ym + yoff +5, zm + zoff))   #zoom camera out so we can see our robot

  #draw robot
  robot.draw()

  myecube.draw()#Draw environment cube
  myecube.position(xm, ym, zm)
  mymap.draw()		#Draw the landscape
  station.draw()

  mx, my = mymouse.position()

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
      ym = (mymap.calcHeight(xm,zm)+avhgt)
    elif k==115:  #kry S
      xm+=math.sin(math.radians(rot))
      zm-=math.cos(math.radians(rot))
      ym = (mymap.calcHeight(xm,zm)+avhgt)
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
