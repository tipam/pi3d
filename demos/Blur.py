from __future__ import absolute_import

import math,random,time

from pi3d import *

from pi3d import Display
from pi3d.Texture import Texture
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light
from pi3d.Shader import Shader

from pi3d.util.String import String
from pi3d.util.Ttffont import Ttffont
from pi3d.util.Defocus import Defocus
from pi3d.util.Screenshot import screenshot
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Sphere import Sphere
from pi3d.shape.Sprite import Sprite

# Setup display and initialise pi3d
DISPLAY = Display.create(x=10, y=10, w=1000, h=800)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

#setup textures, light position and initial model position
Light((0, 5, 0))
#create shaders
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
defocus = Defocus()

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
    myshape.add(asphere, num[0]*0.9 - 1.8*i, num[1]*0.9 -1.8*j, 0.0)
  
myshape.position(0.0, 0.0, 5.0)
myshape.set_draw_details(shader, [shapeimg, shapebump, shapeshine], 8.0, 0.0)

mysprite = Sprite(w=10.0, h=10.0)

cAngle = [0.0, 0.0, 0.0]
dx = 0.02

tick=0
next_time = time.time()+2.0

arialFont = Ttffont("fonts/FreeMonoBoldOblique.ttf", "#dd00aa")   #load ttf font and set the font colour to 'raspberry'
mystring = String(font=arialFont, string="Now the Raspberry Pi really does rock")
mystring.translate(0.0, 0.0, 1)
mystring.set_shader(flatsh)

# Fetch key presses.
mykeys = Keyboard()

# Display scene and rotate shape
while DISPLAY.loop_running():
  
  defocus.start_blur() #1
  myshape.draw()
  defocus.end_blur() #2
  defocus.blur(myshape, 6, 7, 12) #3
  #defocus.blur(mysprite, 6, 7, 20)
  
  myshape.rotateIncY(0.247)
  myshape.rotateIncX(0.1613)
  
  mysprite.translateZ(dx)
  if mysprite.z() > 15: dx = -0.02
  elif mysprite.z() < 1.0: dx = 0.02

  mystring.draw()
  mystring.rotateIncZ(0.05)

  if time.time() > next_time:
    print "FPS:",tick/2.0
    tick=0
    next_time = time.time()+2.0
    #screenshot("midpic.jpg")
  tick+=1

  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

quit()
