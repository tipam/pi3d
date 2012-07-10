# Clouds 3D example using pi3d module
# ===================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 03Jul12
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

import pi3d, random, time

z=0
x=0
speed=1
widex=60
widey = 8
cloudno = 50
cloud_depth = 60.0
zd = cloud_depth / cloudno
    
# Setup display and initialise pi3d
scnx = 800
scny = 600
display = pi3d.display()
display.create3D()
display.setBackColour(0,0.7,1,1)

clouds = []
clouds.append(pi3d.loadTextureAlpha("textures/cloud2.png",True))
clouds.append(pi3d.loadTextureAlpha("textures/cloud3.png",True))
clouds.append(pi3d.loadTextureAlpha("textures/cloud4.png",True))
clouds.append(pi3d.loadTextureAlpha("textures/cloud5.png",True))
clouds.append(pi3d.loadTextureAlpha("textures/cloud6.png",True))

# Setup cloud positions and cloud image refs
z = 0.0
cxyz = []
for b in range (0, cloudno):
	cxyz.append([random.random() * widex - widex*.5, -random.random() * widey, cloud_depth-z, int(random.random() * 4) + 1])
	z = z + zd
	
# Fetch key presses
mykeys = pi3d.key()

while True:
	
	display.clear()
	
	maxDepth = 0
	axDepthIndex = 0
	# this is easier to understand, the z position of each cloud is (only) held in cxyz[][2]
	# it stops the clouds appearing in front of nearer clouds!
	# first go through the clouds to find index of furthest away
	for i in range(len(cxyz)):
	    cxyz[i][2] = (cxyz[i][2] - speed) % cloud_depth
	    if (cxyz[i][2] > maxDepth):
		maxDepth = cxyz[i][2]
		maxDepthIndex = i
		
	# paint the clouds from background to foreground
	for i in range(maxDepthIndex, maxDepthIndex + cloudno):
		c = cxyz[i%cloudno]
		pi3d.sprite(clouds[c[3]], c[0], c[1], -c[2], 8, 5)

	#Press ESCAPE to terminate
	if mykeys.read() == 27:       
	    display.destroy()
	    mykeys.close()
	    break
		
	display.swapBuffers()
	time.sleep(0.01)
