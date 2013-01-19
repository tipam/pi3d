#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random,time

import demo

from pi3d.constants import *

from pi3d import Display
from pi3d.Texture import Texture
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light
from pi3d.Shader import Shader

from pi3d.shape.Sphere import Sphere
from pi3d.util.String import String
from pi3d.util.Ttffont import Ttffont
from pi3d.shape.MergeShape import MergeShape

# Setup display and initialise pi3d
DISPLAY = Display.create(x=10, y=10, w=1000, h=800)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

#setup textures, light position and initial model position
Light((0, 5, 0))
#create shaders
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")

#Create textures
shapeimg = Texture("textures/straw1.jpg")
shapebump = Texture("textures/floor_nm.jpg", True)
shapeshine = Texture("textures/pong3.png")

#Create shape
myshape = MergeShape()
num = (2, 2)
asphere = Sphere(sides=32)
for i in range(num[0]):
  for j in range(num[1]):
    myshape.add(asphere, -num[0]*0.9 + 1.8*i, -num[1]*0.9 +1.8*j, 0.0)

myshape.position(0.0, 0.0, 5)
myshape.set_draw_details(shader, [shapeimg, shapebump, shapeshine], 8.0, 0.0, 2.0, 2.0)
#light2 = Light((-5, -5, i - 3))
#myshape.set_light(light2)

cAngle = [0.0, 0.0, 0.0]
dx = 0.05

tick=0
next_time = time.time()+10.0

arialFont = Ttffont("fonts/FreeMonoBoldOblique.ttf", "#dd00aa")   #load ttf font and set the font colour to 'raspberry'
mystring = String(font=arialFont, string="Now the Raspberry Pi really does rock")
mystring.translate(0.0, 0.0, 1)
mystring.set_shader(flatsh)

# Fetch key presses.
mykeys = Keyboard()

# Display scene and rotate shape
while DISPLAY.loop_running():

  #camera.reset()
  #cAngle[1] += 0.5
  #camera.rotateY(cAngle[1])

  myshape.draw()
  myshape.rotateIncY(0.247)
  myshape.rotateIncZ(0.1613)
  myshape.translateX(dx)
  if myshape.x() > 5: dx = -0.05
  elif myshape.x() < -5: dx = 0.05


  mystring.draw()
  mystring.rotateIncZ(0.05)

  #camera.was_moved = False

  if time.time() > next_time:
    print("FPS:",tick/10.0)
    tick=0
    next_time = time.time()+10.0
  tick+=1

  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

quit()
