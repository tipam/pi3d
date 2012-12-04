# Tiger Tank in TK window
# Version 0.02 - 23Nov12

import math, random, time

from pi3d import *

from pi3d import Display
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Fog import Fog
from pi3d.context.Light import Light

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model

from pi3d.util import Draw
from pi3d.util import Log
from pi3d.util.Matrix import Matrix
from pi3d.util.TkWin import TkWin

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0   	#64MB GPU memory setting
#winw,winh,bord = 1920,1080,0	#128MB GPU memory setting
win = TkWin(None, "Mega Space Station in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived

display = Display.create(x=win.winx, y=win.winy, w=winw, h=winh - bord,
                         far=2200.0, background=(0.4, 0.8, 0.8, 1))

ectex = EnvironmentCube.loadECfiles("textures/ecubes/RedPlanet", "redplanet_256", "png", True)
myecube = EnvironmentCube.EnvironmentCube(1800.0,"FACES")


# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
redplanet = Texture("textures/mars_colour.png")
mymap = ElevationMap("textures/mars_height.png",mapwidth,mapdepth,mapheight,64,64)

#Load Corridors sections

x,z = 0,0
y = mymap.calcHeight(-x,-z)
cor_win = Model("models/MegaStation/corridor_win_lowpoly.egg", "", x,y,z, -90,0,0, .1,.1,.1)
corridor = Model("models/MegaStation/corridor_lowpoly.egg", "", x,y,z, -90,0,0, .1,.1,.1)
cor_cross = Model("models/MegaStation/cross_room.egg", "", x,y,z, -90,0,0, .1,.1,.1)
cor_cross_doors = Model("models/MegaStation/cross_room_doors.egg", "", x,y,z, -90,0,0, .1,.1,.1)
cor_bend = Model("models/MegaStation/bend_lowpoly.egg", "", x,y,z, -90,0,0, .1,.1,.1)

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
mymouse = Mouse()
mymouse.start()
mtrx = Matrix()

omx=mymouse.x
omy=mymouse.y

myfog = Fog(0.001,(0.65,0.1,0.3,0.5))
mylight = Light(0,1,1,1,"",100,100,100) #, .9,.7,.6)


# Update display before we begin (user might have moved window)
win.update()
display.resize(win.winx, win.winy, win.width, win.height - bord)

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

    Draw.lodDraw3xyz(-xm,-ym,-zm,0,0,0,opendist,cor_cross,1000,cor_cross_doors)
    cor_win.moveAndDraw(0,0,-spc*1.5)
    corridor.moveAndDraw(0,0,-spc*2.5)
    cor_win.moveAndDraw(0,0,-spc*3.5)
    Draw.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*5,opendist,cor_cross,1000,cor_cross_doors)
    cor_win.moveAndDraw(0,0,-spc*6.5)
    Draw.lodDraw3xyz(-xm,-ym,-zm,0,0,-spc*8,opendist,cor_cross,1000,cor_cross_doors)
    cor_win.moveAndDraw(-spc*1.5,0,-spc*5, 0,90,0)
    cor_bend.moveAndDraw(-spc*2.5,0,-spc*5, 0,90,0)
    Draw.lodDraw3xyz(-xm,-ym,-zm,-spc*2.6,0,-spc*6.6,opendist,cor_cross,1000,cor_cross_doors)
    cor_win.moveAndDraw(spc*1.5,0,-spc*5, 0,90,0)
    corridor.moveAndDraw(spc*2.5,0,-spc*5, 0,90,0)
    Draw.lodDraw3xyz(-xm,-ym,-zm,spc*4,0,-spc*5,opendist,cor_cross,1000,cor_cross_doors)


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


#except Exception:
#    texs.deleteAll()
#    display.destroy()
#    win.destroy()
#    print "Bye bye!"
#    #pass # avoid errors when closed

