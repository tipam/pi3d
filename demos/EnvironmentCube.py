#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot
from pi3d.util import Utility

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50)

shader = Shader('shaders/uv_flat')
#========================================

#select the environment cube with 'box'...
box = 3
if box == 0:
  ectex = [Texture('textures/ecubes/skybox_interstellar.jpg')]
  myecube = EnvironmentCube(size=900.0, maptype='CROSS')
elif box == 1:
  ectex = [Texture('textures/ecubes/SkyBox.jpg')]
  myecube = EnvironmentCube(size=900.0, maptype='HALFCROSS')
elif box == 2:
  ectex = loadECfiles('textures/ecubes','sbox_interstellar', nobottom=True)
  myecube = EnvironmentCube(size=900.0, maptype='FACES', nobottom=True)
else:
  ectex = loadECfiles('textures/ecubes','skybox_hall')
  myecube = EnvironmentCube(size=900.0, maptype='FACES')

myecube.set_draw_details(shader, ectex)

rot = 0.0
tilt = 0.0

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse(restrict=False)
mymouse.start()

omx, omy = mymouse.position()

CAMERA = Camera.instance()

# Display scene and rotate cuboid
while DISPLAY.loop_running():

  CAMERA.reset()
  CAMERA.rotate(tilt, 0, 0)
  CAMERA.rotate(0, rot, 0)

  myecube.draw()

  mx, my = mymouse.position()

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot -= (mx - omx)*0.4
  tilt += (my - omy)*0.4
  omx = mx
  omy = my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==112:  #key P
      screenshot('envcube.jpg')
    elif k==27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.stop()
      break
    else:
      print(k)


