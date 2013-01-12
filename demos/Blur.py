from __future__ import absolute_import
"""if in demos subdirectory, to run from geany set build command to
python ../Demo.py "%e%
"""
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
myshape.set_draw_details(shader, [shapeimg, shapebump, shapeshine], 8.0, 0.1)

mysprite = Sprite(w=20.0, h=20.0)
mysprite.position(0.0, 0.0, 15.0)
mysprite.set_draw_details(flatsh, [shapebump])

tick=0
next_time = time.time()+2.0

#load ttf font and set the font colour to 'raspberry'
arialFont = Ttffont("fonts/FreeMonoBoldOblique.ttf", "#dd00aa")
mystring = String(font=arialFont, string="blurring with distance!")
mystring.translate(0.0, 0.0, 1)
mystring.set_shader(flatsh)

# Fetch key presses.
mykeys = Keyboard()

# Display scene and rotate shape
while DISPLAY.loop_running():
  
  defocus.start_blur()
  # 1. drawing objects now renders to an offscreen texture
  mysprite.draw()
  myshape.draw()
  defocus.end_blur()
  # 2. drawing back to screen. the texture can now be used by defocus.blur()
  
  # 3. redraw these two objects applying a distance blur effect
  defocus.blur(myshape, 4, 9, 5) #4 away in focus, >= 9 5xblurring linear between
  defocus.blur(mysprite, 4, 9, 5)
  
  myshape.rotateIncY(1.247)
  myshape.rotateIncX(0.1613)
  
  mystring.draw()
  mystring.rotateIncZ(0.05)

  if time.time() > next_time:
    print "FPS:",tick/2.0
    tick=0
    next_time = time.time()+2.0
  tick+=1

  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

quit()
