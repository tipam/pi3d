# Environment Cube examples using pi3d module
# ===========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 20Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader
from pi3d.context.Light import Light

from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles

from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot
from pi3d.util import Utility

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50)

camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_flat")
#========================================

#select the environment cube with 'box'...
box = 3
if box == 0:
  ectex = [Texture("textures/ecubes/skybox_interstellar.jpg")]
  myecube = EnvironmentCube(camera, light, 900.0,"CROSS")
elif box == 1:
  ectex = [Texture("textures/ecubes/SkyBox.jpg")]
  myecube = EnvironmentCube(camera, light, 900.0,"HALFCROSS")
elif box == 2:
  ectex = loadECfiles("textures/ecubes","sbox_interstellar")
  myecube = EnvironmentCube(camera, light, 900.0,"FACES")
else:
  ectex = loadECfiles("textures/ecubes","skybox_hall")
  myecube = EnvironmentCube(camera, light, 900.0,"FACES")
for i, b in enumerate(myecube.buf):
  b.set_draw_details(shader, [ectex[i]], 0.0, -1.0)

rot=0.0
tilt=0.0

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

omx = mymouse.x
omy = mymouse.y

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  camera.reset()
  camera.rotate(tilt, 0, 0)
  camera.rotate(0, rot, 0)

  myecube.draw()

  mx=mymouse.x
  my=mymouse.y

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==112:  #key P
      screenshot("envcube.jpg")
    elif k==27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()

quit()


