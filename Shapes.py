# Shapes using pi3d module
# ========================
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
texs = pi3d.textures()
patimg = texs.loadTexture("textures/PATRN.PNG")   
coffimg = texs.loadTexture("textures/COFFEE.PNG")

#Create inbuilt shapes
mysphere = pi3d.createSphere(1,24,24,0.0,"sphere",-4,2,-7)
mytcone = pi3d.createTCone(0.8,0.6,1,24,"TCone", -2,2,-7)
myspiral = pi3d.createSpiral(0.4,0.1,12,24,1.5,3.0,"spiral", 0,2,-7)
mytube = pi3d.createTube(0.4,0.1,1.5,24,"tube",2,2,-7, 30,0,0)
myextrude = pi3d.createExtrude( ((-0.5, 1),(0.5,0),(0.5,-0.2),(-0.5,-0.3)), 0.05,"Extrude",4,2,-7)

mycone = pi3d.createCone(1,2,24,"Cone",-4,-1,-7)
mycylinder = pi3d.createCylinder(.7,1.5,24,"Cyli",-2,-1,-7)
myhemisphere = pi3d.createSphere(1,24,24,0.5,"hsphere",0,-1,-7)
mytorus = pi3d.createTorus(1,0.3,12,24,"Torus", 2,-1,-7)
mylathe = pi3d.createLathe( ((1,0),(0.1,0.2),(0.08,0.21),(0.08,1),(0.7,1.2),(0.9, 1.4), (1.1,1.7)), 24,"Cup",4,-1,-7, 0,0,0, 0.8,0.8,0.8)

arialFont = pi3d.font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
destineFont = pi3d.font("AR_Destine", "#0055ff")


# Fetch key presses
mykeys = pi3d.key()

#create a light
mylight = pi3d.createLight(0,1,1,1,"",10,10,10)
mylight.on()

# Display scene
while 1:
    display.clear()
    
    mysphere.draw(patimg)
    mysphere.rotateIncY( 0.5 )

    myhemisphere.draw(coffimg)
    myhemisphere.rotateIncY( .5 )

    myspiral.draw(patimg)
    myspiral.rotateIncY(3)
    myspiral.rotateIncZ(1)
    
    mytube.draw(coffimg)
    mytube.rotateIncY(3)
    mytube.rotateIncZ(2)
    
    myextrude.draw(coffimg,patimg,coffimg)
    myextrude.rotateIncY(-2)
    myextrude.rotateIncX(2)

    mycone.draw(coffimg)
    mycone.rotateIncY(-2)
    mycone.rotateIncZ(1)

    mycylinder.draw(patimg)
    mycylinder.rotateIncY(2)
    mycylinder.rotateIncZ(1)

    mytcone.draw(coffimg)
    mytcone.rotateIncY(2)
    mytcone.rotateIncZ(-1)

    mytorus.draw(patimg)
    mytorus.rotateIncY(3)
    mytorus.rotateIncZ(1)

    mylathe.draw(patimg)
    mylathe.rotateIncY(2)
    mylathe.rotateIncZ(1)
    
    pi3d.drawString(arialFont,"Raspberry Pi ROCKS!",-0.8,-0.7,-2.2, 10.0, 0.003,0.003)
    #pi3d.drawString(destineFont,"Some nice OpenGL bitmap fonts to play with",-1.3,-0.3,-2.2, 10.0, 0.002,0.002)
    
    k = mykeys.read()
    if k >-1:
	if k==112: display.screenshot("shapesPic.jpg")
	elif k==27:
	    mykeys.close()
	    texs.deleteAll()
	    display.destroy()
	    break
	else:
	    print k

    display.swapBuffers()
