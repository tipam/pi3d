#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Different types of environment cube mapping. Change them by setting box to
values 0 to 3. in nobottom is set to True then that image can be absent, the
drawing will use the previous image which is top
"""
import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50)

shader = pi3d.Shader('uv_flat')
#========================================

#select the environment cube with 'box'...
box = 3
if box == 0:
  ectex = [pi3d.Texture('textures/ecubes/skybox_interstellar.jpg')]
  myecube = pi3d.EnvironmentCube(size=900.0, maptype='CROSS')
elif box == 1:
  ectex = [pi3d.Texture('textures/ecubes/SkyBox.jpg')]
  myecube = pi3d.EnvironmentCube(size=900.0, maptype='HALFCROSS')
elif box == 2:
  ectex = pi3d.loadECfiles('textures/ecubes','sbox_interstellar', nobottom=True)
  myecube = pi3d.EnvironmentCube(size=900.0, maptype='FACES', nobottom=True)
else:
  ectex = pi3d.loadECfiles('textures/ecubes','skybox_hall')
  myecube = pi3d.EnvironmentCube(size=900.0, maptype='FACES')

myecube.set_draw_details(shader, ectex)

rot = 0.0
tilt = 0.0

# Fetch key presses
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict=False)
mymouse.start()

omx, omy = mymouse.position()

CAMERA = pi3d.Camera.instance()

# Display scene and rotate cuboid
while DISPLAY.loop_running():

  CAMERA.reset()
  CAMERA.rotate(tilt, 0, 0)
  CAMERA.rotate(0, rot, 0)

  myecube.draw()

  mx, my = mymouse.position()

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot -= (mx - omx)*0.4
  tilt += (my - omy)*0.4
  omx = mx
  omy = my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==112:  #key P
      pi3d.screenshot('envcube.jpg')
    elif k==27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.stop()
      break
    else:
      print(k)


