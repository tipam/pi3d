# Forest walk example using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.04 - 20Jul12
#
# grass added, new environment cube using FACES
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#    $ sudo apt-get install python-imaging
#
# before running this example
#
from __future__ import absolute_import

import math,random

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Light import Light

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100, w=800, h=600, near=0.5,
                         far=800.0, aspect=60.0)
DISPLAY.setBackColour(0.4,0.8,0.8,1)      # r,g,b,alpha

tree2img = Texture("textures/tree2.png")
tree1img = Texture("textures/tree1.png")
grassimg = Texture("textures/grass.png")
hb2img = Texture("textures/hornbeam2.png")

#myecube = EnvironmentCube(900.0,"HALFCROSS")

ectex=loadECfiles("textures/ecubes","sbox")
myecube = EnvironmentCube(900.0,"FACES")

light = Light(0, 10,10,10, "", 0,100,0)
light.on()

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = Texture("textures/mountains3_512.jpg")
mymap = ElevationMap("textures/mountainsHgt.jpg",mapwidth,mapdepth,mapheight,64,64) #testislands.jpg

#Create tree models
treeplane = Plane(4.0,5.0)

treemodel1 = MergeShape("baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

treemodel2 = MergeShape("bushytree")
treemodel2.add(treeplane, 0,0,0)
treemodel2.add(treeplane, 0,0,0, 0,60,0)
treemodel2.add(treeplane, 0,0,0, 0,120,0)

#Create grass model
grassplane = Plane(1.0,0.3,"",0,-2,0)
grassmodel = MergeShape("grass")
grassmodel.add(grassplane, 0,0,0)
grassmodel.add(grassplane, 0,0,0, 0,60,0)
grassmodel.add(grassplane, 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape("trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,200.0,200.0,30,"",8.0,3.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees2 = MergeShape("trees2")
mytrees2.cluster(treemodel2, mymap,0.0,0.0,200.0,200.0,30,"",6.0,3.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees3 = MergeShape("trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,30,"",4.0,2.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mygrass = MergeShape("grass")
mygrass.cluster(grassmodel, mymap,0.0,0.0,100.0,100.0,100,"",10.0,4.0)

#mygrass2 = MergeShape("grass2")
#mygrass2.cluster(mygrass, mymap,100.0,0.0,100.0,100.0,1,"",1.0,1.0)

#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)


#screenshot number
scshots = 1

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# setup matrices
mtrx = Matrix()

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  mtrx.identity()
  mtrx.rotate(tilt, 0, 0)
  mtrx.rotate(0, rot, 0)
  mtrx.translate(xm,ym,zm)

  myecube.draw(ectex,xm,ym,zm)
  mymap.draw(mountimg1)
  mygrass.drawAll(grassimg)
  mytrees1.drawAll(tree2img)
  mytrees2.drawAll(tree1img)
  mytrees3.drawAll(hb2img)

  mx=mymouse.x
  my=mymouse.y

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:  #key W
      xm-=math.sin(math.radians(rot))
      zm+=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==115:  #kry S
      xm+=math.sin(math.radians(rot))
      zm-=math.cos(math.radians(rot))
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==39:   #key '
      tilt -= 2.0
      print tilt
    elif k==47:   #key /
      tilt += 2.0
    elif k==97:   #key A
      rot -= 2
    elif k==100:  #key D
      rot += 2
    elif k==112:  #key P
      screenshot("forestWalk"+str(scshots)+".jpg")
      scshots += 1
    elif k==10:   #key RETURN
      mc = 0
    elif k==27:  #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
quit()
