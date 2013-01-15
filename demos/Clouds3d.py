#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import random, time

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.shape.Sprite import Sprite
from pi3d.Camera import Camera
from pi3d.Shader import Shader

z = 0
x = 0
speed = 1
widex = 100
widey = 80
cloudno = 20
cloud_depth = 350.0
zd = 1.0 * cloud_depth / cloudno

MARGIN = 100

# Setup display and initialise pi3d
DISPLAY = Display.create(x=MARGIN, y=MARGIN)
scnx = DISPLAY.width
scny = DISPLAY.height

DISPLAY.set_background(0,0.7,1,1)
shader = Shader("shaders/uv_flat")
#############################

clouds = []
clouds.append(Texture("textures/cloud2.png",True))
clouds.append(Texture("textures/cloud3.png",True))
clouds.append(Texture("textures/cloud4.png",True))
clouds.append(Texture("textures/cloud5.png",True))
clouds.append(Texture("textures/cloud6.png",True))

# Setup cloud positions and cloud image refs
cz = 0.0
cxyz = []
for b in range (0, cloudno):
  size = 0.5 + random.random()/2.0
  #TODO if the position is set in the constructor, needs to be sorted
  #cloudi = Sprite(w=size * widex, h=size * widey)
  #cloudi.position(150.0 * (random.random() - 0.5), 0.0, cloud_depth - cz)
  cloudi = Sprite(w=size * widex, h=size * widey, x=150.0 * (random.random() - 0.5), y=0.0, z=cloud_depth - cz)
  cloudi.set_draw_details(shader, [clouds[int(random.random() * 4.99999)]], 0.0, 0.0)
  cxyz.append(cloudi)
  cz = cz + zd

CAMERA = Camera.instance()
CAMERA.position((0.0, 0.0, 50.0))

# Fetch key presses
mykeys = Keyboard()

while True:

  DISPLAY.clear()

  # the z position of each cloud is held in cxyz[i].unif[2] returned by cloud.z()
  # it stops the clouds being drawn behind nearer clouds and pixels being 
  # discarded by the shader! that should be blended.
  # first go through the clouds to find index of furthest away
  maxDepthIndex = 0
  maxDepth = -100
  for i, cloud in enumerate(cxyz):
    if cloud.z() > maxDepth:
      maxDepth = cloud.z()
      maxDepthIndex = i

  # paint the clouds from background to foreground
  # normally not the most efficient order but has to be done this way for low alpha
  for i in range(cloudno):
    cloud = cxyz[(maxDepthIndex + i) % cloudno]
    cloud.draw()
    cloud.translateZ(-speed)
    if cloud.z() < -20.0:
      # send to back
      cloud.positionZ(cloud_depth)



  #Press ESCAPE to terminate
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

  CAMERA.was_moved = False
  DISPLAY.swapBuffers()

