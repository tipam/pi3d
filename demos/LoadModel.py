#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" pi3d.Model loaded from panda3d egg file. Diffuse colours picked up from file,
would be overridden if texture file defined. Althou normal mapping is defined
it cannot be used (and has no effect) because there are no u-v coordinates
defined in this egg file
"""
import demo

import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=100, y=100, background=(0.2, 0.4, 0.6, 1))

pi3d.Light((1, 1, 1))

shader = pi3d.Shader("mat_reflect")
#========================================
# load bump and reflection textures
bumptex = pi3d.Texture("textures/floor_nm.jpg")
shinetex = pi3d.Texture("textures/stars.jpg")

# load model_loadmodel
mymodel = pi3d.Model(file_string='models/teapot.egg', name='teapot', x=0, y=0, z=10)
mymodel.set_shader(shader)

# material is set in the file
mymodel.set_normal_shine(bumptex, 4.0, shinetex, 0.2, is_uv = False)

# Fetch key presses
mykeys = pi3d.Keyboard()

while DISPLAY.loop_running():
  mymodel.draw()
  mymodel.rotateIncY(2.0)
  mymodel.rotateIncZ(0.1)
  mymodel.rotateIncX(0.3)

  k = mykeys.read()
  if k >-1:
    if k == 112:
      pi3d.screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print(k)
