# Tiger Tank in TK window
# Version 0.02 - 23Nov12

import math, random, time

from pi3d import *

from pi3d import Display
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model

from pi3d.util.Screenshot import screenshot
from pi3d.util import Log
from pi3d.util.TkWin import TkWin
from pi3d.util.Utility import lodDraw

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
winw,winh,bord = 1200,600,0   	#64MB GPU memory setting
#winw,winh,bord = 1920,1080,0	#128MB GPU memory setting
win = TkWin(None, "Mega Space Station in Pi3D",winw,winh)

# Setup display and initialise pi3d viewport over the window
win.update()  #requires a window update first so that window sizes can be retreived

display = Display.create(x=win.winx, y=win.winy, w=winw, h=winh - bord,
                         far=2200.0, background=(0.4, 0.8, 0.8, 1))
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, display.win_width/1000.0, display.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#############################
ectex = EnvironmentCube.loadECfiles("textures/ecubes/RedPlanet", "redplanet_256", "png", True)
myecube = EnvironmentCube.EnvironmentCube(camera, light, 1800.0,"FACES")
myecube.set_draw_details(flatsh,ectex)


# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
redplanet = Texture("textures/mars_colour.png")
bumpimg = Texture("textures/mudnormal.jpg")
mymap = ElevationMap(camera=camera, light= light, mapfile='textures/mars_height.png', width=mapwidth,
                     depth=mapdepth, height=mapheight, divx=64, divy=64)
mymap.buf[0].set_draw_details(shader,[redplanet, bumpimg],128.0, 0.0)
mymap.set_fog((0.3,0.15,0.1,1.0), 1000.0)

#Load Corridors sections

sttnbmp = Texture("textures/floor_nm.jpg")
sttnshn = Texture("textures/stars.jpg")
x,z = 0,0
y = mymap.calcHeight(x, z)
cor_win = Model(camera, light, "models/MegaStation/corridor_win_lowpoly.egg", "", x,y,z, 0,0,0, 0.1,0.1,0.1)
cor_win.set_shader(shader)
corridor = Model(camera, light, "models/MegaStation/corridor_lowpoly.egg", "", x,y,z, 0,0,0, 0.1,0.1,0.1)
corridor.set_shader(shader)
cor_cross = Model(camera, light, "models/MegaStation/cross_room.egg", "", x,y,z, 0,0,0, 0.1,0.1,0.1)
cor_cross.set_shader(shader)
cor_cross.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.4)
cor_cross_doors = Model(camera, light, "models/MegaStation/cross_room_doors.egg", "", x,y,z, 0,0,0, 0.1,0.1,0.1)
cor_cross_doors.set_shader(shader)
cor_cross_doors.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.4)
cor_bend = Model(camera, light, "models/MegaStation/bend_lowpoly.egg", "", x,y,z, 0,0,0, 0.1,0.1,0.1)
cor_bend.set_shader(shader)
cor_bend.set_normal_shine(sttnbmp)

#position vars
mouserot=0.0
tilt=0.0
avhgt = 2.3
xm=0.0
zm=0.0
ym= (mymap.calcHeight(xm,zm) + avhgt)
spc = 39.32
mody = ym
opendist = 80

# Fetch key presses
mymouse = Mouse()
mymouse.start()

omx, omy = mymouse.position()

# Update display before we begin (user might have moved window)
win.update()
display.resize(win.winx, win.winy, win.width, win.height - bord)

while 1:
  display.clear()

  camera.reset()
  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt < -1: sf = 6 - 5.5/abs(tilt)
  else: sf = 0.5
  xoff, yoff, zoff = sf*math.sin(mouserot*rads), abs(1.25*sf*math.sin(tilt*rads)) + 3.0, -sf*math.cos(mouserot*rads)
  camera.rotate(tilt, mouserot, 0)           #Tank still affected by scene tilt
  camera.translate((xm + xoff, ym + yoff +5, zm + zoff))   #zoom camera out so we can see our robot

  mymap.draw()  #Draw the landscape

  lodDraw([xm, ym, zm], [0, mody, 0], [[opendist,cor_cross],[1000,cor_cross_doors]])
  cor_win.position(0, mody, -spc*1.5)
  cor_win.draw()
  corridor.position(0, mody, -spc*2.5)
  corridor.draw()
  cor_win.position(0, mody, -spc*3.5)
  cor_win.draw()
  lodDraw([xm, ym, zm], [0, mody, -spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])
  cor_win.position(0, mody, -spc*6.5)
  cor_win.draw()
  lodDraw([xm, ym, zm],[0, mody, -spc*8], [[opendist,cor_cross],[1000,cor_cross_doors]])
  cor_win.rotateToY(90)
  cor_win.position(-spc*1.5, mody, -spc*5)
  cor_win.draw()
  cor_bend.rotateToY(90)
  cor_bend.position(-spc*2.5, mody, -spc*5)
  cor_bend.draw()
  lodDraw([xm, ym, zm],[-spc*2.6, mody, -spc*6.6],[[opendist,cor_cross],[1000,cor_cross_doors]])
  cor_win.rotateToY(90)
  cor_win.position(spc*1.5, mody, -spc*5)
  cor_win.draw()
  corridor.rotateToY(90)
  corridor.position(spc*2.5, mody, -spc*5)
  corridor.draw()
  lodDraw([xm, ym, zm],[spc*4, mody, -spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])

  myecube.position(xm, ym, zm)
  myecube.draw()#Draw environment cube

  #update mouse/keyboard input
  mx, my = mymouse.position()

  mouserot -= (mx-omx)*0.2
  tilt += (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate

  display.swapBuffers()

  #Handle window events
  try:
    win.update()
  except:
    print "bye bye 3"
    display.destroy()
    try:
      win.destroy()
    except:
      pass
    mymouse.stop()
    exit()

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
      screenshot("MegaStation.jpg")
    elif win.key=="Escape":
      try:
        display.destroy()
        win.destroy()
        print "Bye bye! 1"
      except Exception:
        print "Bye bye! 2"

  if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
    xm-=math.sin(mouserot*rads)*2
    zm+=math.cos(mouserot*rads)*2

  win.ev=""  #clear the event so it doesn't repeat

