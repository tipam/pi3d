# Raspberry Rain example using pi3d module
# ========================================
# Copyright (c) 2012 - Tim Skillman
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
# Rasperry rain demonstrates pi3d sprites over the desktop.
# The sprites make use of the z value in a perspective view

import time, random
import pi3d

# Setup display and initialise pi3d
display = pi3d.glDisplay()
display.create(0,0,1900,1200)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.7,1,0)    

# Load textures
raspimg = pi3d.load_textureAlpha("Textures/Raspi256x256.png")
	
pino=20

# Setup array of random x,y,z coords and initial rotation
xyz=[]
for b in range (0, pino):
    xyz.append((random.random()*8-4,random.random() * 8,random.random() * 6 + 5, random.random() * 360))

# Display scene and rotate cuboid
while 1:
    display.clear()

    for b in range (0, pino):
	pi3d.sprite(raspimg,xyz[b][0],5-xyz[b][1],-xyz[b][2],1,1,xyz[b][3])	#draw a rectangle(x,y,z,scaleX,scaleY,rotation)
	r = xyz[b][3]+1
	y = (xyz[b][1]+0.1) % 10
	if y<0.06:
	    xyz[b] = ((random.random()*8-4, y, xyz[b][2], r))
	else:
	    xyz[b] = ((xyz[b][0], y, xyz[b][2], r))
    
    display.swap_buffers()
    #time.sleep(0.01)
