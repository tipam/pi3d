# Rotating box example using pi3d module
# ======================================
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

import pi3d,math,random

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,800,600)   	# x,y,width,height
display.setBackColour(0,0.2,0.4,1)    	# r,g,b,alpha

# Create shapes
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mymap = pi3d.createElevationMapFromTexture("Mountains",0.0,0.0,0.0,"Textures/testislands.jpg",mapwidth,mapdepth,mapheight) #mountainsHgt128.png
#mycube = pi3d.createCuboid("cb1",5,4,4.0)
myplane = pi3d.createPlane("myp",5,3,0,1.5,0)
mymerge = pi3d.createMergeShape("merge")
for v in range(0,50):
    x=random.random()*mapwidth*.9-mapwidth*.5
    z=random.random()*mapdepth*.9-mapdepth*.5
    y=mymap.calcHeight(-x,-z)
    mymerge.merge(myplane, x,y,z, 0,0,0, 1,random.random()*4+2,1)


#print "indices",mymerge.shape[1][0],mymerge.shape[1][1],mymerge.shape[1][2]


# Load textures
mountimg1 = pi3d.loadTexture("Textures/mountains3_256.jpg")
palmimg = pi3d.loadTextureAlpha("Textures/palm.png")
coffimg = pi3d.loadTexture("Textures/COFFEE.PNG")

rot=0.0
xm=0.0
ym=2.0
zm=0.0
mymap.translate(xm,0,zm)

# Fetch key presses
mykeys = pi3d.key()

# Display scene and rotate cuboid
while 1:
    #break
    display.clear()

    #pi3d.sprite(starsimg, 0,0,-20, 20,20,rot)
    #rot=rot+0.02
    
    pi3d.resetMatrices()
    pi3d.rotate(0,rot,0)
    pi3d.position(xm,ym,zm)
    mymap.draw(mountimg1)
    #mycube.draw(coffimg)
    
    #mymerge.draw(0,coffimg)
    #mymerge.draw(1,coffimg)
    mymerge.drawAll(palmimg)
    #mymap.rotateIncY(0.05)
    #mymap.rotateIncX(0.01)

    #Press ENTER to terminate
    k = mykeys.read()
    if k >-1:
	if k==119:
	    xm-=math.sin(rot/57.29)
	    zm+=math.cos(rot/57.29)
	    ym = -(mymap.calcHeight(xm,zm)+2.0)
	elif k==115:
	    xm+=math.sin(rot/57.29)
	    zm-=math.cos(rot/57.29)
	    ym = -(mymap.calcHeight(xm,zm)+2.0)
	elif k==97:
	    rot -= 2
	    #mymap.rotY=rot
	    #mymap.rotateToY(rot)
	elif k==100:
	    rot += 2
	elif k==112:
	    display.screenshot("screen3D.jpg")
	else:
	    print k
	#pi3d.screenshot("screenshot3d.jpg")
	    #mymap.rotateToY(rot)
	#	display.destroy()
	#	break
	#print k
    
    display.swapBuffers()
