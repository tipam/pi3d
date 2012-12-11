# Tiger Tank in TK window
# =======================
# Version 0.03 - 23Nov12
# By Tim Skillman, copyright(c) 2012
# 
# First tank demo - more to come!
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi

print "=============================================================="
print "        Demo mimics the World Of Tanks online game"
print ""
print "Tank Instructions:"
print ""
print "Keys-              W - Forward,"
print "        A - Left   S - Back     D - right    R - auto-drive"
print ""
print "        Look up with mouse to enter sniper/zoom mode"
print ""
print "        Move mouse to pan view.  Press ESCAPE to exit"
print "=============================================================="

import pi3d,math,random
rads = 0.017453292512  # degrees to radians

# Create a Tkinter window
winx,winy,winw,winh = 360,250,1200,600     #64MB GPU memory setting
#winx,winy,winw,winh = 0,0,1920,1200   	   #128MB GPU memory setting
win = pi3d.tkwin("Tiger Tank demo in Pi3D",winx,winy,winw,winh)
win.update()  #display window now with splash

# Setup display and initialise pi3d viewport over the window
display = pi3d.display(winx,winy,winw,winh)
display.setBackColour(0.7,0.8,0.8,1.0)     # r,g,b,alpha

# texture storage for loading textures
texs = pi3d.textures() 
ectex = pi3d.loadECfiles("textures/ecubes/Miramar","miramar_256","png",texs,True)
myecube = pi3d.createEnvironmentCube(1800.0,"FACES")

# create a font
arialFont = pi3d.font("MicrosoftSansSerif","#88ff88")

# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
mountimg1 = texs.loadTexture("textures/mountains3_512.jpg")
#roadway = texs.loadTexture("textures/road5.png")
mymap = pi3d.createElevationMapFromTexture("textures/mountainsHgt2.png",mapwidth,mapdepth,mapheight,64,64) 

# map dots and settings
dotsize=8
doth=dotsize*.5
reddot = texs.loadTexture("textures/red_ball.png")
grndot = texs.loadTexture("textures/blu_ball.png")
target = texs.loadTexture("textures/target.png")
target.blend = True
sniper = texs.loadTexture("textures/snipermode.png")
sniper.blend = True  #Enable true blending
smaps=200
smph=smaps*.5


# Load tank parts
tank_body = pi3d.loadModel("models/Tiger/body.obj",texs,"TigerBody", 0,0,0, 0,-90,0, .1,.1,.1)
tank_gun = pi3d.loadModel("models/Tiger/gun.obj",texs,"TigerGun", 0,0,0, 0,-90,0, .1,.1,.1, 0,0,0)
tank_turret = pi3d.loadModel("models/Tiger/turret.obj",texs,"TigerTurret", 0,0,0, 0,-90,0, .1,.1,.1, 0,0,0)

# Load church (high/low detail)
x,z = 20,-320
y = mymap.calcHeight(-x,-z)
church = pi3d.loadModel("models/AllSaints/AllSaints.obj",texs,"church1", x,y,z, 0,0,0, .1,.1,.1)
churchlow = pi3d.loadModel("models/AllSaints/AllSaints-lowpoly.obj",texs,"church2", x,y,z, 0,0,0, .1,.1,.1)

# Load cottages
x,z = 250,-40
y = mymap.calcHeight(-x,-z)
cottages = pi3d.loadModel("models/Cottages/cottages_low.obj",texs,"cottagesLo", x,y,z, 0,-5,0, .1,.1,.1)
#cottagesHi = pi3d.loadModel("models/Cottages/cottages.egg",texs,"cottagesHi", x,y,z, -90,-5,0, .1,.1,.1)

# player tank vars
tankrot=0.0
turrot=0.0
tankroll=0.0     #side-to-side roll of tank on ground
tankpitch=0.0   #too and fro pitch of tank on ground

# position vars
mouserot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# enemy tank vars
etx=50
etz=90
etr=0.0

# Fetch key presses
mymouse = pi3d.mouse()
mymouse.start()
mtrx = pi3d.matrix()

omx=mymouse.x
omy=mymouse.y

myfog = pi3d.fog(0.0014,(0.7,0.8,0.9,0.5))
mylight = pi3d.createLight(0,1,1,1,"",100,100,100) #, .9,.7,.6)

def drawTiger(x,y,z,rot,roll,pitch,turrot,gunangle):    
        tank_body.draw(None,None,x,y,z,pitch,rot,roll)
        tank_turret.draw(None,None,x,y,z,pitch,turrot,roll)
        tank_gun.draw(None,None,x,y,z,pitch,turrot,roll)

fps=pi3d.FPS()
smode=False
pc=1
autodrive=False

try:
    while 1:
		
	display.clear()
	
	#tilt can be used as a means to prevent the view from going under the landscape!
	if tilt<-1:
	    #go into sniper mode
	    sf=1.0/-tilt
	    smode=True
	    display.setPerspective(0.5, 2200.0, 20.0)
	else:
	    #go into normal mode
	    display.setPerspective(0.5, 2200.0, 60.0)
	    sf=1.0
	    smode=False

	mtrx.identity()
	mtrx.translate(0,-10*sf-5.0,-40*sf)   #zoom camera out so we can see our robot
	mtrx.rotate(tilt,0,0)           #Tank still affected by scene tilt
	
	# Draw player tank
	if autodrive:
	    xm+=math.sin(tankrot*rads)*2
	    zm+=math.cos(tankrot*rads)*2
	    ym = -(mymap.calcHeight(xm,zm)+avhgt)
		
	mtrx.rotate(0,mouserot,0)
	mylight.on()
	if smode==False: drawTiger(0,0,0,tankrot,tankroll,tankpitch,-turrot,0.0)
	
	mtrx.translate(xm,ym,zm)        #translate rest of scene relative to tank position
	
	myfog.on()
	mymap.draw(mountimg1)           #Draw the landscape
	
	# Draw enemy tank
	etx-=math.sin(etr*rads)
	etz-=math.cos(etr*rads)
	etr+=1.0
	drawTiger(etx,(mymap.calcHeight(-etx,-etz)+avhgt),etz,etr,0,0,etr,0)

	# Draw buildings
	pi3d.lodDraw3(-xm,-ym,-zm,300,church,1000,churchlow)
	cottages.draw()

	mylight.off()
	myfog.off()
	
	# Draw environment cube
	myecube.draw(ectex,xm,ym,zm)

	# update mouse/keyboard input
	mx,my=mymouse.x,mymouse.y
	mouserot += (mx-omx)*0.2
	tilt -= (my-omy)*0.2
	omx,omy=mx,my
	    
	# turns player tank turret towards center of screen which will have a crosshairs
	if turrot+2.0 < mouserot:
		turrot+=2.0
	if turrot-2.0 > mouserot:
		turrot-=2.0
	
	# switch to 2D orthographic rendering
	display.setOrthographic()
	
	# Draw Frames Per Second info
	pi3d.drawString2D(arialFont,"FPS:"+str(fps.count()),10,50,20)
	    
	# Draw targetting cross
	pi3d.rectangle(target,display.win_width*.5-64,display.win_height*.5+64,128,128)
	
	# Draw map and tank positions
	mx = display.win_width-smaps
	pi3d.rectangle(grndot,mx+(xm/mapwidth)*smaps+smph-doth,smph+doth-(zm/mapdepth)*smaps,dotsize,dotsize)
	pi3d.rectangle(reddot,mx+(-etx/mapwidth)*smaps+smph-doth,smph+doth-(-etz/mapdepth)*smaps,dotsize,dotsize)
	pi3d.rectangle(mountimg1,mx,smaps,smaps,smaps)
	
	# If in sniper mode, then display sniper overlay
	if smode==True: pi3d.rectangle(sniper,0,display.win_height,display.win_width,display.win_height)
	
	display.swapBuffers()
	
	# Handle window events
	# Press ESCAPE to terminate
	win.update()
	if win.ev=="key":  
	    if win.key=="w":
		xm+=math.sin(tankrot*rads)*2
		zm+=math.cos(tankrot*rads)*2
		ym = -(mymap.calcHeight(xm,zm)+avhgt)
	    elif win.key=="s": 
		xm-=math.sin(tankrot*rads)*2
		zm-=math.cos(tankrot*rads)*2
		ym = -(mymap.calcHeight(xm,zm)+avhgt)
	    elif win.key=="a":   
		tankrot += 2
	    elif win.key=="d":  
		tankrot -= 2
	    elif win.key=="p":  
		display.screenshot("TigerTank"+str(pc)+".jpg")
		pc+=1
	    elif win.key=="r":
		autodrive = not autodrive
	    elif win.key=="Escape":
		texs.deleteAll()
		display.destroy()
		win.shutdown()
		print "Bye bye!"
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


    
