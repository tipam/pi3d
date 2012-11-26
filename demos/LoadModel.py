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
#    $ sudo apt-get install python-imaging
#
# before running this example
#

from pi3d import Display
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light
from pi3d.shape.Model import Model
from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100, w=1200, h=900)
DISPLAY.setBackColour(r=0.2, g=0.4, b=0.6, alpha=1)

# load model_loadmodel
mymodel = Model('models/teapot.egg' ,'teapot', 0,-1,0)

# Fetch key presses
mykeys = Keyboard()

# setup matrices
mtrx = Matrix()

#create a light
mylight = Light(0,1,1,1,'',10,10,0)
mylight.on()

while 1:
  DISPLAY.clear()

  mtrx.identity()
  mtrx.translate(0,0,-10)

  mymodel.draw()
  mymodel.rotateIncY(3.0)

  k = mykeys.read()
  if k >-1:
    if k==112:
      screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
