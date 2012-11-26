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
from pi3d.Display import Display
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light

from pi3d.shape.Model import Model
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
display = Display()
display.create3D(50,50,display.max_width-100,display.max_height-100)   	# x,y,width,height
display.setBackColour(0.2,0.4,0.6,1)    # r,g,b,alpha

# load model_loadmodel
mymodel = Model('models/Triceratops/Triceratops.egg',
                'Triceratops', 0, -1, 0, -90, 0, 0, .005, .005, .005)

# Fetch key presses
mykeys = Keyboard()

# mastrix and rotate variables
rot=0

#create a light
mylight = Light(0,1,1,1,'',10,10,0)
mylight.on()

while 1:
  display.clear()

  Utility.load_identity()
  Utility.translatef(0,0, -40)
  Utility.rotatef(rot, 0, 1, 0)
  rot += 3

  mymodel.draw()

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot('Triceratops.jpg')
    elif k==27:
      mykeys.close()
      display.destroy()
      break
    else:
      print k

  display.swapBuffers()
