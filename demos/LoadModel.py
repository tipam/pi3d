#!/usr/bin/python

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.Shader import Shader
from pi3d.context.Light import Light

from pi3d.shape.Model import Model
from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100, background=(0.2, 0.4, 0.6, 1))

Light((1, 1, 1))

shader = Shader("shaders/mat_reflect")
#========================================
# load bump and reflection textures
bumptex = Texture("textures/floor_nm.jpg")
shinetex = Texture("textures/stars.jpg")

# load model_loadmodel
mymodel = Model(file_string='models/teapot.egg', name='teapot', x=0, y=-2, z=8)
mymodel.set_shader(shader)
# material is set in the file
mymodel.set_normal_shine(bumptex, 4.0, shinetex, 0.2, is_uv = False)

# Fetch key presses
mykeys = Keyboard()

while DISPLAY.loop_running():
  mymodel.draw()
  mymodel.rotateIncY(2.0)
  mymodel.rotateIncZ(0.1)
  mymodel.rotateIncX(0.3)

  k = mykeys.read()
  if k >-1:
    if k == 112:
      screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.close()
      break
    else:
      print k
