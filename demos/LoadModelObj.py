# Loading EGG model
# =================
# This example - Copyright (c) 2012 - Tim Skillman
# OBJ loader code by Paddy Gaunt, Copyright (c) 2012
# Version 0.01 - 08Nov12
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

from pi3d.Display import Display
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light

from pi3d.shape.Model import Model

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
display = Display()
display.create3D(100, 100, 1200, 900)    # x,y,width,height
display.setBackColour(0.2, 0.4, 0.6, 1)      # r,g,b,alpha


# load model_loadmodel
mymodel = Model('models/teapot.obj' ,'teapot', 0, -1.0, 0)

# Fetch key presses
mykeys = Keyboard()

# setup matrices
mtrx = Matrix()

#create a light
mylight = Light(0,1,1,1,'',10,10,0)
mylight.on()

while 1:
  display.clear()

  mtrx.identity()
  mtrx.translate(0,2,-5)

  mymodel.draw()
  mymodel.rotateIncY(1.0)
  mymodel.rotateIncX(1.3)

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      display.destroy()
      break
    else:
      print k

  display.swapBuffers()
