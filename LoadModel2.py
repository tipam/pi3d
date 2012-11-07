# Loading EGG model - clone(), reparentTo() and lights
# ====================================================
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
from math import sin, cos, hypot

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1200,900)      # x,y,width,height
display.setBackColour(0.2,0.4,0.6,1)        # r,g,b,alpha

print "\n\n\rpress escape to stop!\n\n\r"

# load model_loadmodel
mymodel = pi3d.loadModel("models/teapot.egg","teapot", 0,-1,-10)
    
# clone mymodel
myclone = []
mcDirection = []
mcSpeed = []
for i in range(6):
    myclone.append(mymodel.clone())
    # attach myclone[] as appendage to mymodel
    myclone[i].reparentTo(mymodel)
    # position and rotations of myclone[] are now relative to mymodel
    myclone[i].position(0,0,0)
    mcDirection.append(0.52 * i)
    mcSpeed.append(0.01 + i*0.01)

    
# Fetch key presses
mykeys = pi3d.key()

#create a light
mylight = pi3d.createLight(0,3,3,1,"",30,30,-5) # light brighter and further away and yellower
mylight.on()
mylight2 = pi3d.createLight(1,0.1,0.1,0.5,"",-2, 0,-8) # light dimmer and nearer and bluer
mylight2.on()
    
while 1:
    display.clear()

    # Compare model movement with matrix method in LoadModel2.py You can change the object's position and orientation directly which is easier to follow
    # especially if there are reparentTo() objects and clones
    mymodel.rotateIncY(1)
    mymodel.rotateIncX(0.05)
    
    for i in range(len(myclone)):
        myclone[i].x += mcSpeed[i] * sin(mcDirection[i])
        myclone[i].y += mcSpeed[i] * cos(mcDirection[i])
        myclone[i].z += mcSpeed[i] * sin(mcDirection[i]*2)
        myclone[i].rotateIncZ(0.1 * i)
        if (hypot(myclone[i].x, hypot(myclone[i].y, myclone[i].z)) > 4): mcSpeed[i] *= -1 # could get trapped 'outside' by rounding errors

    mymodel.draw()
    
    k = mykeys.read()
    if k >-1:
        if k==27:
            display.destroy()
            mykeys.close()
            break

    display.swapBuffers()
