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
clouds.append(pi3d.loadTextureAlpha("Textures/cloud2.png",True))
clouds.append(pi3d.loadTextureAlpha("Textures/cloud3.png",True))
clouds.append(pi3d.loadTextureAlpha("Textures/cloud4.png",True))
clouds.append(pi3d.loadTextureAlpha("Textures/cloud5.png",True))
clouds.append(pi3d.loadTextureAlpha("Textures/cloud6.png",True))

# Setup cloud positions and cloud image refs
z = 0.0
cxyz = []
for b in range (0, cloudno):
	cxyz.append((random.random() * widex - widex*.5, -random.random() * widey, cloud_depth-z, int(random.random() * 4) + 1))
	z = z + zd
	
zc = 0

# Fetch key presses
mykeys = pi3d.key()

while True:
	
	display.clear()
	
	z = (z+(cloud_depth-speed)) % cloud_depth	
	zc = (zc + (cloudno-1)) % cloudno

	#attempts to resolve z-sorting of clouds
	for d in range (zc, cloudno):
		pi3d.sprite(clouds[cxyz[d][3]], x+cxyz[d][0],cxyz[d][1],-((z+cxyz[d][2]) % cloud_depth),8,5)
			
	for d in range (0, zc):
		pi3d.sprite(clouds[cxyz[d][3]], x+cxyz[d][0],cxyz[d][1],-((z+cxyz[d][2]) % cloud_depth),8,5)

	#Press ESCAPE to terminate
	if mykeys.read() == 27:       
	    display.destroy()
	    break
		
	display.swapBuffers()
	time.sleep(0.01)
