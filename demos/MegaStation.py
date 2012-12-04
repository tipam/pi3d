# Tiger Tank in TK window
# Version 0.02 - 23Nov12
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

import pi3d, math, random, time

from pi3d import Display
from pi3d.Texture import Texture

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0   	#64MB GPU memory setting
#winw,winh,bord = 1920,1080,0	#128MB GPU memory setting
win = pi3d.tkwin(None,"Mega Space Station in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived
display = pi3d.display()
display.create3D(win.winx,win.winy,winw,winh-bord, 0.5, 2200.0, 60.0)   	# x,y,width,height,near,far,aspect,zdepth
display.setBackColour(0.4,0.8,0.8,1)    	# r,g,b,alpha

#texture storage for loading textures
texs = pi3d.textures()
ectex=pi3d.loadECfiles("textures/ecubes/RedPlanet","redplanet_256","png",texs,True)
myecube = pi3d.createEnvironmentCube(1800.0,"FACES")


# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
redplanet = texs.loadTexture("textures/mars_colour.png")
mymap = pi3d.createElevationMapFromTexture("textures/mars_height.png",mapwidth,mapdepth,mapheight,64,64)

#Load Corridors sections

x,z = 0,0
y = mymap.calcHeight(-x,-z)
cor_win = pi3d.loadModel("models/MegaStation/corridor_win_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
corridor = pi3d.loadModel("models/MegaStation/corridor_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
cor_cross = pi3d.loadModel("models/MegaStation/cross_room.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
cor_cross_doors = pi3d.loadModel("models/MegaStation/cross_room_doors.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
cor_bend = pi3d.loadModel("models/MegaStation/bend_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)

#position vars
mouserot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)
spc = 39.32
opendist = 120

# Fetch key presses
mymouse = pi3d.mouse()
mymouse.start()
mtrx = pi3d.matrix()

omx=mymouse.x
omy=mymouse.y

myfog = pi3d.fog(0.001,(0.65,0.1,0.3,0.5))
mylight = pi3d.createLight(0,1,1,1,"",100,100,100) #, .9,.7,.6)


# Update display before we begin (user might have moved window)
win.update()
display.resize(win.winx,win.winy,win.width,win.height-bord)

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
	mylight.on()

	mtrx.translate(xm,ym-4,zm)	#translate rest of scene relative to tank position
	myfog.on()
	mymap.draw(redplanet)		#Draw the landscape

	pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,0,opendist,cor_cross,1000,cor_cross_doors)
	cor_win.draw(None,None,0,0,-spc*1.5)
	corridor.draw(None,None,0,0,-spc*2.5)
	cor_win.draw(None,None,0,0,-spc*3.5)
	pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*5,opendist,cor_cross,1000,cor_cross_doors)
	cor_win.draw(None,None,0,0,-spc*6.5)
	pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*8,opendist,cor_cross,1000,cor_cross_doors)
	cor_win.draw(None,None,-spc*1.5,0,-spc*5, 0,90,0)
	cor_bend.draw(None,None,-spc*2.5,0,-spc*5, 0,90,0)
	pi3d.lodDraw3xyz(-xm,-ym,-zm,-spc*2.6,0,-spc*6.6,opendist,cor_cross,1000,cor_cross_doors)
	cor_win.draw(None,None,spc*1.5,0,-spc*5, 0,90,0)
	corridor.draw(None,None,spc*2.5,0,-spc*5, 0,90,0)
	pi3d.lodDraw3xyz(-xm,-ym,-zm,spc*4,0,-spc*5,opendist,cor_cross,1000,cor_cross_doors)


	mylight.off()
	myfog.off()

	myecube.draw(ectex,xm,ym,zm)#Draw environment cube

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
		display.resize(win.winx,win.winy,win.width,win.height-bord)
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
		    display.screenshot("MegaStation.jpg")
		elif win.key=="Escape":
		    texs.deleteAll()
		    display.destroy()
		    win.destroy()
		    print "Bye bye!"
		    break

	if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
		xm-=math.sin(mouserot*rads)*2
		zm+=math.cos(mouserot*rads)*2

	win.ev=""  #clear the event so it doesn't repeat


except Exception:
    texs.deleteAll()
    display.destroy()
    win.destroy()
    print "Bye bye!"
    #pass # avoid errors when closed

