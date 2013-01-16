#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Maze showing various features: textured terrain, movement restricted by
terrain, bouncing off the ElevationMap using clashTest, loading wavefront
obj files, MergeShape using a Model with multiple Textures, first person
view camera movement
"""

import math, random

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane
from pi3d.shape.Model import Model
from pi3d.shape.TCone import TCone

from pi3d.util.Matrix import Matrix
from pi3d.util.RotateVec import *
from pi3d.util.Screenshot import screenshot

rads = 0.017453292512 # degrees to radians

#helpful messages
print("############################################################")
print("Esc to quit, W to go forward, Mouse to steer, Space to jump.")

print("N.B. W now works as a TOGGLE one press to go one to stop.")

print("At the edge you will turn into a ghost and be able to fly ")
print("and pass through rocks! There are limited numbers of jumps.")
print("Good turnings are often greener and tend to be near")
print("(but in the opposite direction to) big holes")
print("############################################################")
print("If you get touched by a monster you will return to the start!")
print("############################################################")
print()

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100, background=(0.4, 0.8, 0.8, 1))

shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#========================================

# load Textures
rockimg1 = Texture("textures/techy1.jpg")
rockimg2 = Texture("textures/rocktile2.jpg")
tree2img = Texture("textures/tree2.png")
raspimg = Texture("textures/Raspi256x256.png")
monstimg = Texture("textures/pong2.jpg")
monsttex = Texture("textures/floor_nm.jpg")
shineimg = Texture("textures/stars.jpg")

# environment cube
ectex = Texture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(size=900.0, maptype="CROSS")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
mapheight = 100.0
mymap = ElevationMap("textures/maze1.jpg",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=128, divy=128, name="sub")
mymap.set_draw_details(shader, [rockimg1, rockimg2, shineimg], 128.0, 0.05)

# Create fog for more realistic fade in distance. This can be turned on and off between drawing different object (i.e backgound not foggy)
mymap.set_fog((0.1,0.1,0.1,1.0), 200.0)

#Create tree models
treeplane = Plane(w=4.0, h=5.0)

treemodel1 = MergeShape(name="baretree")
treemodel1.add(treeplane.buf[0], 0,0,0)
treemodel1.add(treeplane.buf[0], 0,0,0, 0,90,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape(name="trees1")
mytrees1.cluster(treemodel1.buf[0], mymap,0.0,0.0,900.0,900.0,10,"",8.0,3.0)
mytrees1.buf[0].set_draw_details(shader, [tree2img, rockimg2], 4.0, 0.0)
mytrees1.set_fog((0.1,0.1,0.1,1.0), 200.0)

raspberry = MergeShape(name="rasp")
raspberry.cluster(treemodel1.buf[0], mymap,-250,+250,470.0,470.0,5,"",8.0,1.0)
raspberry.buf[0].set_draw_details(shader, [raspimg, raspimg], 1.0, 0.0)
raspberry.set_fog((0.1,0.1,0.1,1.0), 200.0)

""" MergeShape can be used to join a number of Model object for much greater 
 rendering speed however, because Models can contain multiple Buffers,
 each with their own texture image it is necessary to make a merge for each
 Buffer and, later, draw each merged object using each of the textures.
 The cluster method can be used where there is only one Buffer but with more
 than one the different parts of the object get split up by the randomisation!
 Here I manually do the same thing as cluster by first generating an array
 of random locations and y-rotations
"""
shed = Model(file_string="models/shed1.obj",
             name="shed", y=3, sx=2, sy=2, sz=2)

shedgp = []
xArr = []
yArr = []
zArr = []
rArr = []
for i in range(5):
  xval = (random.random()-0.5)*50 + 19
  xArr.append(xval)
  zval = (random.random()-0.5)*50 - 19
  zArr.append(zval)
  yArr.append(mymap.calcHeight(xval, zval))
  rArr.append(random.random()*45)

for b in shed.buf:
  thisAbbGp = MergeShape(name="shed")
  # i.e. different merge groups for each part requiring different texture
  for i in range(len(xArr)):
    thisAbbGp.add(b, xArr[i], yArr[i], zArr[i], 0, rArr[i], 0)
  shedgp.append(thisAbbGp)
  shedgp[len(shedgp)-1].set_draw_details(shader, b.textures, 0.0, 0.0)
  shedgp[len(shedgp)-1].set_fog((0.1,0.1,0.1,1.0), 250.0)

# monster
monst = TCone()
# use the uv_reflect shader but if shiny=0.0 there will be no reflection
# the third texture is unset so there are unpredictable results if > 0
monst.set_draw_details(shader, [monstimg, monsttex], 4.0, 0.0)
mDx,mDy,mDz = 0.1,0,0.2
mSx,mSy,mSz = -15, mymap.calcHeight(-15,5)+1, 5
gravity = 0.02

#screenshot number key p for screenshots
scshots = 1

#energy counter (space bar jumping)
hp = 25

rot = 0.0
tilt = 0.0
avhgt = 3.0
xm, oxm = 0.0, -1.0
zm, ozm = 0.0, -1.0
ym= mymap.calcHeight(xm,zm) + avhgt
lastX0=0.0
lastZ0=0.0

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse(restrict = False)
mymouse.start()

omx, omy = mymouse.position()

fly = False
walk = True

angle = 0

#################################################### LOOP ###############################################

CAMERA = Camera.instance()
while 1:
  DISPLAY.clear()

  # movement of camera
  mx, my = mymouse.position()
  rot -= (mx-omx)*0.2
  tilt += (my-omy)*0.1

  dx = -math.sin(rot*rads)
  dz = math.cos(rot*rads)
  dy = math.sin(tilt*rads)
  if (walk):
    if (fly):
      xm += dx*3
      zm += dz*3
      ym += dy*3
    else:
      dy = mymap.calcHeight(xm + dx*1.5, zm + dz*1.5) + avhgt - ym
      if dy < 1.2: # limit steepness so can't climb up walls
        xm += dx*0.5
        zm += dz*0.5
        ym += dy*0.5
    if (xm < -490 or xm > 490 or zm < -490 or zm > 490): fly = True #reached the edge of the maze!
  if not (mx == omx and my == omy and oxm == xm and ozm == zm):
    CAMERA.reset()
    CAMERA.rotate(tilt, 0, 0)
    CAMERA.rotate(0, rot, 0)
    CAMERA.position((xm, ym, zm))
  omx = mx
  omy = my
  oxm = xm
  ozm = zm

  myecube.position(xm, ym, zm)
  myecube.draw()
  mymap.draw()
  mytrees1.draw()
  raspberry.draw()
  monst.draw()

  # monster movement
  mDy -= gravity
  mDelx,mDelz = mSx-xm, mSz-zm #distance from monster
  mDist = math.sqrt(mDelx**2 + mDelz**2)
  mDx = -0.1*mDelx/mDist
  mDz = -0.1*mDelz/mDist
  monst.rotateIncY(100.0/mDist)
  if mDist > 100: #far away so teleport it nearer
    mSx, mSz = xm + 100*random.random() - 50, zm + 100*random.random() - 50
    if mSx < -mapwidth/2: mSx = -mapwidth/2
    if mSx > mapwidth/2: mSx = mapwidth/2
    if mSz < -mapdepth/2: mSz = -mapdepth/2
    if mSz > mapdepth/2: mSz = mapdepth/2
  if mDist < 3: #it's got you, return to GO
    xm, ym, zm = 0, mymap.calcHeight(0,0) + avhgt, 0

  clash = mymap.clashTest(mSx, mSy, mSz, 1.5)
  if clash[0]:
    # returns the components of normal vector if clash
    nx, ny, nz =  clash[1], clash[2], clash[3]
    # move it away a bit to stop it getting trapped inside if it has tunelled
    jDist = clash[4] + 0.1
    mSx, mSy, mSz = mSx + jDist*nx, mSy + jDist*ny, mSz + jDist*nz

    # use R = I - 2(N.I)N
    rfact = 2.05*(nx*mDx + ny*mDy + nz*mDz) #small extra boost by using value > 2 to top up energy in defiance of 1st LOT
    mDx, mDy, mDz = mDx - rfact*nx, mDy - rfact*ny*0.8, mDz - rfact*nz
    # stop the speed increasing too much
    if mDx > 0.4: dsz = 0.4
    if mDy > 0.1: dsx = 0.05
    if mDz > 0.4: mDz = 0.4
  mSx += mDx
  mSy += mDy
  mSz += mDz
  monst.position(mSx, mSy, mSz)

  # draw the sheds
  for g in shedgp:
    g.draw()

  #key press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119: #key W toggle NB no longer need to hold down all the time
      walk = not(walk)
    elif k==115: #kry S
      walk = False
      dy = -(mymap.calcHeight(xm - dx, zm - dz)+avhgt) - ym
      if dy > -1.0:
        xm -= dx
        zm -= dz
        ym += dy
    elif k==112: #key P
      screenshot("amazing"+str(scshots)+".jpg")
      scshots += 1
    elif k==32 and hp > 0: #key SPACE
      walk = False
      dy = mymap.calcHeight(xm + dx, zm + dz) + avhgt + ym
      xm += dx
      zm += dz
      ym += dy
      hp -= 1
    elif k==102: #f key to fire
      missile.fire(xm, ym, zm, -dx, -math.sin(tilt*rads), -dz, 10)
    elif k==27: #Escape key
      DISPLAY.destroy()
      mykeys.close()
      mymouse.stop()
      break
  # this will save a little time each loop if the camera is not moved
  CAMERA.was_moved = False
  DISPLAY.swapBuffers()

quit()
