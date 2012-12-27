# Raspberry Rain example using pi3d module
# ========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.03 - 20Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#	  $ sudo apt-get install python-imaging
#
# before running this example
#
# Rasperry rain demonstrates pi3d sprites over the desktop.
# The sprites make use of the z value in a perspective view

import random, time

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Sprite import Sprite
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create()

# Set last value (alpha) to zero for a transparent background!
DISPLAY.set_background(0.0, 0.7, 1.0, 0.0)
camera = Camera((0, 0, 0), (0, 0, -0.1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_flat")
#############################

# Load textures
raspimg = Texture("textures/Raspi256x256.png")

pino=15

# Setup array of random x,y,z coords and initial rotation
raspberries=[]
for b in range (0, pino):
  rasp = Sprite(camera, light, 2.0, 2.0)
  rasp.position(random.random()*16-8, random.random() * 16, random.random() * 4)
  rasp.rotateToZ(random.random() * 360)
  rasp.buf[0].set_draw_details(shader, [raspimg])
  raspberries.append(rasp)

# Fetch key presses
mykeys = Keyboard()

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  for b in raspberries:
    b.draw()
    b.translateY(-0.1)
    b.rotateIncZ(1)
    if b.unif[1] < -8:
      b.positionX(random.random()*16-8)
      b.translateY(16.0)

  k = mykeys.read()
  if k >-1:
    if k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    elif k==112:
      screenshot("raspberryRain.jpg")

  DISPLAY.swapBuffers()
