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

import math, random, time, traceback

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

LOGGER = Log.logger(__name__)

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0     #64MB GPU memory setting
#winw,winh,bord = 1920,1200,0   #128MB GPU memory setting
win = TkWin(None,"Tiger Tank demo in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived
display = Display.create(x=win.winx, y=win.winy, w=winw, h=winh - bord,
                         far=2200.0, background=(0.4, 0.8, 0.8, 1))

#texture storage for loading textures
ectex = EnvironmentCube.loadECfiles("textures/ecubes/Miramar", "miramar_256", suffix="png")
myecube = EnvironmentCube.EnvironmentCube(1800.0, "FACES")

# Create elevation map
mapwidth = 2000.0
mapdepth = 2000.0
mapheight = 100.0
mountimg1 = Texture("textures/mountains3_512.jpg")
#roadway = Texture("textures/road5.png")
mymap = ElevationMap("textures/mountainsHgt2.png",mapwidth,mapdepth,mapheight,64,64)

#Load tank
tank_body = Model("models/Tiger/bodylow.egg", "TigerBody", 0,0,0, -90,-90,0, .1,.1,.1)
tank_gun = Model("models/Tiger/gunlow.egg", "TigerGun", 0,0,0, -90,-90,0, .1,.1,.1, 0,0,0)
tank_turret = Model("models/Tiger/turretlow.egg", "TigerTurret", 0,0,0, -90,-90,0, .1,.1,.1, 0,0,0)

#Load church
x,z = 20,-320
y = mymap.calcHeight(-x,-z)
church = Model("models/AllSaints/AllSaints.egg", "church1", x,y,z, -90,0,0, .1,.1,.1)
churchlow = Model("models/AllSaints/AllSaints-lowpoly.egg", "church2", x,y,z, -90,0,0, .1,.1,.1)

#Load cottages
x,z = 250,-40
y = mymap.calcHeight(-x,-z)
cottages = Model("models/Cottages/cottages_low.egg", "cottagesLo", x,y,z, -90,-5,0, .1,.1,.1)
#cottagesHi = Model("models/Cottages/cottages.egg", "cottagesHi", x,y,z, -90,-5,0, .1,.1,.1)

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
mymouse = Mouse()
mymouse.start()
mtrx = Matrix()

omx=mymouse.x
omy=mymouse.y

myfog = Fog(0.0014,(0.7,0.8,0.9,0.5))
mylight = Light(0,1,1,1,"",100,100,100) #, .9,.7,.6)

def draw(item, x, y, z, pitch, rotation, roll):
  item.x = x
  item.y = y
  item.z = z
  item.rx = pitch
  item.ry = rotation
  item.rz = roll
  item.draw()

def drawTiger(x, y, z, rot, roll, pitch, turret, gunangle):
  draw(tank_body, x, y, z, pitch, rot, roll)
  draw(tank_turret, x, y, z, pitch, turret, roll)
  draw(tank_gun, x, y, z, pitch, turret, roll)

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
  Draw.lodDraw3(-xm, -ym, -zm, 300, church, 1000, churchlow)
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
          try:
            display.destroy()
            win.destroy()
            print "Bye bye!"
          except Exception:
            print "Bye bye!"

  if win.ev=="resized":
      display.resize(win.winx,win.winy,win.width,win.height-bord)
      win.resized=False  #this flag must be set otherwise no further events will be detected

  win.ev=""  #clear the event so it doesn't repeat



