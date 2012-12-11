# MarsStation in TK window
# ========================
# Tim Skillman, copright (c) 2012
# Version 0.02 - 23Nov12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi


import pi3d,math,random, time

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winx,winy,winw,winh = 360,150,1200,800          #64MB GPU memory setting
#winx,winy,winw,winh = 0,0,1920,1080            #128MB GPU memory setting
win = pi3d.tkwin("Mars Station in Pi3D",winx,winy,winw,winh)
win.update()  #requires a window update first so that window sizes can be retreived

# Setup display and initialise pi3d viewport over the window
display = pi3d.display(winx,winy,winw,winh,24,0.5,2200,60)
display.setBackColour(0.4,0.8,0.8,1)            # r,g,b,alpha

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
corridor_win = pi3d.loadModel("models/MarsStation/corridor_win_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
corridor = pi3d.loadModel("models/MarsStation/corridor_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
corridor_bend = pi3d.loadModel("models/MarsStation/bend_lowpoly.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
#LOD models
room_hipoly = pi3d.loadModel("models/MarsStation/cross_room.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)
room_lopoly = pi3d.loadModel("models/MarsStation/cross_room_doors.egg",texs,"", x,y,z, -90,0,0, .1,.1,.1)

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

try:
    while 1:
            
        display.clear()

        mtrx.identity()
        #tilt can be used as a means to prevent the view from going under the landscape!
        if tilt<-1: sf=1.0/-tilt
        else: sf=1.0
        mtrx.rotate(tilt,0,0)           #Tilt scene

        #draw scene
        mtrx.rotate(0,mouserot,0)
        mylight.on()

        mtrx.translate(xm,ym-4,zm)      #translate rest of scene relative to tank position
        myfog.on()
        mymap.draw(redplanet)           #Draw the landscape
                
        pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,0,opendist,room_hipoly,1000,room_lopoly)
        corridor_win.draw(None,None,0,0,-spc*1.5)
        corridor.draw(None,None,0,0,-spc*2.5)
        corridor_win.draw(None,None,0,0,-spc*3.5)
        pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*5,opendist,room_hipoly,1000,room_lopoly)
        corridor_win.draw(None,None,0,0,-spc*6.5)
        pi3d.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*8,opendist,room_hipoly,1000,room_lopoly)
        corridor_win.draw(None,None,-spc*1.5,0,-spc*5, 0,90,0)
        corridor_bend.draw(None,None,-spc*2.5,0,-spc*5, 0,90,0)
        pi3d.lodDraw3xyz(-xm,-ym,-zm,-spc*2.6,0,-spc*6.6,opendist,room_hipoly,1000,room_lopoly)
        corridor_win.draw(None,None,spc*1.5,0,-spc*5, 0,90,0)
        corridor.draw(None,None,spc*2.5,0,-spc*5, 0,90,0)
        pi3d.lodDraw3xyz(-xm,-ym,-zm,spc*4,0,-spc*5,opendist,room_hipoly,1000,room_lopoly)

        mylight.off()
        myfog.off()

        #Draw environment cube
        myecube.draw(ectex,xm,ym,zm)

        #update mouse/keyboard input
        mx=mymouse.x
        my=mymouse.y

        mouserot += (mx-omx)*0.2
        tilt -= (my-omy)*0.2
        omx=mx
        omy=my
                        

        display.swapBuffers()

        # Handle window events
        # Press ESCAPE to terminate
        win.update()

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
                    display.screenshot("MarsStation.jpg")
                elif win.key=="Escape":
                    texs.deleteAll()
                    display.destroy()
                    win.shutdown()
                    print "Bye bye!"
                    break
                
        if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
		# would be nice if wheel worked!
                xm-=math.sin(mouserot*rads)*2
                zm+=math.cos(mouserot*rads)*2

        win.ev=""  #clear the event so it doesn't repeat


except Exception:
    texs.deleteAll()
    display.destroy()
    win.shutdown()
    print "Bye bye!"
    pass # avoid errors when closed
    
