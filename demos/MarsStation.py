#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Uses a Tkinter window with elevation map, and more complicated models
loaded from panda3d egg files. The models demostrate various things:
1. loading the shader for them to be drawn with 2. loading the normal map
file and reflection map file, although this is done for the whole model it can
be used to set them differently for each Buffer, i.e. different parts of the
Model. 3. level of detail drawing using Utility.draw_level_of_detail() This allows different
versions of the model to be shown as the viewpoint gets nearer, in this case
the distant one has the doors and windows closed, the near one open
"""
import math, random, time

import demo
from pi3d import *

from pi3d.util.TkWin import TkWin
#from pi3d.event.Event import InputEvents

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window
# TODO: the display will do this for you automatically now
winw,winh,bord = 1200,600,0 #64MB GPU memory setting
#winw,winh,bord = 1920,1080,0 #128MB GPU memory setting

DISPLAY = Display.create(tk=True, window_title='Mars Station demo in Pi3D',
                        w=winw, h=winh - bord, far=2200.0,
                        background=(0.4, 0.8, 0.8, 1), frames_per_second=20)

#inputs = InputEvents()

win = DISPLAY.tkwin

shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
shade2d = Shader('shaders/2d_flat')

#========================================
# create splash screen and draw it
splash = ImageSprite("textures/pi3d_splash.jpg", shade2d, w=10, h=10, z=0.2)
splash.draw()
DISPLAY.swap_buffers()
#############################
ectex = loadECfiles("textures/ecubes/RedPlanet", "redplanet_256", "png", True)
myecube = EnvironmentCube(size=1800.0, maptype="FACES")
myecube.set_draw_details(flatsh,ectex)

# Create elevation map
mapwidth=2000.0
mapdepth=2000.0
mapheight=100.0
redplanet = Texture("textures/mars_colour.png")
bumpimg = Texture("textures/mudnormal.jpg")
mymap = ElevationMap(mapfile='textures/mars_height.png',
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=64, divy=64)
mymap.buf[0].set_draw_details(shader,[redplanet, bumpimg],128.0, 0.0)
mymap.set_fog((0.3, 0.15, 0.1, 0.0), 1000.0)

#Load Corridors sections

sttnbmp = Texture("textures/floor_nm.jpg")
sttnshn = Texture("textures/stars.jpg")
x,z = 0,0
y = mymap.calcHeight(x, z)

cor_win90 = Model(file_string="models/MegaStation/corridor_win_lowpoly.egg",
                x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
cor_win90.set_shader(shader)
# TODO seem to be able to 'stamp' the same object in different locations
# but not different rotations! need to find out cause
cor_win00 = cor_win90.clone()
cor_win90.rotateToY(90)

corridor90 = Model(file_string="models/MegaStation/corridor_lowpoly.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
corridor90.set_shader(shader)
corridor00 = corridor90.clone()
corridor90.rotateToY(90)

cor_cross = Model(file_string="models/MegaStation/cross_room.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
cor_cross.set_shader(shader)
cor_cross.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.1)

cor_cross_doors = Model(file_string="models/MegaStation/cross_room_doors.egg",
                        x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
cor_cross_doors.set_shader(shader)
cor_cross_doors.set_normal_shine(sttnbmp, 32.0, sttnshn, 0.1)

cor_bend = Model(file_string="models/MegaStation/bend_lowpoly.egg",
                 x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
cor_bend.set_shader(shader)
cor_bend.set_normal_shine(sttnbmp, 32.0)
cor_bend.rotateToY(180)

#position vars
mouserot=0.0
tilt=0.0
avhgt = 5.3
xm=0.0
zm=0.0
ym= (mymap.calcHeight(xm,zm) + avhgt)
spc = 39.32
mody = ym + 3.0
opendist = 80

#key presses
mymouse = Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()

# Update display before we begin (user might have moved window)
win.update()
DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)

CAMERA = Camera.instance()
#inputs.get_mouse_movement()

try:
  while DISPLAY.loop_running():
    CAMERA.reset()

    #tilt can be used as a means to prevent the view from going under the landscape!
    if tilt < -1: sf = 6 - 5.5/abs(tilt)
    else: sf = 0.5
    xoff, yoff, zoff = sf*math.sin(mouserot*rads), abs(1.25*sf*math.sin(tilt*rads)) + 3.0, -sf*math.cos(mouserot*rads)
    CAMERA.rotate(tilt, mouserot, 0)
    CAMERA.position((xm + xoff, ym + yoff +5, zm + zoff))

    Utility.draw_level_of_detail([xm, ym, zm], [0, mody, 0], [[opendist,cor_cross],[1000,cor_cross_doors]])
    cor_win90.position(0, mody, spc*1.5)
    cor_win90.draw()
    corridor90.position(0, mody, spc*2.5)
    corridor90.draw()
    cor_win90.position(0, mody, spc*3.5)
    cor_win90.draw()
    Utility.draw_level_of_detail([xm, ym, zm], [0, mody, spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])
    cor_win90.position(0, mody, spc*6.5)
    cor_win90.draw()
    Utility.draw_level_of_detail([xm, ym, zm],[0, mody, spc*8], [[opendist,cor_cross],[1000,cor_cross_doors]])
    cor_win00.position(-spc*1.5, mody, spc*5)
    cor_win00.draw()
    cor_bend.position(-spc*2.5, mody, spc*5)
    cor_bend.draw()
    Utility.draw_level_of_detail([xm, ym, zm],[-spc*2.6, mody, spc*6.6],[[opendist,cor_cross],[1000,cor_cross_doors]])
    cor_win00.position(spc*1.5, mody, spc*5)
    cor_win00.draw()
    corridor00.position(spc*2.5, mody, spc*5)
    corridor00.draw()
    Utility.draw_level_of_detail([xm, ym, zm],[spc*4, mody, spc*5],[[opendist,cor_cross],[1000,cor_cross_doors]])

    mymap.draw()  #Draw the landscape

    myecube.position(xm, ym, zm)
    myecube.draw()#Draw environment cube

    mx, my = mymouse.position()
    mouserot -= (mx-omx)*0.2
    tilt += (my-omy)*0.2
    omx=mx
    omy=my
    try:
      win.update()
    except Exception as e:
      print("bye,bye2", e)
      DISPLAY.destroy()
      try:
        win.destroy()
      except:
        pass
      mymouse.stop()
      exit()
    if win.ev == "resized":
      print("resized")
      DISPLAY.resize(win.winx, win.winy, win.width, win.height-bord)
      CAMERA.reset((DISPLAY.near, DISPLAY.far, DISPLAY.fov, 
                  DISPLAY.width / float(DISPLAY.height)))
      win.resized = False
    if win.ev == "key":
      if win.key == "w":
        xm-=math.sin(mouserot*rads)*2
        zm+=math.cos(mouserot*rads)*2
      if win.key == "s":
        xm+=math.sin(mouserot*rads)*2
        zm-=math.cos(mouserot*rads)*2
      if win.key == "a":
        mouserot -= 2
      if win.key == "d":
        mouserot += 2
      if win.key == "p":
        screenshot("MarsStation.jpg")
      if win.key == "Escape":
        try:
          print("bye,bye1")
          DISPLAY.destroy()
          try:
            win.destroy()
          except:
            pass
          mymouse.stop()
          exit()
        except:
          pass
    if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
      xm-=math.sin(mouserot*rads)*2
      zm+=math.cos(mouserot*rads)*2
    else:
      win.ev=""  #clear the event so it doesn't repeat

except Exception as e:
  print("bye,bye3", e)
  DISPLAY.destroy()
  try:
    win.destroy()
  except:
    pass
  mymouse.stop()
  exit()

