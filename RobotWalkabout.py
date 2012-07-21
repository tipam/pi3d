# Robot walkabout example using pi3d module
# =========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 20Jul12
# 
# Demonstrates offset camera to view an avatar moving about a map.  Also includes tiled mapping on landscape
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

rads = 0.017453292512  # degrees to radians

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1600,800, 0.5, 800.0, 60.0)   	# x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1)    	# r,g,b,alpha

# Load textures
texs = pi3d.textures()
tree2img = texs.loadTexture("textures/tree2.png")
tree1img = texs.loadTexture("textures/tree1.png")
grassimg = texs.loadTexture("textures/grass.png")
hb2img = texs.loadTexture("textures/hornbeam2.png")

#load environment cube
ectex = pi3d.loadECfiles("textures/ecubes","sbox_interstellar",texs)
myecube = pi3d.createEnvironmentCube(900.0,"FACES")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = texs.loadTexture("textures/mars_colour.png")
mymap = pi3d.createElevationMapFromTexture("textures/mars_height.png",mapwidth,mapdepth,mapheight,128,128) #testislands.jpg

#create robot 
metalimg = texs.loadTexture("textures/metalhull.jpg")
robot_head= pi3d.createSphere(2.0,12,12,0.5,"",0,3,0)
robot_body = pi3d.createCylinder(2.0,4,12,"",0,1,0)
robot_leg = pi3d.createCuboid(0.7,4.0,1.0,"",0,0.8,0)

robot = pi3d.createMergeShape()
robot.add(robot_head)
robot.add(robot_body)
robot.add(robot_leg, -2.1,0,0)
robot.add(robot_leg, 2.1,0,0)

#create space station
ssphere = pi3d.createSphere(10,16,16)
scorrid = pi3d.createCylinder(4,22,12)

station = pi3d.createMergeShape("",0,mymap.calcHeight(0,0),0, 0,0,0, 4,4,4)
station.add(ssphere, -20,0,-20)
station.add(ssphere, 20,0,-20)
station.add(ssphere, 20,0,20)
station.add(ssphere, -20,0,20)
station.add(scorrid, -20,0,0, 90,0,0)
station.add(scorrid, 0,0,20, 90,90,0)
station.add(scorrid, 0,0,-20, 90,90,0)

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# Fetch key presses
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()
mtrx = pi3d.matrix()

omx=mymouse.x
omy=mymouse.y

myfog = pi3d.fog(0.002,(0.3,0.8,0.6,0.5))
mylight = pi3d.createLight(0,1,1,1,"",10,10,10, .9,.7,.6)

# Display scene and rotate cuboid
while 1:
    display.clear()
    
    mtrx.identity()
    #tilt can be used as a means to prevent the view from going under the landscape!
    if tilt<-1: sf=1.0/-tilt
    else: sf=1.0
    mtrx.translate(0,-10*sf-5.0,-40*sf)   #zoom camera out so we can see our robot
    mtrx.rotate(tilt,0,0)		#Robot still affected by scene tilt
    
    #draw robot
    mylight.on()
    robot.drawAll(metalimg)
    mylight.off()
    
    mtrx.rotate(0,rot,0)		#rotate rest of scene around robot
    mtrx.translate(xm,ym,zm)	#translate rest of scene relative to robot position
    
    myecube.draw(ectex,xm,ym,zm)#Draw environment cube
    myfog.on()
    mymap.draw(mountimg1)		#Draw the landscape
    station.drawAll(metalimg)
    myfog.off()
    
    mx=mymouse.x
    my=mymouse.y
    
    #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
    rot += (mx-omx)*0.2
    tilt -= (my-omy)*0.2
    omx=mx
    omy=my
		
    #Press ESCAPE to terminate
    k = mykeys.read()
    if k >-1:
	if k==119:    #key W
	    xm-=math.sin(rot*rads)
	    zm+=math.cos(rot*rads)
	    ym = -(mymap.calcHeight(xm,zm)+avhgt)
	elif k==115:  #kry S
	    xm+=math.sin(rot*rads)
	    zm-=math.cos(rot*rads)
	    ym = -(mymap.calcHeight(xm,zm)+avhgt)
	elif k==39:   #key '
		tilt -= 2.0
		print tilt
	elif k==47:   #key /
		tilt += 2.0
	elif k==97:   #key A
	    rot -= 2
	elif k==100:  #key D
	    rot += 2
	elif k==112:  #key P
	    display.screenshot("walkaboutRobot.jpg")
	elif k==27:    #Escape key
		mykeys.close()
		texs.deleteAll()
		display.destroy()
		break
	else:
	    print k
   
    display.swapBuffers()
