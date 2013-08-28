#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" 3D model loading: complex architectural model with multiple vertex groups
and images
"""
import math, random

import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=100, y=100)
DISPLAY.set_background(1.0,0.4,0.6,1)    	# r,g,b,alpha
pi3d.Light((5, -10, -20), (0.6, 0.6, 0.5), (0.3, 0.3, 0.4))

# load shader
shader = pi3d.Shader("uv_light")
flatsh = pi3d.Shader("uv_flat")

print("==============================================================")
print("Instructions:")
print("")
print("Keys-             W - Forward,")
print("        A - Left   S - Back     D - right")
print("")
print("Move mouse to pan view.  Click mouse to exit or press ESCAPE")
print("==============================================================")

ectex = pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES",
                          name="bfa", y=50.0)
myecube.set_draw_details(flatsh, ectex)

# load model_loadmodel
mymodel = pi3d.Model(
  file_string="models/Buckfast Abbey/BuckfastAbbey.egg",
  name="Abbey",
  rx=90, sx=0.03, sy=0.03, sz=0.03)

mymodel.set_shader(shader)

# Create keyboard and mouse event objects
mykeys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

#screenshot number
scshots = 1

#avatar camera
rot = 220.0
tilt = 10.0
avhgt = 2.0
xm = 0.0
zm = 0.0
ym = avhgt

omx, omy = mymouse.position()
CAMERA = pi3d.Camera.instance()

while DISPLAY.loop_running():
  CAMERA.reset()
  CAMERA.rotate(tilt, 0, 0)
  CAMERA.rotate(0, rot, 0)
  CAMERA.position((xm, ym, zm))

  mymodel.draw()
  myecube.draw()

  mx, my = mymouse.position()

  rot -= (mx-omx)*0.8
  tilt += (my-omy)*0.8
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k > -1:
    if k == 119:    #key W
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))
    elif k == 115:  #kry S
      xm += math.sin(math.radians(rot))
      zm -= math.cos(math.radians(rot))
    elif k == 39:   #key '
      tilt -= 2.0
      print(tilt)
    elif k == 47:   #key /
      tilt += 2.0
    elif k == 97:   #key A
      rot -= 2
    elif k == 100:  #key D
      rot += 2
    elif k == 112:  #key P
      pi3d.screenshot("BuckfastAbbey"+str(scshots)+".jpg")
      scshots += 1
    elif k == 27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print(k)

quit()
