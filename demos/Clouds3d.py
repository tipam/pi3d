# Clouds 3D example using pi3d module
# ===================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.04 20Jul12 - z order improved by Paddywwoof, improved texture management
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#

import random, time

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.shape.Sprite import Sprite
from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

z = 0
x = 0
speed = 1
widex = 50
widey = 20
cloudno = 5
cloud_depth = 150.0
zd = 1.0*cloud_depth / cloudno

MARGIN = 100

# Setup display and initialise pi3d
DISPLAY = Display.create(x=MARGIN, y=MARGIN)
scnx = DISPLAY.win_width
scny = DISPLAY.win_height

DISPLAY.setBackColour(0,0.7,1,1)
camera = Camera((0, 0, 0), (0, 0, -0.1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/bumpShade")
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
  cloudi = Sprite(camera, light, size * widex, size * widey, "", 50.0*(random.random()-0.5), 0.0, cloud_depth - z)
  cloudi.buf[0].set_draw_details(shader, [clouds[int(random.random() * 4.99999)]], 0.0, -1.0)
  cxyz.append(cloudi)
  z = z + zd

camera.translate((0.0, 0.0, 50.0))

# Fetch key presses
mykeys = Keyboard()

while True:

  DISPLAY.clear()

  # this is easier to understand, the z position of each cloud is (only) held in cxyz[i].locn[2]
  # it stops the clouds appearing in front of nearer clouds!
  # first go through the clouds to find index of furthest away
  maxDepthIndex = 0
  # paint the clouds from background to foreground
  for i in range(maxDepthIndex, maxDepthIndex + cloudno):
    cloud = cxyz[i % cloudno]
    cloud.draw()
    cloud.unif[2] -= speed
    if cloud.unif[2] < -2.0:
      cloud.unif[2] = cloud_depth
      maxDepthIndex = i % cloudno


  #Press ESCAPE to terminate
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

  DISPLAY.swapBuffers()

