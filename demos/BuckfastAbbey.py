# Loading EGG model
# =================
# This example - Copyright (c) 2012 - Tim Skillman
# EGG loader code by Paddy Gaunt, Copyright (c) 2012
# Version 0.01 - 03Jul12
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
from __future__ import absolute_import

import math,random

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.Model import Model

from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100)
DISPLAY.set_background(1.0,0.4,0.6,1)    	# r,g,b,alpha
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.width/1000.0, DISPLAY.width/1000.0))
light = Light((5, 10, 20))

# load shader
shader = Shader("shaders/uv_light")
flatsh = Shader("shaders/uv_flat")

print "=============================================================="
print "Instructions:"
print ""
print "Keys-             W - Forward,"
print "        A - Left   S - Back     D - right"
print ""
print "Move mouse to pan view.  Click mouse to exit or press ESCAPE"
print "=============================================================="

ectex = loadECfiles("textures/ecubes","sbox")
myecube = EnvironmentCube(camera, light, 900.0,"FACES", "bfa", 0.0, 50.0, 0.0)
myecube.set_draw_details(flatsh, ectex)

# load model_loadmodel
mymodel = Model(camera, light, "models/Buckfast Abbey/BuckfastAbbey.egg", "Abbey",
                0, 0, 0, -90, 0, 0, 0.03, 0.03, 0.03)
mymodel.set_shader(shader)

# Create keyboard and mouse event objects
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

#screenshot number
scshots = 1

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= avhgt

omx, omy = mymouse.position()

while 1:
  DISPLAY.clear()

  camera.reset()
  camera.rotate(tilt, 0, 0)
  camera.rotate(0, rot, 0)
  camera.translate((xm, ym, zm))

  myecube.draw()
  mymodel.draw()

  mx, my = mymouse.position()

  if mx>DISPLAY.left and mx<DISPLAY.right and my>DISPLAY.top and my<DISPLAY.bottom:
    rot -= (mx-omx)*0.8
    tilt += (my-omy)*0.8
    omx=mx
    omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k > -1:
    if k == 119:    #key W
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))
    elif k == 115:  #kry S
      xm += math.sin(math.radians(rot))
      zm -= math.cos(math.radians(rot))
    elif k == 39:   #key '
      tilt -= 2.0
      print tilt
    elif k == 47:   #key /
      tilt += 2.0
    elif k == 97:   #key A
      rot -= 2
    elif k == 100:  #key D
      rot += 2
    elif k == 112:  #key P
      screenshot("BuckfastAbbey"+str(scshots)+".jpg")
      scshots += 1
    elif k == 27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
quit()
