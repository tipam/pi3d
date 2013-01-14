#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math, random

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.ClipPlane import ClipPlane
from pi3d.context.Light import Light

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100, w=1600, h=800)
DISPLAY.set_background(0.4,0.8,0.8,1) # r,g,b,alpha

# Load textures
tree2img = Texture("textures/tree2.png")
tree1img = Texture("textures/tree1.png")
hb2img = Texture("textures/hornbeam2.png")

ectex = Texture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(size=900.0, maptype="CROSS")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
landimg = Texture("textures/stonygrass.jpg")
mymap = ElevationMap(mapfile="textures/mountainsHgt.jpg", width=mapwidth,
                     depth=mapdepth, height=mapheight,
                     divx=64, divy=64, ntiles=10.0, name='fw') #testislands.jpg
#mymap2 = ElevationMap("textures/mountainsHgt.jpg",mapwidth,mapdepth,mapheight,64,64, 128)

myclip = ClipPlane()

Light((100,100,-100))  # Was Light(0, 2,2,3, "", 5,5,0)

#Create tree models
treeplane = Plane(w=4.0, h=5.0)

treemodel1 = MergeShape(name="baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

treemodel2 = MergeShape(name="bushytree")
treemodel2.add(treeplane, 0,0,0)
treemodel2.add(treeplane, 0,0,0, 0,60,0)
treemodel2.add(treeplane, 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape(name="trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,200.0,200.0,30,"",8.0,3.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees2 = MergeShape(name="trees2")
mytrees2.cluster(treemodel2, mymap,0.0,0.0,200.0,200.0,30,"",6.0,3.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees3 = MergeShape(name="trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,30,"",4.0,2.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)


#screenshot number
scshots = 1

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()
mtrx = Matrix()

omx, omy = mymouse.position()

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  mtrx.identity()
  mtrx.rotate(tilt, 0, 0)
  mtrx.rotate(0, rot, 0)
  mtrx.translate(xm,ym,zm)

  myecube.draw(ectex,xm,ym,zm)
  mymap.draw(landimg)
  #myclip.enable()
  #mymap2.draw(surface1)
  #myclip.disable()
  mytrees1.drawAll(tree2img)
  mytrees2.drawAll(tree1img)
  mytrees3.drawAll(hb2img)

  mx, my = mymouse.position()

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119: #key W
      xm-=math.sin(math.radians(rot))
      zm+=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==115: #kry S
      xm+=math.sin(math.radians(rot))
      zm-=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==39: #key '
      tilt -= 2.0
      print(tilt)
    elif k==47: #key /
      tilt += 2.0
    elif k==97: #key A
      rot -= 2
    elif k==100: #key D
      rot += 2
    elif k==112: #key P
      screenshot("ForestWalk2.jpg")
    elif k==10: #key RETURN
      mc = 0
    elif k==27: #Escape key
      mymouse.stop()
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print(k)

  DISPLAY.swapBuffers()

quit()
