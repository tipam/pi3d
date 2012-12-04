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

import pi3d,math,random, time

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0     #64MB GPU memory setting
#winw,winh,bord = 1920,1200,0   #128MB GPU memory setting
win = pi3d.tkwin(None,"Tiger Tank demo in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived
display = pi3d.display()
display.create3D(win.winx,win.winy,winw,winh-bord, 0.5, 2200.0, 60.0)           # x,y,width,height,near,far,aspect,zdepth
display.setBackColour(0.4,0.8,0.8,1)            # r,g,b,alpha

#texture storage for loading textures
texs = pi3d.textures() 
ectex = pi3d.loadECfiles("textures/ecubes/Miramar","miramar_256","png",texs,True)
myecube = pi3d.createEnvironmentCube(1800.0,"FACES")


# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
mountimg1 = texs.loadTexture("textures/mountains3_512.jpg")
#roadway = texs.loadTexture("textures/road5.png")
mymap = pi3d.createElevationMapFromTexture("textures/mountainsHgt2.png",mapwidth,mapdepth,mapheight,64,64) 

#Load tank
tank_body = pi3d.loadModel("models/Tiger/bodylow.egg",texs,"TigerBody", 0,0,0, -90,-90,0, .1,.1,.1)
tank_gun = pi3d.loadModel("models/Tiger/gunlow.egg",texs,"TigerGun", 0,0,0, -90,-90,0, .1,.1,.1, 0,0,0)
tank_turret = pi3d.loadModel("models/Tiger/turretlow.egg",texs,"TigerTurret", 0,0,0, -90,-90,0, .1,.1,.1, 0,0,0)

#Load church
x,z = 20,-320
y = mymap.calcHeight(-x,-z)
church = pi3d.loadModel("models/AllSaints/AllSaints.egg",texs,"church1", x,y,z, -90,0,0, .1,.1,.1)
churchlow = pi3d.loadModel("models/AllSaints/AllSaints-lowpoly.egg",texs,"church2", x,y,z, -90,0,0, .1,.1,.1)

#Load cottages
x,z = 250,-40
y = mymap.calcHeight(-x,-z)
cottages = pi3d.loadModel("models/Cottages/cottages_low.egg",texs,"cottagesLo", x,y,z, -90,-5,0, .1,.1,.1)
#cottagesHi = pi3d.loadModel("models/Cottages/cottages.egg",texs,"cottagesHi", x,y,z, -90,-5,0, .1,.1,.1)

#player tank vars
tankrot=0.0
turrot=0.0
tankroll=0.0     #side-to-side roll of tank on ground
tankpitch=0.0   #too and fro pitch of tank on ground

#position vars
mouserot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

#enemy tank vars
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


try:
    while 1:
                
        display.clear()
        
        mtrx.identity()
        #tilt can be used as a means to prevent the view from going under the landscape!
        if tilt<-1: sf=1.0/-tilt
        else: sf=1.0
        mtrx.translate(0,-10*sf-5.0,-40*sf)   #zoom camera out so we can see our robot
        mtrx.rotate(tilt,0,0)           #Tank still affected by scene tilt
        
        #draw player tank
        mtrx.rotate(0,mouserot,0)
        mylight.on()
        drawTiger(0,0,0,tankrot,tankroll,tankpitch,-turrot,0.0)
        
        mtrx.translate(xm,ym,zm)        #translate rest of scene relative to tank position
        
        myfog.on()
        mymap.draw(mountimg1)           #Draw the landscape
        
        #Draw enemy tank
        etx-=math.sin(etr*rads)
        etz-=math.cos(etr*rads)
        etr+=1.0
        drawTiger(etx,(mymap.calcHeight(-etx,-etz)+avhgt),etz,etr,0,0,etr,0)

        #Draw buildings
        pi3d.lodDraw3(-xm,-ym,-zm,300,church,1000,churchlow)
        cottages.draw()

        mylight.off()
        myfog.off()
        
        myecube.draw(ectex,xm,ym,zm)#Draw environment cube

        #update mouse/keyboard input
        mx,my=mymouse.x,mymouse.y
        mouserot += (mx-omx)*0.2
        tilt -= (my-omy)*0.2
        omx,omy=mx,my
            
        # turns player tankt turret towards center of screen which will have a crosshairs
        if turrot+2.0 < mouserot:
                turrot+=2.0
        if turrot-2.0 > mouserot:
                turrot-=2.0
                
        #Press ESCAPE to terminate
        
        display.swapBuffers()
        
        #Handle window events
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
                display.screenshot("TigerTank.jpg")
            elif win.key=="Escape":
                texs.deleteAll()
                display.destroy()
                win.destroy()
                print "Bye bye!"
                break
        if win.ev=="resized":
            display.resize(win.winx,win.winy,win.width,win.height-bord)
            win.resized=False  #this flag must be set otherwise no further events will be detected

        win.ev=""  #clear the event so it doesn't repeat


except Exception:
    texs.deleteAll()
    display.destroy()
    win.destroy()
    print "Bye bye!"
    #pass # avoid errors when closed
    
