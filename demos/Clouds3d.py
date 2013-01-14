#!/usr/bin/python

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
widex = 150
widey = 120
cloudno = 30
cloud_depth = 350.0
zd = 1.0*cloud_depth / cloudno

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
z = 0.0
cxyz = []
for b in range (0, cloudno):
  size = random.random()
  cloudi = Sprite(w=size * widex, h=size * widey,
                  x=50.0 * (random.random() - 0.5), y=0.0, z=cloud_depth - z)
  cloudi.buf[0].set_draw_details(shader, [clouds[int(random.random() * 4.99999)]], 0.0, -1.0)
  cxyz.append(cloudi)
  z = z + zd

CAMERA = Camera.instance()
CAMERA.position((0.0, 0.0, 50.0))

# Fetch key presses
mykeys = Keyboard()

while True:

  DISPLAY.clear()

  #TODO this is still drawing the clouds in the wrong order, needs to be sorted out

  # this is easier to understand, the z position of each cloud is (only) held in cxyz[i].unif[2]
  # it stops the clouds appearing in front of nearer clouds!
  # first go through the clouds to find index of furthest away
  maxDepthIndex = 0
  maxDepth = -100
  for i, cloud in enumerate(cxyz):
    if cloud.unif[2] > maxDepth:
      maxDepth = cloud.unif[2]
      maxDepthIndex = i

  # paint the clouds from background to foreground
  for i in range(maxDepthIndex, maxDepthIndex + cloudno):
    cloud = cxyz[i % cloudno]
    cloud.draw()
    cloud.translateZ(-speed)
    if cloud.unif[2] < -2.0:
      cloud.positionZ(cloud_depth)



  #Press ESCAPE to terminate
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

  CAMERA.was_moved = False
  DISPLAY.swapBuffers()

