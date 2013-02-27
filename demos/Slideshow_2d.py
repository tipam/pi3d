#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import random, time, glob

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader
from pi3d.shape.Sprite import ImageSprite

# Setup display and initialise pi3d

DISPLAY = Display.create(background=(0.0, 0.0, 0.0, 0.0), x=100, y=100)

shader = Shader("shaders/2d_flat")
#############################

# Setup sprite
""" ImageSprite is just the 'canvas' to draw the 2d onto, it needs to be bigger
than the screen, that's all. z value will be used as depth by the shader
as it decides what to draw and what to discard """
slide = []
maxslides = 15
iFiles = glob.glob("textures/*.jpg")
for i, f in enumerate(iFiles):
  """ here the images are scaled to fit the Display size, if they were to be
  rendered pixel for pixel as the original then the mipmap=False argument would
  be used, which is much faster, and w and h values set to the Texture size i.e.

  tex = Texture(f, mipmap=False)
  ...
  wi, hi = tex.ix, tex.iy

  NB if some textures are set with different values of mipmap then the last one
  loaded will define how the global behaviour is set.
  """
  tex = Texture(f)
  #tex = Texture(f, mipmap=False)
  slide.append(ImageSprite(tex, shader, w=10.0, h=10.0, z=0.1))
  xrat = DISPLAY.width/tex.ix
  yrat = DISPLAY.height/tex.iy
  if yrat < xrat:
    xrat = yrat
  wi, hi = tex.ix * xrat, tex.iy * xrat
  #wi, hi = tex.ix, tex.iy
  xi = (DISPLAY.width - wi)/2
  yi = (DISPLAY.height - hi)/2
  slide[i].set_2d_size(w=wi, h=hi, x=xi, y=yi)
  if i > maxslides:
    break
    
num = len(slide)
pici = 0
tm = 2.56

next_time = time.time() + tm

# Fetch key presses
mykeys = Keyboard()
CAMERA = Camera.instance()
CAMERA.was_moved = False #to save a tiny bit of work each loop

while DISPLAY.loop_running():
  slide[pici].draw()

  if time.time() > next_time:
    pici = (pici + 1) % num
    if pici == 0 and tm > 0.001:
      tm = tm/2.0
    next_time = time.time() + tm

  k = mykeys.read()
  if k >-1:
    if k==27: #ESC
      mykeys.close()
      DISPLAY.stop()
      break

