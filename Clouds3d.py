#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Simple 'sprite' images are moved towards the camera position to give the
illusion of movement through clouds, uses the uv_flat shader to simply show
the image with no lighting effect, blend is set to True so that parts of the
image with alpha less than 1 are merged with the images already drawn but
further from the camera. Because of this it is important that the clouds are
drawn from furthest to nearest (the opposite to opaque objects)
"""

import random, time

import demo
import pi3d

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
DISPLAY = pi3d.Display.create(x=MARGIN, y=MARGIN)
scnx = DISPLAY.width
scny = DISPLAY.height

DISPLAY.set_background(0,0.7,1,1)
shader = pi3d.Shader("uv_flat")
#############################

cloudTex = []
cloudTex.append(pi3d.Texture("textures/cloud2.png",True))
cloudTex.append(pi3d.Texture("textures/cloud3.png",True))
cloudTex.append(pi3d.Texture("textures/cloud4.png",True))
cloudTex.append(pi3d.Texture("textures/cloud5.png",True))
cloudTex.append(pi3d.Texture("textures/cloud6.png",True))

# Setup cloud positions and cloud image refs
cz = 0.0
clouds = [] # an array for the clouds
for b in range (0, cloudno):
  size = 0.5 + random.random()/2.0
  cloud = pi3d.Sprite(w=size * widex, h=size * widey,
          x=150.0 * (random.random() - 0.5), y=0.0, z=cloud_depth - cz)
  cloud.set_draw_details(shader, [cloudTex[int(random.random() * 4.99999)]], 0.0, 0.0)
  clouds.append(cloud)
  cz = cz + zd

CAMERA = pi3d.Camera.instance()
CAMERA.position((0.0, 0.0, 50.0))
CAMERA.was_moved = False
# Fetch key presses
mykeys = pi3d.Keyboard()

while DISPLAY.loop_running():
  # the z position of each cloud is held in clouds[i].unif[2] returned by cloud.z()
  # it stops the clouds being drawn behind nearer clouds and pixels being
  # discarded by the shader! that should be blended.
  # first go through the clouds to find index of furthest away
  maxDepthIndex = 0
  maxDepth = -100
  for i, cloud in enumerate(clouds):
    if cloud.z() > maxDepth:
      maxDepth = cloud.z()
      maxDepthIndex = i

  # paint the clouds from background to foreground
  # normally not the most efficient order but has to be done this way for low alpha
  for i in range(cloudno):
    cloud = clouds[(maxDepthIndex + i) % cloudno]
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
