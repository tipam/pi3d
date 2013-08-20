#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Copy of the ForestWalk demo but with the addition of the Clashtest class
Because the clash test works by drawing only the near parts of the objects
to be checked for, it has to be done before anything else has been drawn.

First person view using ElevationMap.calcHeight function to move over
undulating surface, MergeShape.cluster to create a forest that renders quickly,
uv_reflect shader is used give texture and reflection to a monolith, fog is
applied to objects so that their details become masked with distance.
The lighting is also defined with a yellow directional tinge and an indigo tinge
to the ambient light.

There is also demonstration of the point_at method of Camera, press the D key
"""
from __future__ import absolute_import

import math, random

import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=100, y=100)
DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
# yellowish directional light blueish ambient light
pi3d.Light(lightpos=(1, -1, -3), lightcol =(1.0, 1.0, 0.7), lightamb=(0.15, 0.1, 0.3))

#========================================

# load shader
shader = pi3d.Shader("shaders/uv_reflect")
flatsh = pi3d.Shader("shaders/uv_flat")

tree2img = pi3d.Texture("textures/tree2.png")
tree1img = pi3d.Texture("textures/tree1.png")
hb2img = pi3d.Texture("textures/hornbeam2.png")
bumpimg = pi3d.Texture("textures/grasstile_n.jpg")
reflimg = pi3d.Texture("textures/stars.jpg")
rockimg = pi3d.Texture("textures/rock1.jpg")

clash = pi3d.Clashtest()

FOG = ((0.3, 0.3, 0.4, 0.5), 650.0)
TFOG = ((0.1, 0.14, 0.12, 0.3), 150.0)

#myecube = pi3d.EnvironmentCube(900.0,"HALFCROSS")
ectex=pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="cube")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
mapheight = 60.0
mountimg1 = pi3d.Texture("textures/mountains3_512.jpg")
mymap = pi3d.ElevationMap("textures/mountainsHgt.jpg", name="map",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32) #testislands.jpg
mymap.set_draw_details(shader, [mountimg1, bumpimg, reflimg], 128.0, 0.0)
mymap.set_fog(*FOG)

#Create tree models
treeplane = pi3d.Plane(w=4.0, h=5.0)

treemodel1 = pi3d.MergeShape(name="baretree")
treemodel1.add(treeplane.buf[0], 0,0,0)
treemodel1.add(treeplane.buf[0], 0,0,0, 0,90,0)

treemodel2 = pi3d.MergeShape(name="bushytree")
treemodel2.add(treeplane.buf[0], 0,0,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,60,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.MergeShape(name="trees1")
mytrees1.cluster(treemodel1.buf[0], mymap,0.0,0.0,120.0,120.0,30,"",8.0,3.0)
mytrees1.set_draw_details(flatsh, [tree2img], 0.0, 0.0)
mytrees1.set_fog(*TFOG)

mytrees2 = pi3d.MergeShape(name="trees2")
mytrees2.cluster(treemodel2.buf[0], mymap,0.0,0.0,100.0,100.0,30,"",6.0,3.0)
mytrees2.set_draw_details(flatsh, [tree1img], 0.0, 0.0)
mytrees2.set_fog(*TFOG)

mytrees3 = pi3d.MergeShape(name="trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,30,"",4.0,2.0)
mytrees3.set_draw_details(flatsh, [hb2img], 0.0, 0.0)
mytrees3.set_fog(*TFOG)

#Create monolith
monolith = pi3d.Sphere(radius=8.0, slices=12, sides=48,
                  sy=10.0, name="monolith")
monolith.translate(100.0, -mymap.calcHeight(100.0, 350) + 10.0, 350.0)
monolith.set_draw_details(shader, [rockimg, bumpimg, reflimg], 32.0, 0.3)
monolith.set_fog(*FOG)

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
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

omx, omy = mymouse.position()

CAMERA = pi3d.Camera.instance()

# Display scene and rotate cuboid
while DISPLAY.loop_running():
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm, ym, zm))

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:  #key W
      """clashtest has to be done before anything else is drawn to screen
      only the non-tranpsarent parts fo these objects nearer than 2.5 will
      be drawn
      """
      clash.draw(mytrees1)
      clash.draw(mytrees2)
      clash.draw(mytrees3)
      clash.draw(monolith)
      if not clash.check():
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
    elif k==100:  #key D now used for point_at monolith!
      rot += 2
      tilt, rot = CAMERA.point_at([monolith.x(), monolith.y(), monolith.z()])
    elif k==112:  #key P
      pi3d.screenshot("forestWalk"+str(scshots)+".jpg")
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

  # for opaque objects it is more efficient to draw from near to far as the
  # shader will not calculate pixels already concealed by something nearer
  monolith.draw()
  mytrees1.draw()
  mytrees2.draw()
  mytrees3.draw()
  mymap.draw()
  myecube.draw()

  mx, my = mymouse.position()

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot -= (mx-omx)*0.2
  tilt += (my-omy)*0.2
  omx=mx
  omy=my

  CAMERA.was_moved = False
quit()
