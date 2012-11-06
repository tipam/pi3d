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

import pi3d

from pi3d.Display import Display
from pi3d.Light import Light

from pi3d.shape.Model import Model

# Setup display and initialise pi3d
display = Display()
display.create3D(100,100,1200,900)   	# x,y,width,height
display.setBackColour(0.2,0.4,0.6,1)    	# r,g,b,alpha

# load model_loadmodel
mymodel = Model("models/teapot.egg","teapot", 0,-1,0)

# Fetch key presses
mykeys = pi3d.key()

# setup matrices
mtrx = pi3d.matrix()

#create a light
mylight = Light(0,1,1,1,"",10,10,0)
mylight.on()

while 1:
    display.clear()

    mtrx.identity()
    mtrx.translate(0,0,-10)

    mymodel.draw()
    mymodel.rotateIncY(3.0)
    display.swapBuffers()
