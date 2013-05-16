#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" The basic ForestWalk but with shadows cast onto the ElevationMap using 
the ShadowCaster class.
Also demonstrates passing an array of objects to the MergeShape.merge()
method which is much faster for adding large numbers of objects
"""

import demo

import math,random

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane
from pi3d.shape.Sphere import Sphere

from pi3d.util.Screenshot import screenshot
from pi3d.util.ShadowCaster import ShadowCaster


# Setup display and initialise pi3d
DISPLAY = Display.create(x=0, y=0, w=800, h=600)
DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
# yellowish directional light blueish ambient light
#TODO doesn't cope with z direction properly
mylight = Light(lightpos=(0.5, -1.0, 0.0), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))
CAMERA = Camera.instance()

#========================================
# load shader
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")

tree2img = Texture("textures/tree2.png")
tree1img = Texture("textures/tree1.png")
hb2img = Texture("textures/hornbeam2.png")
bumpimg = Texture("textures/grasstile_n.jpg")
reflimg = Texture("textures/stars.jpg")
rockimg = Texture("textures/rock1.jpg")

FOG = ((0.3, 0.3, 0.4, 0.5), 650.0)
TFOG = ((0.2, 0.24, 0.22, 0.3), 150.0)

#myecube = EnvironmentCube(900.0,"HALFCROSS")
ectex=loadECfiles("textures/ecubes","sbox")
myecube = EnvironmentCube(size=900.0, maptype="FACES", name="cube")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
mapheight = 45.0 # can't cope with much elevation
mountimg1 = Texture("textures/mountains3_512.jpg")
mymap = ElevationMap("textures/mountainsHgt.jpg", name="map",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32) #testislands.jpg
mymap.set_draw_details(shader, [mountimg1, bumpimg, bumpimg], 128.0, 0.0)
mymap.set_fog(*FOG)

#Create tree models
treeplane = Plane(w=4.0, h=5.0)

treemodel1 = MergeShape(name="baretree")
treemodel1.merge([[treeplane, 0,0,0, 0,0,0, 1,1,1],
                [treeplane, 0,0,0, 0,90,0, 1,1,1]])

treemodel2 = MergeShape(name="bushytree")
treemodel2.merge([[treeplane, 0,0,0, 0,0,0, 1,1,1],
                [treeplane, 0,0,0, 0,60,0, 1,1,1],
                [treeplane, 0,0,0, 0,120,0, 1,1,1]])

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape(name="trees1")
mytrees1.cluster(treemodel1.buf[0], mymap, 50.0, 200.0, 50.0, 500.0, 50, "", 5.0, 20.0)
mytrees1.set_draw_details(flatsh, [tree2img], 0.0, 0.0)
mytrees1.set_fog(*TFOG)

mytrees2 = MergeShape(name="trees2")
mytrees2.cluster(treemodel2.buf[0], mymap, 0.0, 0.0, 200.0, 300.0, 50,"",3.0,7.0)
mytrees2.set_draw_details(flatsh, [tree1img], 0.0, 0.0)
mytrees2.set_fog(*TFOG)

mytrees3 = MergeShape(name="trees3")
mytrees3.cluster(treemodel2, mymap,0.0, 0.0, 600.0, 100.0, 50,"", 4.0, 20.0)
mytrees3.set_draw_details(flatsh, [hb2img], 0.0, 0.0)
mytrees3.set_fog(*TFOG)

#is it a bird? is it a plane?
myplane = Plane(h=80.0, w=80.0)
myplane.set_draw_details(shader, [rockimg, bumpimg, reflimg], 2.0, 0.6)
xrot, yrot, zrot = 90.0, 0.0, 0.0 #degrees
dxrot, dyrot, dzrot = 0.01, 0.22, 0.061
radius = 100.0
angle = 0.0
rotn = 0.012 #radians
elev = 80.0

myshadows = ShadowCaster(emap=mymap, light=mylight)

#screenshot number
scshots = 1

#avatar camera
rot = 0.0
tilt = 0.0
avhgt = 3.5
xm = 0.0
zm = 0.0
ym = mymap.calcHeight(xm, zm) + avhgt

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse(restrict = False)
mymouse.start()

omx, omy = mymouse.position()

# main loop
while DISPLAY.loop_running():
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm, ym, zm))
  
  xrot += dxrot
  yrot += dyrot
  zrot += dzrot
  angle += rotn
  myplane.position(radius * math.cos(angle) - radius, elev, radius * math.sin(angle))
  myplane.rotateToX(xrot)
  myplane.rotateToY(yrot)
  myplane.rotateToZ(zrot)

  # put the shadows onto the shadowcaster texture
  myshadows.start_cast((xm, ym, zm))
  myshadows.add_shadow(mytrees1)
  myshadows.add_shadow(mytrees2)
  myshadows.add_shadow(mytrees3)
  myshadows.add_shadow(myplane)
  myshadows.end_cast()
  
  myplane.draw()
  mytrees1.draw()
  mytrees2.draw()
  mytrees3.draw()
  
  myshadows.draw_shadow() # this draws the elevation map passed to it in constructor
  myecube.draw()

  mx, my = mymouse.position()

  rot -= (mx-omx)*0.2
  tilt += (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:  #key W
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))
      ym = mymap.calcHeight(xm, zm) + avhgt
    elif k==115:  #kry S
      xm += math.sin(math.radians(rot))
      zm -= math.cos(math.radians(rot))
      ym = mymap.calcHeight(xm, zm) + avhgt
    elif k==39:   #key '
      tilt -= 2.0
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
      DISPLAY.stop()
      break
    else:
      print(k)

  CAMERA.was_moved = False
quit()
