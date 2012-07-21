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
display.create3D(100,100,1400,800)   	# x,y,width,height
display.setBackColour(0.2,0.4,0.6,1)    	# r,g,b,alpha

print "=============================================================="
print "Instructions:"
print ""
print "Keys-             W - Forward,"
print "        A - Left   S - Back     D - right"
print ""
print "Move mouse to pan view.  Click mouse to exit or press ESCAPE"
print "=============================================================="

texs = pi3d.textures()
ectex = pi3d.loadECfiles("textures/ecubes","sbox",texs)
myecube = pi3d.createEnvironmentCube(900.0,"FACES")

# load model_loadmodel
mymodel = pi3d.loadModel("models/Buckfast Abbey/BuckfastAbbey.egg",texs,"Abbey",0,0,0, -90,160,0, 0.03,0.03,0.03)
	
# Create keyboard and mouse event objects
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()

#screenshot number
scshots = 1  

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -avhgt

#create a light
mylight = pi3d.createLight(0,1,1,1,"",0,200,200,0.4,0.4,0.4)
mtrx=pi3d.matrix()

omx=mymouse.x
omy=mymouse.y
        
while 1:
    display.clear()

    mtrx.identity()
    mtrx.rotate(tilt,rot,0)
    mtrx.translate(xm,ym,zm)
    mtrx.push()
    mtrx.rotate(0,180,0)
    myecube.draw(ectex,xm,ym,zm)
    mtrx.pop()
    
    mylight.on()
    mymodel.draw()
    mylight.off()
    
    mx=mymouse.x
    my=mymouse.y
    
    if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
	rot += (mx-omx)*0.5
	tilt -= (my-omy)*0.5
	omx=mx
	omy=my

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
	elif k==27:    #Escape key
		mykeys.close()
		texs.deleteAll()
		display.destroy()
		break
	else:
	    print k
 
    display.swapBuffers()
