# How to make orbiters
# =================
# This example - Copyright (c) 2012 - Jesse Jaara
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

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D()
display.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Load textures
cloudimg = pi3d.loadTextureAlpha("textures/earth_clouds.png",True)   
earthimg = pi3d.loadTexture("textures/world_map256x256.jpg")
moonimg = pi3d.loadTexture("textures/moon.jpg")

# Init models
Earth = pi3d.createSphere(10,24,24,0.0,"Earth",0,0,0,0,0,23.5)
Moon = pi3d.createSphere(1,24,24,0.0,"Moon",13.8,0,0)
	
#create a light
mylight = pi3d.createLight(0,1,1,1,"Sun",0,0,100)
mylight.on()
    
while 1:
    display.clear()

    pi3d.identity()
    pi3d.position(0,0,-20)
    Earth.rotateIncY(2)
    Earth.draw(earthimg)
    Moon.rotateAroundObject(Earth,"y",0.07)
    Moon.draw(moonimg)
    display.swapBuffers()
