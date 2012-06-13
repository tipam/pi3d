# 3D clouds
# Copyright (c) Tim Skillman 2012

import pi3d, sys, random, time

z=0
x=0
speed=1
widex=60
widey = 8
cloudno = 50
cloud_depth = 60.0

zd = cloud_depth / cloudno

def drawCloud(c, xx,zz):
    zzz=(zz+c[2]) % cloud_depth
    xxx=(xx+c[0])
    #if xxx>widex*.5: xxx=xxx-widex
    pi3d.rectangle(clouds[c[3]], xxx,c[1],-zzz,0, 8,5)
    
# Setup display and initialise pi3d
scnx = 1920
scny = 1100
display = pi3d.glDisplay()
display.create(0,0,scnx,scny)
display.setBackColour(0,0.7,1,1)

clouds = []
clouds.append(pi3d.load_textureAlpha("cloud2.png"))
clouds.append(pi3d.load_textureAlpha("cloud3.png"))
clouds.append(pi3d.load_textureAlpha("cloud4.png"))
clouds.append(pi3d.load_textureAlpha("cloud5.png"))
clouds.append(pi3d.load_textureAlpha("cloud6.png"))

# Setup cloud positions and cloud image refs
z = 0.0
cxyz = []
for b in range (0, cloudno):
	cxyz.append((random.random() * widex - widex*.5, -random.random() * widey, cloud_depth-z, int(random.random() * 4) + 1))
	z = z + zd  #(z+random.random() * 100) % 1000
	
zc = 0

while True:
	
	display.clear()
	
	# Clear the drawing area with my background sprite or drawing a rectangle		

	#pi3d.rectangle(cloud1, 0,0,-10, 2,1)
	
	z = (z+(cloud_depth-speed)) % cloud_depth
	#zc = int((z/1000) * cloudno)
	zc = (zc + (cloudno-1)) % cloudno
	#zc = (zc + 1) % cloudno
	#x=(x+.1) % widex

	for d in range (zc, cloudno):
		#b = d #% cloudno #cloudno - d - 1
		drawCloud(cxyz[d],x,z)
		
		#if ((cxyz[b][0]+z) % cloud_depth) < speed:
		#	cxyz[b] = (random.random() * widex - widex*.5, cxyz[b][1], cxyz[b][2], cxyz[b][3])
	
	for d in range (0, zc):
		#b = d #% cloudno #cloudno - d - 1
		drawCloud(cxyz[d],x,z)
		
	display.swap_buffers()
	time.sleep(0.01)
