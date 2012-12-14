# Conference Hall
# Version 0.01 - 03Dec12
# 
# First tank demo - more to come!
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

import pi3d,math,random, time

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winx,winy,winw,winh = 100,100,1200,600   	#64MB GPU memory setting
#winw,winh,bord = 1920,1080,0	#128MB GPU memory setting
win = pi3d.tkwin("Conference Hall using baked textures in Pi3D",winx,winy,winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived
display = pi3d.display(winx,winy,winw,winh,24, 0.5, 2200.0, 60.0)
display.setBackColour(0.4,0.8,0.8,1)    	# r,g,b,alpha

#texture storage for loading textures
texs = pi3d.textures()
ectex=pi3d.loadECfiles("textures/ecubes/Miramar","miramar_256","png",texs,True)
myecube = pi3d.createEnvironmentCube(1800.0,"FACES")

x,y,z = 0,-7,0
hall = pi3d.loadModel("models/ConferenceHall/conferencehall.egg",texs,"Hall", x,y,z, -90.0,0.0,0.0, 0.1,0.1,0.1)

#position vars
mouserot=0.0
tilt=0.0
avhgt = 2.0
xm=5.0
zm=0.0
ym=avhgt
spc = 39.32
opendist = 120

# Fetch key presses
mymouse = pi3d.mouse()
mymouse.start()
mtrx = pi3d.matrix()

omx=mymouse.x
omy=mymouse.y

try:
    while 1:
	    
	display.clear()

	mtrx.identity()
	#tilt can be used as a means to prevent the view from going under the landscape!
	if tilt<-1: sf=1.0/-tilt
	else: sf=1.0
	#mtrx.translate(0,-3,0)   #zoom camera out so we can see our robot
	mtrx.rotate(tilt,0,0)		#Tank still affected by scene tilt

	#draw scene
	mtrx.rotate(0,mouserot,0)

	#mtrx.translate(xm,ym,zm)	#translate rest of scene relative to tank position
		
	hall.draw(None,None,xm,ym,zm)

	myecube.draw(ectex,xm,ym,zm) #Draw environment cube

	#update mouse/keyboard input
	mx=mymouse.x
	my=mymouse.y

	mouserot += (mx-omx)*0.2
	tilt -= (my-omy)*0.2
	omx=mx
	omy=my
			
	#Press ESCAPE to terminate
	display.swapBuffers()

	#Handle window events
	win.update() #resize event takes priority before we grab other events

	if win.ev=="resized":
		print "resized"
		display.resize(win.winx,win.winy,win.width,win.height)
		win.resized=False

	if win.ev=="key":  
		if win.key=="w":
		    xm-=math.sin(mouserot*rads)*2
		    zm+=math.cos(mouserot*rads)*2
		#ym = -(mymap.calcHeight(xm,zm)+avhgt)
		elif win.key=="s": 
		    xm+=math.sin(mouserot*rads)*2
		    zm-=math.cos(mouserot*rads)*2
		#ym = -(mymap.calcHeight(xm,zm)+avhgt)
		elif win.key=="a":   
		    mouserot -= 2
		elif win.key=="d":  
		    mouserot += 2
		elif win.key=="p":  
		    display.screenshot("ConferenceHall.jpg")
		elif win.key=="Escape":
		    texs.deleteAll()
		    display.destroy()
		    win.shutdown()
		    print "Bye bye!"
		    break
	
	win.ev=""  #clear the event so it doesn't repeat


except Exception:
    texs.deleteAll()
    display.destroy()
    win.shutdown()
    print "Bye bye!"
    pass # avoid errors when closed
    
