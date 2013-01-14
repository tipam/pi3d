import random, time

import demo
demo.demo(__name__)

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Sprite import Sprite
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create()

# Set last value (alpha) to zero for a transparent background!
DISPLAY.set_background(0.0, 0.7, 1.0, 0.0)
shader = Shader("shaders/uv_flat")
#############################

# Load textures
raspimg = Texture("textures/Raspi256x256.png")

pino=15

# Setup array of random x,y,z coords and initial rotation
raspberries=[]
for b in range (0, pino):
  rasp = Sprite(w=2.0, h=2.0)
  rasp.position(random.random()*16-8, random.random() * 16, random.random() * 4)
  rasp.rotateToZ(random.random() * 360)
  rasp.buf[0].set_draw_details(shader, [raspimg])
  raspberries.append(rasp)

# Fetch key presses
mykeys = Keyboard()

while DISPLAY.loop_running():
  for b in raspberries:
    b.draw()
    b.translateY(-0.1)
    b.rotateIncZ(1)
    if b.unif[1] < -8:
      b.positionX(random.random()*16-8)
      b.translateY(16.0)

  k = mykeys.read()
  if k >-1:
    if k==27:
      mykeys.close()
      DISPLAY.stop()
      break
    elif k==112:
      screenshot("raspberryRain.jpg")

  Camera.instance().was_moved = False #to save a tiny bit of work each loop
