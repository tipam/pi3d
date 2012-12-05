from __future__ import absolute_import

import math,random,time

from pi3d import Display
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Cuboid import Cuboid

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100)
DISPLAY.setBackColour(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

#setup textures, light position and initial model position
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, 1.6, 1.2))
light = Light((5, 5, 1))
#create shaders
shader = Shader("shaders/bumpShade")

#Create textures
shapeimg = Texture("textures/straw1.jpg")
shapebump = Texture("textures/floor_nm.jpg", True)
shapeshine = Texture("textures/stars.jpg")

#Create shape
myshape = Cuboid(camera, light, 2.0, 2.0, 2.0)
myshape.translate(0, 0, 5)

cAngle = [0.0, 0.0, 0.0]
dx = 0.05

tick=0
next_time = time.time()+1.0

myshape.buf[0].setdrawdetails(shader, [shapeimg, shapebump, shapeshine], 4.0, 0.2)
#myshape.buf[0].material = (1.0, 0.2, 0.5, 1.0)

# Display scene and rotate shape
while 1:
  DISPLAY.clear()

  camera.reset()
  #cAngle[1] += 0.5
  #camera.rotateY(cAngle[1])

  myshape.draw()

  myshape.rotateIncZ(1.247)
  myshape.rotateIncX(0.613)
  myshape.translate(dx, 0.0, 0.0)
  if myshape.x > 5: dx = -0.05
  elif myshape.x < -5: dx = 0.05
  """
  if time.time() > next_time:
    print "FPS:",tick/1.0
    tick=0
    next_time = time.time()+1.0
  tick+=1
  """
  DISPLAY.swapBuffers()
quit()
