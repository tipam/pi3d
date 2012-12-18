from __future__ import absolute_import

import math,random,time

from pi3d import Display
from pi3d.Texture import Texture
from pi3d.Keyboard import Keyboard

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Tube import Tube
from pi3d.util.String import String
from pi3d.util.Font import Font

# Setup display and initialise pi3d
DISPLAY = Display.create(x=10, y=10, w=1000, h=800)
DISPLAY.setBackColour(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

#setup textures, light position and initial model position
camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((5, 5, 1))
#create shaders
shader = Shader("shaders/bumpShade")

#Create textures
shapeimg = Texture("textures/straw1.jpg")
shapebump = Texture("textures/floor_nm.jpg", True)
shapeshine = Texture("textures/stars.jpg")

#Create shape
myshape = []
num = 4
for i in range(num):
  myshape.append(Tube(camera, light, sides=32))
  myshape[i].translate(0, -num +2*i, 10)
  myshape[i].buf[0].set_draw_details(shader, [shapeimg, shapebump, shapeshine], 0.0, 0.0)

cAngle = [0.0, 0.0, 0.0]
dx = 0.05

tick=0
next_time = time.time()+10.0

arialFont = Font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
mystring = String(camera, light, arialFont, "RaspberryPi-Rocks")
#mystring.translate(0.0, 0.0, 1)
mystring.set_shader(shader)

#myshape.buf[0].set_draw_details(shader, [shapeimg, shapebump, shapeshine], 0.0, 0.0)
#myshape.buf[1].set_draw_details(shader, [shapebump, shapebump, shapeshine], 4.0, 0.2)
#myshape.buf[2].set_draw_details(shader, [shapeshine, shapebump, shapeshine], 4.0, 0.2)
#myshape.buf[0].material = (1.0, 0.2, 0.5, 1.0)

# Fetch key presses. This line has to be commented out to see the FPS printout
mykeys = Keyboard()

# Display scene and rotate shape
while True:
  DISPLAY.clear()

  #camera.reset()
  #cAngle[1] += 0.5
  #camera.rotateY(cAngle[1])
  
  for s in myshape:
    s.draw()
    s.rotateIncY(1.247)
    s.rotateIncZ(0.613)
    s.translateX(dx)
    if s.unif[0] > 5: dx = -0.05
    elif s.unif[0] < -5: dx = 0.05


  mystring.draw()
  mystring.rotateIncZ(0.05)
  
  #camera.movedFlag = False
  
  if time.time() > next_time:
    print "FPS:",tick/10.0
    tick=0
    next_time = time.time()+10.0
  tick+=1
  
  DISPLAY.swapBuffers()
  #""" # this block needs to be commented out to be able to see the FPS readout (actually the creation of the Keyboard instance above is what does it)
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
  #"""
quit()
