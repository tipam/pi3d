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
cloudimg = pi3d.loadTextureAlpha("textures/earth_clouds.png",True)   
earthimg = pi3d.loadTexture("textures/world_map256x256.jpg")
starsimg = pi3d.loadTexture("textures/stars.jpg")
	
mysphere = pi3d.createSphere(2,24,24,0.0,"earth",0,0,-7)
mysphere2 = pi3d.createSphere(2.05,24,24,0.0,"clouds",0,0,-7)

arialFont = pi3d.font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
destineFont = pi3d.font("AR_DELANEY", "#0055ff")

# Fetch key presses
mykeys = pi3d.key()

rot=0.0

# Display scene
while 1:
    display.clear()

    pi3d.sprite(starsimg, 0,0,-20, 20,20,rot)
    rot=rot+0.02
    
    pi3d.identity()
    mysphere.draw(earthimg)
    mysphere.rotateIncY( 0.1 )

    mysphere2.draw(cloudimg)
    mysphere2.rotateIncY( .2 )
        
    pi3d.drawString(arialFont,"The Raspberry Pi ROCKS!",-1.0,0.0,-2.2, 10.0, 0.003,0.003)
    pi3d.drawString(destineFont,"Some nice OpenGL bitmap fonts to play with!",-1.3,-0.3,-2.2, 10.0, 0.002,0.002)
    
    k = mykeys.read()
    if k >-1:
	if k==112: display.screenshot("earthPic.jpg")
	elif k==27:
	    display.destroy()
	    break
	else:
	    print k

    display.swapBuffers()
