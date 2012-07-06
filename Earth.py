# Earth and example shapes using pi3d module
# ==========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 03Jul12
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
display.create3D(100,100,1200,900)   	# x,y,width,height
display.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Load textures

# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = pi3d.loadTextureAlpha("Textures/earth_clouds.png",True)   

earthimg = pi3d.loadTexture("Textures/world_map256x256.jpg")
starsimg = pi3d.loadTexture("Textures/stars.jpg")
coffimg = pi3d.loadTexture("Textures/COFFEE.PNG")
	
mysphere = pi3d.createSphere(2,24,24,0.0,"earth",0,0,-7)
mysphere2 = pi3d.createSphere(2.05,24,24,0.0,"clouds",0,0,-7)

myspiral = pi3d.createSpiral(0.4,0.1,12,24,1.5,3.0,"spiral", 0,0,-4)
mytube = pi3d.createTube(0.3,0.2,1.5,24,"tube",-2,0,-5)

arialFont = pi3d.font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
destineFont = pi3d.font("AR_Destine", "#0055ff")

path = ((-0.5, 1),(0.5,0),(0.5,-0.2),(-0.5,-0.3))
myextrude = pi3d.createExtrude(path, 0.05,"Extrude",2.0,0,-5)
# Fetch key presses
mykeys = pi3d.key()

mymatrix=pi3d.matrix()
rot=0.0

# Display scene
while 1:
    display.clear()

    pi3d.sprite(starsimg, 0,0,-20, 20,20,rot)
    rot=rot+0.02
    
    mymatrix.identity()
    mymatrix.push()
    mysphere.draw(earthimg)
    mysphere.rotateIncY( 0.1 )
    mymatrix.pop()

    mymatrix.push()
    mysphere2.draw(cloudimg)
    mysphere2.rotateIncY( .2 )
    mymatrix.pop()
    
    mymatrix.push()
    myspiral.draw(coffimg)
    myspiral.rotateIncY(2)
    myspiral.rotateIncZ(1)
    mymatrix.pop()
    
    mymatrix.push()
    mytube.draw(coffimg)
    mytube.rotateIncY(2)
    mytube.rotateIncZ(1)
    mymatrix.pop()
    
    mymatrix.push()
    myextrude.draw(earthimg,starsimg,coffimg)
    myextrude.rotateIncY(-2)
    myextrude.rotateIncX(1)
    mymatrix.pop()
    
    pi3d.drawString(arialFont,"The Raspberry Pi ROCKS!",-1.0,0.0,-2.2, 10.0, 0.003,0.003)
    pi3d.drawString(destineFont,"Some nice OpenGL bitmap fonts to play with",-1.3,-0.3,-2.2, 10.0, 0.002,0.002)
    
    k = mykeys.read()
    if k >-1:
	if k==112: display.screenshot("earthPic.jpg")
	elif k==27:
	    display.destroy()
	    break
	else:
	    print k

    display.swapBuffers()
