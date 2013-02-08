#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Simple Sprite objects fall across the screen and are moved back to the
top once they have the bottom edge
"""
import random, time

import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()

# Set last value (alpha) to zero for a transparent background!
DISPLAY.set_background(0.0, 0.7, 1.0, 0.0)
shader = pi3d.Shader("shaders/uv_flat")
#############################

# Load textures
raspimg = pi3d.Texture("textures/Raspi256x256.png")

pino = 15

# Setup array of random x,y,z coords and initial rotation
raspberries=[]
for b in range (0, pino):
  size = random.random() * 2.0 + 0.5
  rasp = pi3d.Sprite(w=size, h=size)
  dist = random.random() * 8.0 + 2.0
  rasp.position((random.random()*2.0 - 1.0) * dist, (random.random() * 4) * dist, dist)
  rasp.rotateToZ(random.random() * 360)
  rasp.buf[0].set_draw_details(shader, [raspimg])
  raspberries.append(rasp)

# Fetch key presses
mykeys = pi3d.Keyboard()

while DISPLAY.loop_running():
  for b in raspberries:
    b.draw()
    b.translateY(-0.3)
    b.rotateIncZ(1)
    if b.y() < -2 * b.z():
      b.positionX((random.random()*2 - 1) * b.z())
      b.translateY(4.0 * b.z())

  k = mykeys.read()
  if k >-1:
    if k==27:
      mykeys.close()
      DISPLAY.stop()
      break
    elif k==112:
      pi3d.screenshot("raspberryRain.jpg")

  pi3d.Camera.instance().was_moved = False #to save a tiny bit of work each loop
