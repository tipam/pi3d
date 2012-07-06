# Loading EGG model
# =================
# This example - Copyright (c) 2012 - Tim Skillman
# EGG loader code by Paddy Gaunt, Copyright (c) 2012
# Version 0.01 - 03Jul12
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

import pi3d, math

rads = 0.017453292512  # degrees to radians

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1200,900)   	# x,y,width,height
display.setBackColour(0.2,0.4,0.6,1)    	# r,g,b,alpha

ectex = pi3d.loadTexture("Textures/SkyBox.png")
myecube = pi3d.createEnvironmentCube(900.0,"CROSS")

# load model_loadmodel
mymodel = pi3d.loadModel("models/Buckfast Abbey/BuckfastAbbey.egg","Abbey")
	
# Fetch key presses
mykeys = pi3d.key()

#screenshot number
scshots = 1  

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -avhgt
mtrx = pi3d.matrix()

#create a light
mylight = pi3d.createLight(0,1,1,1,"",100,100,0,.8,.8,.8)
    
while 1:
    display.clear()

    mtrx.identity()
    pi3d.rotate(tilt,0,0)
    pi3d.rotate(0,rot,0)
    pi3d.position(xm,ym,zm)
    myecube.draw(ectex,xm,ym,zm)
    mylight.position(0,500,500)
    
    mtrx.push()
    pi3d.scale(0.03,0.03,0.03)
    pi3d.rotate(-90.0,160,0)
    mylight.on()
    mymodel.draw()
    mylight.off()
    mtrx.pop()
    
    #Press ESCAPE to terminate
    k = mykeys.read()
    if k >-1:
	if k==119:    #key W
	    xm-=math.sin(rot*rads)
	    zm+=math.cos(rot*rads)
	elif k==115:  #kry S
	    xm+=math.sin(rot*rads)
	    zm-=math.cos(rot*rads)
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
	    display.screenshot("BuckfastAbbey"+str(scshots)+".jpg")
	    scshots += 1
	elif k==10:   #key RETURN
	    mc = 0
	elif k==27:    #Escape key
		#pi3d.quit()
		display.destroy()
		break
	else:
	    print k
 
    display.swapBuffers()
