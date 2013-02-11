#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Simple Sprite objects fall across the screen and are moved back to the top once
they hit the bottom edge.
"""

import random, time

import demo
import pi3d

# Set last value (alpha) to zero for a transparent background!
BACKGROUND = (0.0, 0.0, 0.0, 0.0)

# Setup display and initialise pi3d and a shader.
DISPLAY = pi3d.Display.create(background=BACKGROUND)
SHADER = pi3d.Shader('shaders/uv_flat')

RASPBERRY_TEXTURE = pi3d.Texture('textures/Raspi256x256.png')
BERRY_COUNT = 15

# Setup array of random x,y,z coords and initial rotation
RASPBERRIES = []

for b in range(BERRY_COUNT):
  # Select size as a random number 0.2 and 2.5.
  size = random.uniform(0.5, 2.5)
  rasp = pi3d.Sprite(w=size, h=size)

  # distance from the camera.
  dist = random.uniform(2.0, 10.0)
  rasp.position(random.uniform(-1.0, 1.0) * dist,
                random.uniform(0.0, 4.0) * dist,
                dist)
  rasp.rotateToZ(random.uniform(0.0, 360.0))
  rasp.buf[0].set_draw_details(SHADER, [RASPBERRY_TEXTURE])

  RASPBERRIES.append(rasp)

# Fetch key presses
KEYBOARD = pi3d.Keyboard()

while DISPLAY.loop_running():
  for b in RASPBERRIES:
    b.draw()
    b.translateY(-0.3)
    b.rotateIncZ(1)
    if b.y() < -2 * b.z():
      b.positionX((random.uniform(0.0, 2.0) - 1) * b.z())
      b.translateY(4.0 * b.z())

  k = KEYBOARD.read()
  if k >-1:
    if k == 27:
      KEYBOARD.close()
      DISPLAY.stop()
      break
    elif k == 112:
      pi3d.screenshot('raspberryRain.jpg')

