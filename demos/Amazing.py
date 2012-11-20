# Maze with water example using pi3d module
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

from pi3d.Fog import Fog
from pi3d.Display import Display
from pi3d.Key import Key
from pi3d.Light import Light
from pi3d.Matrix import Matrix
from pi3d.Mouse import Mouse
from pi3d.Texture import Textures
from pi3d.RotateVec import *

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane
from pi3d.shape.Model import Model
from pi3d.shape.TCone import TCone

rads = 0.017453292512 # degrees to radians

#helpful messages
print "############################################################"
print "Esc to quit, W to go forward, Mouse to steer, Space to jump."

print "N.B. W now works as a TOGGLE one press to go one to stop."

print "At the edge you will turn into a ghost and be able to fly "
print "and pass through rocks! There are limited numbers of jumps."
print "Good turnings are often greener and tend to be near"
print "(but in the opposite direction to) big holes"
print "############################################################"
print "If you get touched by a monster you will return to the start!"
print "############################################################"
print

# Setup display and initialise pi3d
display = Display()
display.create3D(10,10,display.max_width-20,display.max_height-20, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
#display.create3D(10,10,800,600, 0.5, 800.0, 60.0) # small window so terminal can be viewed for errors!
display.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha

# Load textures
texs = Textures()
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'rockimg2.blend = False')
rockimg1 = texs.loadTexture("textures/techy1.jpg")
rockimg2 = texs.loadTexture("textures/rock1.png", True)
tree2img = texs.loadTexture("textures/tree2.png")
raspimg = texs.loadTexture("textures/Raspi256x256.png")
monstimg = texs.loadTexture("textures/pong2.jpg")

# environment cube
ectex = texs.loadTexture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(900.0,"CROSS")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=100.0
mymap = ElevationMap("textures/maze1.jpg",mapwidth,mapdepth,mapheight,128,128,1,"sub",0,0,0, smooth=True)
mymap2 = ElevationMap("textures/maze1.jpg",mapwidth,mapdepth,mapheight+0.1,128,128 ,64,"detail",0.0, 0.01, 0.0, smooth=True)

# Crete fog for more realistic fade in distance. This can be turned on and off between drawing different object (i.e backgound not foggy)
myfog = Fog(0.02, (0.1,0.1,0.1,1.0))

#Create tree models
treeplane = Plane(4.0,5.0)

treemodel1 = MergeShape("baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

shed = Model("models/shed1.obj",texs,"shed",0,3,0, 0,0,0, 2,2,2)

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape("trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,900.0,900.0,10,"",8.0,3.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)
raspberry = MergeShape("rasp")
raspberry.cluster(treemodel1, mymap,-250,+250,470.0,470.0,5,"",8.0,1.0)

# createMergeShape can be used to join loadModel object for much greater rendering speed
# however, because these objects can contain multiple vGroups, each with their own texture image
# it is necessary to make a merge for each vGroup and, later, draw each merged object using each
# of the textures
# The cluster method can be used where there is only one vGroup but with more than one the different
# parts of the object get split up by the randomisation! Here I manually do the same thing as cluster
# by first generating an array of random locations and y-rotations
shedgp = {}
xArr = []
yArr = []
zArr = []
rArr = []
for i in range(5):
  xval = (random.random()-0.5)*50 + 19
  xArr.append(xval)
  zval = (random.random()-0.5)*50 - 19
  zArr.append(zval)
  yArr.append(mymap.calcHeight(-xval, -zval))
  rArr.append(random.random()*45) # front faces approximately towards the sun (found by trial and error)
for g in shed.vGroup:
  thisAbbGp = MergeShape("shed")
  for i in range(len(xArr)):
    thisAbbGp.add(shed.vGroup[g], xArr[i], yArr[i], zArr[i], 0, rArr[i], 0)
  shedgp[g] = thisAbbGp

#monster
monst = TCone()
mDx,mDy,mDz = 0.1,0,0.2
mSx,mSy,mSz = -5, mymap.calcHeight(-5,5)+1, 5
gravity = 0.02

# lighting. The default light is a point light but I have made the position method capable of creating
# a directional light and this is what I do inside the loop. If you want a torch you don't need to move it about
light = Light(0, 4, 4, 2, "", 0,1,-2, 0.1,0.1,0.2) #yellowish 'torch' or 'sun' (could be blueish ambient with different env cube)
light.on()

#screenshot number key P for screenshots
scshots = 1

#energy counter
hp = 25

#avatar camera NB this isn't really moving as an object in the scene - it's staying still and used to move everything else
#relative to it. So -xm, -ym, -zm all need to be used for calcualtions of real object relative to the camera!
camera = Matrix()
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)
lastX0=0.0
lastZ0=0.0

# Fetch key presses
mykeys = Key()
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

fly = False
walk = False
# Display scene and rotate cuboid
angle = 0

#################################################### LOOP ###############################################
while 1:
  display.clear()

  camera.identity()
  camera.rotate(tilt,0,0)
  camera.rotate(0,rot,0)
  camera.translate(xm,ym,zm)

  myecube.draw(ectex,xm,ym,zm)
  myfog.on()
  mymap.draw(rockimg1)
  mymap2.draw(rockimg2)
  mytrees1.drawAll(tree2img)
  raspberry.drawAll(raspimg)
  monst.draw(monstimg)

  # monster movement
  mDy -= gravity
  mDelx,mDelz = mSx+xm, mSz+zm #distance from monster
  mDist = math.sqrt(mDelx**2 + mDelz**2)
  mDx -= 0.01*mDelx/mDist
  mDz -= 0.01*mDelz/mDist
  monst.rotateIncY(100.0/mDist)
  if mDist > 100: #far away so teleport it nearer
    mSx, mSz = -xm + 100*random.random() - 50, -zm + 100*random.random() - 50
    if mSx < -mapwidth/2: mSx = -mapwidth/2
    if mSx > mapwidth/2: mSx = mapwidth/2
    if mSz < -mapdepth/2: mSz = -mapdepth/2
    if mSz > mapdepth/2: mSz = mapdepth/2
  if mDist < 3: #it's got you, return to GO
    xm, ym, zm = 0, -(mymap.calcHeight(0,0)+avhgt), 0

  clash = mymap.clashTest(monst.x, monst.y, monst.z, 1.5)
  if clash[0]:
    # returns the components of normal vector if clash
    nx, ny, nz =  clash[1], clash[2], clash[3]
    # move it away a bit to stop it getting trapped inside if it has tunelled
    jDist = clash[4] + 0.1
    mSx, mSy, mSz = mSx - jDist*nx, mSy - jDist*ny, mSz - jDist*nz

    # use R = I - 2(N.I)N
    rfact = 2.05*(nx*mDx + ny*mDy + nz*mDz) #small extra boost by using value > 2 to top up energy in defiance of 1st LOT
    mDx, mDy, mDz = mDx - rfact*nx, mDy - rfact*ny*0.7, mDz - rfact*nz
    # stop the speed increasing too much
    if mDx > 0.4: dsz = 0.4
    if mDy > 0.1: dsx = 0.05
    if mDz > 0.4: mDz = 0.4
  mSx += mDx
  mSy += mDy
  mSz += mDz
  monst.position(mSx, mSy, mSz)

  # draw the sheds
  for g in shed.vGroup:
    shedgp[g].drawAll(shed.vGroup[g].texID)

  # movement and rotations of light
  myfog.off()

  mx=mymouse.x
  my=mymouse.y

  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my
  v1 = rotate_vec_y(rot,  0, 1, -2)
  v2 = rotate_vec_x(tilt,v1[0], v1[1], v1[2])
  light.position(v2[0], v2[1], v2[2], 0) #fourth parameter in function sets (1=point light , default) or (0=distant light)
  # the light has to be turned as the scene rotates, it took ages to work out how to do this by reversing the rotation order!!!
  dx = -math.sin(rot*rads)
  dz = math.cos(rot*rads)
  dy = math.sin(tilt*rads)
  if (walk):
    if (fly):
      xm += dx*3
      zm += dz*3
      ym += dy*3
    else:
      dy = -(mymap.calcHeight(xm + dx*1.5, zm + dz*1.5)+avhgt) - ym
      if dy > -1.0: # limit steepness so can't climb up walls
        xm += dx
        zm += dz
        ym += dy
    if (xm < -490 or xm > 490 or zm < -490 or zm > 490): fly = True #reached the edge of the maze!

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
      display.screenshot("critters3D"+str(scshots)+".jpg")
      scshots += 1
    elif k==32 and hp > 0: #key SPACE
      walk = False
      dy = -(mymap.calcHeight(xm + dx, zm + dz)+avhgt) - ym
      xm += dx
      zm += dz
      ym += dy
      hp -= 1
    elif k==27: #Escape key
      display.destroy()
      mykeys.close()
      mymouse.stop()
      break
    #else:
    #print k

  display.swapBuffers()
quit()
