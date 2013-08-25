#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" large panda3d egg file with detailed texture
TODO it would be nice to show a comparison with a low poly version of this
with normal mapping for the details of the model.
"""
import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50, w=-100, h=-100,
                         background = (0.2, 0.4, 0.6, 1))

shader = pi3d.Shader('uv_light')
#========================================

# load model_loadmodel
mymodel = pi3d.Model(file_string='models/Triceratops/Triceratops.egg',
                name='Triceratops', x=0, y=-1, z=40,
                sx=0.005, sy=0.005, sz=0.005)
mymodel.set_shader(shader)

# Fetch key presses
mykeys = pi3d.Keyboard()

while 1:
  DISPLAY.clear()

  mymodel.draw()
  mymodel.rotateIncZ(0.001)
  mymodel.rotateIncX(-0.00317543)
  mymodel.rotateIncY(0.11)

  k = mykeys.read()
  if k >-1:
    if k==112: pi3d.screenshot('Triceratops.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print(k)

  DISPLAY.swap_buffers()
