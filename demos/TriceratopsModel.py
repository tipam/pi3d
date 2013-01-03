# Loading EGG model
# =================
# This example - Copyright (c) 2012 - Tim Skillman
# EGG loader code by Paddy Gaunt, Copyright (c) 2012
# Version 0.02 - 20Jul12
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

from pi3d.util import Utility
from pi3d import Display
from pi3d.Keyboard import Keyboard

from pi3d.Camera import Camera
from pi3d.Shader import Shader
from pi3d.context.Light import Light

from pi3d.shape.Model import Model
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50, w=-100, h=-100);
DISPLAY.set_background(0.2,0.4,0.6,1)    # r,g,b,alpha

camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.width/1000.0, DISPLAY.height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_light")
#========================================

# load model_loadmodel
mymodel = Model(camera, light, 'models/Triceratops/Triceratops.egg',
                'Triceratops', 0, -1, 40, 0, 0, 0, .005, .005, .005)
mymodel.set_shader(shader)

# Fetch key presses
mykeys = Keyboard()

while 1:
  DISPLAY.clear()

  mymodel.draw()
  mymodel.rotateIncZ(1)
  mymodel.rotateIncX(-0.317543)
  mymodel.rotateIncY(0.11)

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot('Triceratops.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
