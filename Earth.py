# Earth and example shapes using pi3d module
# ==========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.03 - 20Jul12
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
display.create3D(100,100,1600,900)   	# x,y,width,height
display.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Load textures
texs=pi3d.textures()
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = texs.loadTexture("textures/earth_clouds.png",True)   
earthimg = texs.loadTexture("textures/world_map.jpg")
moonimg = texs.loadTexture("textures/moon.jpg")
starsimg = texs.loadTexture("textures/stars2.jpg")
watimg = texs.loadTexture("textures/water.jpg")
	
mysphere = pi3d.createSphere(2,24,24,0.0,"earth",0,0,0)
mysphere2 = pi3d.createSphere(2.05,24,24,0.0,"clouds",0,0,0)
mymoon = pi3d.createSphere(0.4,16,16,0.0,"moon",0,0,0)
mymoon2 = pi3d.createSphere(0.1,16,16,0.0,"moon2",0,0,0)

arialFont = pi3d.font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
destineFont = pi3d.font("AR_DELANEY", "#0055ff")

# Fetch key presses
mykeys = pi3d.key()

mtrx = pi3d.matrix()

rot=0.0
rot1=0.0
rot2=0.0

#create a light
mylight = pi3d.createLight(0,1,1,1,"",10,10,50, .8,.8,.8)

# Display scene
while 1:
    display.clear()
	
    mylight.off()
    pi3d.sprite(starsimg, 0,0,-20, 25,25,rot)
    rot=rot+0.02
    
    mylight.on()
    mtrx.identity()
    mtrx.translate(0,0,-6)
    mysphere.draw(earthimg)
    mysphere.rotateIncY( 0.1 )
    mysphere2.draw(cloudimg)
    mysphere2.rotateIncY( .2 )
    mtrx.rotate(0,0,10)
    mtrx.rotate(0,rot1,0)
    mtrx.translate(4,0,0)
    mymoon.draw(moonimg)
    mymoon.rotateIncY( 0.2 )
    mtrx.rotate(30,0,0)
    mtrx.rotate(0,rot2,0)
    mtrx.translate(0.7,0,0)
    mymoon2.draw(watimg)
    mymoon2.rotateIncY( -20 )
    
    rot1 += 1.0
    rot2 += 5.0
    
    #pi3d.identity()
    #pi3d.drawString(arialFont,"The Raspberry Pi ROCKS!",-1.0,0.0,-2.2, 10.0, 0.003,0.003)
    #pi3d.drawString(destineFont,"Some nice OpenGL bitmap fonts to play with!",-1.3,-0.3,-2.2, 10.0, 0.002,0.002)
    
    k = mykeys.read()
    if k >-1:
	if k==112: display.screenshot("earthPic.jpg")
	elif k==27:
	    mykeys.close()
	    texs.deleteAll()
	    display.destroy()
	    break
	else:
	    print k

    display.swapBuffers()
