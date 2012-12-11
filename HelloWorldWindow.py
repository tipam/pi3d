# Hello World example in a window using pi3d module
# =================================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.01 - 08Dec12
# 
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi

import pi3d

#Create a Tkinter window
winx,winy,winw,winh = 200,200,800,600
win = pi3d.tkwin("Hello world in a Window",winx,winy,winw,winh)
win.update() #show window now (with default splash)

# Setup display and initialise pi3d
display = pi3d.display(winx,winy,winw,winh)
display.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Load textures
texs=pi3d.textures()
cloudimg = texs.loadTexture("textures/earth_clouds.png",True)   
earthimg = texs.loadTexture("textures/world_map.jpg")

# Create shapes
mysphere = pi3d.createSphere(2,24,24,0.0,"earth",0,0,-6)
mysphere2 = pi3d.createSphere(2.05,24,24,0.0,"clouds",0,0,-6)

#create a light
mylight = pi3d.createLight(0,1,1,1,"",10,10,50, .8,.8,.8)
mylight.on()

# Display scene
try:
    while 1:
	#Display scene
	display.clear()
	   
	mysphere.draw(earthimg)
	mysphere.rotateIncY( 0.1 )
	mysphere2.draw(cloudimg)
	mysphere2.rotateIncY( .2 )
	
	display.swapBuffers()

        #Handle window events
        win.update()
        if win.ev=="key":  
            if win.key=="Escape":
                texs.deleteAll()
                display.destroy()
                win.shutdown()
                break
        if win.ev=="resized":
            display.resize(win.winx,win.winy,win.width,win.height)
            win.resized=False  #this flag must be set otherwise no further events will be detected
        win.ev=""  #clear the event so it doesn't repeat

except Exception:
    texs.deleteAll()
    display.destroy()
    win.shutdown()
    print "Bye bye!"
