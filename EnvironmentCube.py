# Environment Cube examples using pi3d module
# ===========================================
# Copyright (c) 2012 - Tim Skillman
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

import pi3d

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1700,800, 0.5, 800.0, 60.0)   	# x,y,width,height,near,far,aspect

#select the environment cube with 'box'...
box=3
texs=pi3d.textures()
if box==0:
	ectex = texs.loadTexture("textures/ecubes/skybox_interstellar.jpg")
	myecube = pi3d.createEnvironmentCube(900.0,"CROSS")
elif box==1:
	ectex = texs.loadTexture("textures/ecubes/SkyBox.jpg")
	myecube = pi3d.createEnvironmentCube(900.0,"HALFCROSS")
elif box==2:
	ectex=pi3d.loadECfiles("textures/ecubes","sbox_interstellar",texs)
	myecube = pi3d.createEnvironmentCube(900.0,"FACES")
else:
	ectex=pi3d.loadECfiles("textures/ecubes","skybox_hall",texs)
	myecube = pi3d.createEnvironmentCube(900.0,"FACES")


rot=0.0
tilt=0.0

# Fetch key presses
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()
mtrx=pi3d.matrix()

omx=mymouse.x
omy=mymouse.y

# Display scene and rotate cuboid
while 1:
    display.clear()
    
    mtrx.identity()
    mtrx.rotate(tilt,0,0)
    mtrx.rotate(0,rot,0)
    #pi3d.position(xm,ym,zm)
    
    myecube.draw(ectex,0.0,0.0,0.0)

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
	if k==112:  #key P
	    display.screenshot("envcube.jpg")
	elif k==27:    #Escape key
	    mykeys.close()
	    texs.deleteAll()
	    display.destroy()
	    break
	else:
	    print k
   
    display.swapBuffers()
