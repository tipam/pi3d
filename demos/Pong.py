# Ponh using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman, Paddy Gaunt
# Version 0.02 - 20Aug12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
# $ sudo apt-get install python-imaging
#
# before running this example
#

import math, random

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.util.Font import Font

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.Plane import Plane
from pi3d.shape.Sphere import Sphere

from pi3d.util.String import String
from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

#helpful messages
print "############################################################"
print "Mouse to move left and right and up and down"
print "############################################################"
print

# Setup display and initialise pi3d
DISPLAY = Display.create(x=10, y=10)
DISPLAY.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
# load shader
shader = Shader("shaders/bumpShade")
#========================================


# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'rockimg2.blend = False')
groundimg = Texture("textures/stripwood.jpg")
monstimg = Texture("textures/pong3.png")
ballimg = Texture("textures/cloud6.png", True)
# environment cube
ectex = Texture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(camera, light, 900.0,"CROSS")
myecube.buf[0].set_draw_details(shader,[ectex],0.0,-1.0)
#ball
maxdsz = 0.3
radius = 1.0
ball = Sphere(camera, light, radius,12,12,0.0,"sphere",-4,8,-7)
ball.buf[0].set_draw_details(shader,[ballimg], 0.0, 0.0)
#monster
monster = Plane(camera, light, 5.0, 5.0, "monster", 0,0,0, 0,0,0)
monster.buf[0].set_draw_details(shader, [monstimg], 0.0, 0.0)

# Create elevation map
mapwidth=50.0
mapdepth=50.0
maphalf=22.0
mapheight=40.0
#set smooth to give proper normals the bouncing won't work properly without and it doesn't look as good
mymap = ElevationMap("textures/pong.jpg", camera=camera, light=light,
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32, ntiles=4, name="sub")
mymap.buf[0].set_draw_details(shader, [groundimg], 0.0, 0.0)

#avatar camera
rot = 0.0
tilt = 0.0
avhgt = 2.0
xm = 0.0
zm = 0.0
ym = 0.0
lastX0 = 0.0
lastZ0 = 0.0

arialFont = Font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
score = [0,0]
score0 = String(camera, light,  arialFont, str(score[0]), 0, 12, 0, 0.05, 0.05)
score0.set_shader(shader)
score1 = String(camera, light,  arialFont, str(score[1]), 0, 12, 0, 0.05, 0.05)
score1.set_shader(shader)



#sphere loc and speed
sx, sy, sz = 0, 5, 0
dsx, dsy, dsz = 0.2, 0.0, -0.1
gravity = 0.02
#monster loc and speed
rx, ry, rz = 0, 0, -maphalf
drx, dry, drz = 0, 0, 0
max_speed = 0.2

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

while True:
  DISPLAY.clear()

  camera.reset()
  camera.rotate(tilt, 0, 0)
  camera.rotate(0, rot, 0)
  camera.translate((xm, 2 + ym, -maphalf - 2.5))

  myecube.draw()
  mymap.draw()

  #monster movement
  drx = sx - rx
  if abs(drx) > max_speed: drx = drx/abs(drx) * max_speed
  dry = sy - ry
  if abs(dry) > max_speed: dry = dry/abs(dry) * max_speed
  rx += drx
  ry += dry

  monster.position(rx, ry, maphalf)

  dsy -= gravity
  sx += dsx
  sy += dsy
  sz += dsz
  # now uses the clashTest method from elevationMap
  
  clash = mymap.clashTest(sx, sy, sz, radius)
  # bouncing physics
  if clash[0]:
    # returns the components of normal vector if clash
    nx, ny, nz =  clash[1], clash[2], clash[3]
    # move it away a bit to stop it getting trapped inside if it has tunelled
    jDist = clash[4] + 0.2
    sx, sy, sz = sx + jDist*nx, sy + jDist*ny, sz + jDist*nz
    print jDist
    # use R = I - 2(N.I)N
    rfact = 2.05*(nx*dsx + ny*dsy + nz*dsz) #small extra boost by using value > 2 to top up energy in defiance of 1st LOT
    dsx, dsy, dsz = dsx - rfact*nx, dsy - rfact*ny, dsz - rfact*nz
    # stop the speed increasing too much
    if dsz > 0.4: dsz = 0.4
    if dsx > 0.3: dsx = 0.2
    if dsz > maxdsz: dsz = maxdsz
  

  # mouse movement checking here to get bat movment values
  mx=mymouse.x
  dx = (mx-omx)*0.02
  omx=mx
  if ((xm >= (-1*maphalf) and dx < 0) or (xm <= maphalf and dx > 0)):  xm += dx

  my = mymouse.y
  dy = (my-omy)*0.01
  omy = my
  if ((ym >= (0) and dy < 0) or (ym <= mapheight and dy > 0)):  ym += dy

  # bounce off edges and give a random boost
  if sx > maphalf:
    dsx = -1 * abs(dsx) * (1 + random.random())
    dsz += 0.1*random.random()-0.05
  if sx < -maphalf: dsx = abs(dsx)
  if sz < -maphalf: #player end
    #check if bat in position
    if (sx - xm)**2 + (sy - ym)**2 < 10: #NB xm and ym are positions to move 'everthing else' so negative and offset height
      dsz = abs(dsz) * (1 + random.random())
      dsx += dx
      dsy += dy
    else:
      sx, sy, sz = 0, mapheight/3, 0
      dsx, dsy, dsz = 0.3*random.random()-0.15, 0, 0.1
      score[1] += 1
      score1 = String(camera, light,  arialFont, str(score[1]), 0, 12, 5, 0.05, 0.05)
      score1.set_shader(shader)
  elif sz > maphalf: #monster end
    if (sx-rx)**2 + (sy-ry)**2 < 10:
      dsz = -1 * abs(dsz)
    else:
      score[0] += 1
      score0 = String(camera, light,  arialFont, str(score[0]), 0, 12, -5, 0.05, 0.05)
      score0.set_shader(shader)
      radius = 0.1 + (radius - 0.1)*0.75 # ball gets smaller each time you score
      ball = Sphere(camera, light, radius,12,12,0.0,"sphere",0,0,0)
      ball.buf[0].set_draw_details(shader,[ballimg], 0.0, 0.0)
      maxdsz += 0.01 # max speed in z direction increases too
      sx, sy, sz = 0, mapheight/3, 0
      dsx, dsy, dsz = 0.3*random.random()-0.15, 0, -0.1

  ball.position(sx, sy, sz)

  ball.rotateIncX(dsz/radius*50)

  monster.draw()
  ball.draw()

  # write up the score
  score0.draw()
  score1.draw()

  camera.movedFlag = False
  DISPLAY.swapBuffers()

  #Press ESCAPE to terminate
  k = mykeys.read()

  if k==27: #Escape key
    DISPLAY.destroy()
    mykeys.close()
    mymouse.stop()
    break
  elif k==112:  #key P
    screenshot("pong.jpg")

# attempt to tidy up!
quit()
