# Tiger Tank in TK window
# Version 0.02 - 23Nov12
#
# First tank demo - more to come!

import math, random, time, traceback

from pi3d import *

from pi3d import Display
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.context.Fog import Fog
from pi3d.context.Light import Light

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model

from pi3d.util.Screenshot import screenshot
from pi3d.util import Log
from pi3d.util.TkWin import TkWin

LOGGER = Log.logger(__name__)

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0     #64MB GPU memory setting
#winw,winh,bord = 1920,1200,0   #128MB GPU memory setting
win = TkWin(None,"Tiger Tank demo in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived
DISPLAY = Display.create(x=win.winx, y=win.winy, w=winw, h=winh - bord,
                         far=2200.0, background=(0.4, 0.8, 0.8, 1))
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/bumpShade")
#========================================

#texture storage for loading textures
ectex = EnvironmentCube.loadECfiles("textures/ecubes/Miramar", "miramar_256", suffix="png")
myecube = EnvironmentCube.EnvironmentCube(camera, light, 1800.0, "FACES")
for i,b in enumerate(myecube.buf):
  b.set_draw_details(shader,[ectex[i]], 0.0, -1.0)

# Create elevation map
mapwidth = 2000.0
mapdepth = 2000.0
mapheight = 100.0
mountimg1 = Texture("textures/mountains3_512.jpg")
bumpimg = Texture("textures/grasstile_n.jpg")
tigerbmp = Texture("models/Tiger/tiger_bump.jpg")
topbmp = Texture("models/Tiger/top_bump.jpg")
#roadway = Texture("textures/road5.png")
mymap = ElevationMap(camera=camera, light= light, mapfile="textures/mountainsHgt2.png",
                     width=mapwidth, depth=mapdepth,
                     height=mapheight, divx=64, divy=64)
mymap.buf[0].set_draw_details(shader,[mountimg1, bumpimg],128.0, 0.0)
mymap.set_fog((0.7,0.8,0.9,0.5), 1000.0)
#Load tank
tank_body = Model(camera, light, "models/Tiger/bodylow.egg", "TigerBody", 0,0,0, 0,0,0, 0.1,0.1,.1)
tank_body.set_shader(shader)
tank_body.set_fog((0.7,0.8,0.9,0.5), 1000.0)
tank_body.set_normal_shine(tigerbmp)
tank_gun = Model(camera, light, "models/Tiger/gunlow.egg", "TigerGun", 0,0,0, 0,0,0, 0.1,0.1,0.1, 0,0,0)
tank_gun.set_shader(shader)
tank_gun.set_fog((0.7,0.8,0.9,0.5), 1000.0)
tank_turret = Model(camera, light, "models/Tiger/turretlow.egg", "TigerTurret", 0,0,0, 0,0,0, 0.1,0.1,0.1, 0,0,0)
tank_turret.set_shader(shader)
tank_turret.set_fog((0.7,0.8,0.9,0.5), 1000.0)
tank_turret.set_normal_shine(topbmp)


#Load church
x,z = 20,-320
y = mymap.calcHeight(x,z)
church = Model(camera, light, "models/AllSaints/AllSaints.egg", "church1", x,y,z, 0,0,0, 0.1,0.1,0.1)
church.set_shader(shader)
church.set_fog((0.7,0.8,0.9,0.5), 1000.0)
churchlow = Model(camera, light, "models/AllSaints/AllSaints-lowpoly.egg", "church2", x,y,z, 0,0,0, 0.1,0.1,0.1)
churchlow.set_shader(shader)
churchlow.set_fog((0.7,0.8,0.9,0.5), 1000.0)

#Load cottages
x,z = 250,-40
y = mymap.calcHeight(x,z)
cottages = Model(camera, light, "models/Cottages/cottages_low.egg", "cottagesLo", x,y,z, 0,-5,0, 0.1,0.1,0.1)
cottages.set_shader(shader)
cottages.set_fog((0.7,0.8,0.9,0.5), 1000.0)
#cottagesHi = Model(camera, light, "models/Cottages/cottages.egg", "cottagesHi", x,y,z, -90,-5,0, .1,.1,.1)

#player tank vars
tankrot = 180.0
turrot = 0.0
tankroll = 0.0     #side-to-side roll of tank on ground
tankpitch = 0.0   #too and fro pitch of tank on ground

#position vars
mouserot = 0.0
tilt = 0.0
avhgt = 0.85
xm = 0.0
zm = -200.0
dxm = 0.0
dzm = -1.0
ym = mymap.calcHeight(xm,zm) + avhgt

#enemy tank vars
#etx = 130
#etz = -320
etx = 130
etz = -100
etr = 0.0

# Fetch key presses
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

myfog = Fog(0.0014,(0.7,0.8,0.9,0.5))

ltm = 0.0 #last pitch roll check

def drawTiger(x, y, z, rot, roll, pitch, turret, gunangle):
  tank_body.position(x, y, z)
  tank_body.rotateToX(pitch)
  tank_body.rotateToY(rot)
  tank_body.rotateToZ(roll)
  tank_body.draw()
  tank_turret.position(x, y, z)
  tank_turret.rotateToX(pitch)
  tank_turret.rotateToY(turret)
  tank_turret.rotateToZ(roll)
  tank_turret.draw()
  tank_gun.position(x, y, z)
  tank_gun.rotateToX(pitch + gunangle)
  tank_gun.rotateToY(turret)
  tank_gun.rotateToZ(roll)
  tank_gun.draw()

while 1:
  DISPLAY.clear()

  camera.reset()
  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt < -1: sf = 60 - 55.0/abs(tilt)
  else: sf = 5.0
  xoff, yoff, zoff = sf*math.sin(mouserot*rads), abs(1.25*sf*math.sin(tilt*rads)) + 3.0, -sf*math.cos(mouserot*rads)
  #xoff, yoff, zoff = 0,0,0
  #camera.translate((xm, ym-10*sf-5.0, zm-40*sf))   #zoom camera out so we can see our robot
  camera.rotate(tilt, mouserot, 0)           #Tank still affected by scene tilt
  camera.translate((xm + xoff, ym + yoff +5, zm + zoff))   #zoom camera out so we can see our robot

  #draw player tank
  tmnow = time.time()
  if tmnow > (ltm + 0.5):
    tankpitch_to, tankroll_to = mymap.pitch_roll(xm, zm)
  tankpitch += (tankpitch_to - tankpitch)/3.0
  tankroll += (tankroll_to - tankroll)/3.0
  drawTiger(xm, ym, zm, tankrot, tankroll, tankpitch, 180 - turrot, 0.0)

  mymap.draw()           #Draw the landscape

  #Draw enemy tank
  etdx = -math.sin(etr*rads)
  etdz = -math.cos(etr*rads)
  etx += etdx
  etz += etdz
  ety = mymap.calcHeight(etx, etz) + avhgt
  etr += 0.5
  if tmnow > (ltm + 0.5):
    pitch, roll = mymap.pitch_roll(etx, etz)
    ltm = tmnow # updating this here but not for users tank relies on everything being done in the right order
  drawTiger(etx, ety, etz, etr, roll, pitch, etr, 0)

  #Draw buildings
  #Draw.lodDraw3(-xm, -ym, -zm, 300, church, 1000, churchlow)
  church.draw()
  cottages.draw()

  myecube.position(xm, ym, zm)
  myecube.draw()#Draw environment cube

  #update mouse/keyboard input
  mx, my = mymouse.x, mymouse.y
  mouserot -= (mx-omx)*0.2
  tilt += (my-omy)*0.2
  omx, omy = mx, my

  # turns player tankt turret towards center of screen which will have a crosshairs
  if turrot+2.0 < mouserot:
          turrot+=2.0
  if turrot-2.0 > mouserot:
          turrot-=2.0

  #Press ESCAPE to terminate

  DISPLAY.swapBuffers()

  #Handle window events
  try:
    win.update()
  except:
    print "bye bye 3"
    DISPLAY.destroy()
    try:
      win.destroy()
    except:
      pass
    mymouse.stop()
    exit()

  if win.ev=="key":
      if win.key=="w":
          dxm = -math.sin(tankrot*rads)*2
          dzm = -math.cos(tankrot*rads)*2
          xm += dxm
          zm += dzm
          ym = (mymap.calcHeight(xm, zm) + avhgt)
      elif win.key=="s":
          xm += math.sin(tankrot*rads)*2
          zm += math.cos(tankrot*rads)*2
          ym = (mymap.calcHeight(xm, zm) + avhgt)
      elif win.key == "a":
          tankrot -= 2
      elif win.key == "d":
          tankrot += 2
      elif win.key == "p":
          screenshot("TigerTank.jpg")
      elif win.key == "Escape":
          try:
            DISPLAY.destroy()
            win.destroy()
            print "Bye bye! 1"
          except Exception:
            print "Bye bye! 2"

  if win.ev=="resized":
      DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)
      win.resized=False  #this flag must be set otherwise no further events will be detected

  win.ev=""  #clear the event so it doesn't repeat



