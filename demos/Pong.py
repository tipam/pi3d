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

from pi3d.Display import Display
from pi3d.EnvironmentCube import EnvironmentCube
from pi3d.Key import Key
from pi3d.Light import Light
from pi3d.Matrix import Matrix
from pi3d.Mouse import Mouse
from pi3d.Texture import Textures

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.Plane import Plane
from pi3d.shape.Sphere import Sphere

#helpful messages
print "############################################################"
print "Mouse to move left and right and up and down"
print "############################################################"
print

# Setup display and initialise pi3d
display = Display()
#display.create3D(10,10,600,450, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
display.create3D(10,10,1200,900, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha

# Load textures
texs = Textures()
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'rockimg2.blend = False')
groundimg = texs.loadTexture("textures/pong2.jpg")
monstimg = texs.loadTexture("textures/pong3.png")
# environment cube
ectex = texs.loadTexture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(900.0,"CROSS")
#ball
radius = 1
ball = Sphere(radius,12,12,0.0,"sphere",-4,8,-7)
#monster
monster = Plane(5.0, 5.0, "monster", 0,0,0, 0,0,0)
# Create elevation map
mapwidth=50.0                
mapdepth=50.0
maphalf=23.0
mapheight=20.0
#set smooth to give proper normals
mymap = ElevationMap("textures/pong.jpg",mapwidth,mapdepth,mapheight,64,64,2,"sub",0,0,0, smooth=True)
# lighting. The default light is a point light but I have made the position method capable of creating
# a directional light and this is what I do inside the loop. If you want a torch you don't need to move it about
light = Light(0, 2, 2, 1, "", 1,2,3, 0.1,0.1,0.2) #yellowish 'torch' or 'sun' with low level blueish ambient
light.position(1,2,3,0) # set to directional light by setting position with 0 fourth parameter
light.on()

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym=mapheight
lastX0=0.0
lastZ0=0.0

#sphere loc and speed
sx, sy, sz = 0, 5, 0
dsx, dsy, dsz = 0.1, 0.0, -0.1
gravity = 0.02
#monster loc and speed
rx, ry, rz = 0, 0, -maphalf
drx, dry, drz = 0, 0, 0
max_speed = 0.1

# Fetch key presses
mykeys = Key()
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

matrix = Matrix()
while True:
  display.clear()
  
  matrix.identity()
  matrix.translate(xm,-2+ym-mapheight,-maphalf+2)
  
  myecube.draw(ectex,xm,ym,zm)
  mymap.draw(groundimg)
  
  monster.draw(monstimg)
  ball.draw(groundimg)
  
  #monster movement
  drx = sx - rx
  if abs(drx) > max_speed: drx = drx/abs(drx) * max_speed
  dry = sy - ry
  if abs(dry) > max_speed: dry = dry/abs(dry) * max_speed
  rx += drx
  ry += dry
  
  monster.position(rx, ry, -maphalf)
  
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
    jDist = clash[4]*radius
    sx, sy, sz = sx - jDist*nx, sy - jDist*ny, sz - jDist*nz
    # clash[4] is also the ground level below the mid point of the object so this could be used to 'lift' it up
    #if sy < clash[4]+radius: sy = clash[4]+radius

    # use R = I - 2(N.I)N
    rfact = 2.02*(nx*dsx + ny*dsy + nz*dsz) #small extra boost by using value > 2 to top up energy in defiance of 1st LOT
    dsx, dsy, dsz = dsx - rfact*nx, dsy - rfact*ny, dsz - rfact*nz
    # stop the speed increasing too much
    if dsx > 0.3: dsx = 0.2
    if dsz > 0.3: dsz = 0.2    
    
  # mouse movement checking here to get bat movment values
  mx=mymouse.x
  dx = -(mx-omx)*0.02
  omx=mx
  if ((xm >= (-1*maphalf) and dx < 0) or (xm <= maphalf and dx > 0)):  xm += dx

  my=mymouse.y
  dy = -(my-omy)*0.01
  omy=my
  if ((ym >= (0) and dy < 0) or (ym <= mapheight and dy > 0)):  ym += dy

  # bounce off edges and give a random boost
  if sx > maphalf: dsx = -1 * abs(dsx) * (1 + random.random())
  if sx < -maphalf: dsx = abs(dsx)
  if sz > maphalf: #player end
    #check if bat in position
    if (sx + xm)**2 + (sy - mapheight+ym)**2 < 10: #NB xm and ym are positions to move 'everthing else' so negative and offset height
      dsz = -1 * abs(dsz) * (1 + random.random())
      dsx += dx
      dsy += dy
    else:
      sx, sy, sz = 0, 10, 0
      dsx, dsy, dsz = 0.2*random.random(), 0, 0.1
  if sz < -maphalf: #monster end
    if (sx-rx)**2 + (sy-ry)**2 < 10:
      dsz = abs(dsz)
    else:
      sx, sy, sz = 0, mapheight, 0
      dsx, dsy, dsz = 0.2*random.random(), 0, -0.1

  ball.position(sx, sy, sz)
  ball.rotateIncX(dsx*-10)
  ball.rotateIncZ(dsz*-10)

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k==27: #Escape key
    display.destroy()
    mykeys.close()
    break
  
  display.swapBuffers()

display.destroy()
quit()
