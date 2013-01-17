#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Wavefront obj model loading. Material properties set in mtl file.
"""
import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.Shader import Shader

from pi3d.shape.Model import Model
from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100,
                         background=(0.2, 0.4, 0.6, 1))

shader = Shader("shaders/uv_reflect")
#========================================
# load bump and reflection textures
bumptex = Texture("textures/floor_nm.jpg")
shinetex = Texture("textures/stars.jpg")

# load model_loadmodel
mymodel = Model(file_string='models/teapot.obj', name='teapot', z=4)
mymodel.set_shader(shader)
mymodel.set_normal_shine(bumptex, 16.0, shinetex, 0.5)


# Fetch key presses
mykeys = Keyboard()

while 1:
  DISPLAY.clear()

  mymodel.draw()
  mymodel.rotateIncY(2.0)
  mymodel.rotateIncZ(0.1)
  mymodel.rotateIncX(0.3)

  k = mykeys.read()
  if k >-1:
    if k==112:
      screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print(k)

  DISPLAY.swapBuffers()
