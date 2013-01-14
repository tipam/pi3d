from __future__ import absolute_import

import math,random

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.Model import Model

from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100)
DISPLAY.set_background(1.0,0.4,0.6,1)    	# r,g,b,alpha
Light((5, 10, 20))

# load shader
shader = Shader("shaders/uv_light")
flatsh = Shader("shaders/uv_flat")

print "=============================================================="
print "Instructions:"
print ""
print "Keys-             W - Forward,"
print "        A - Left   S - Back     D - right"
print ""
print "Move mouse to pan view.  Click mouse to exit or press ESCAPE"
print "=============================================================="

ectex = loadECfiles("textures/ecubes","sbox")
myecube = EnvironmentCube(size=900.0, maptype="FACES",
                          name="bfa", y=50.0)
myecube.set_draw_details(flatsh, ectex)

# load model_loadmodel
mymodel = Model(file_string="models/Buckfast Abbey/BuckfastAbbey.egg",
                name="Abbey",
                rx=-90, sx=0.03, sy=0.03, sz=0.03)
mymodel.set_shader(shader)

# Create keyboard and mouse event objects
mykeys = Keyboard()
mymouse = Mouse(restrict = False)
mymouse.start()

#screenshot number
scshots = 1

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym = avhgt

omx, omy = mymouse.position()
CAMERA = Camera.instance()

while 1:
  DISPLAY.clear()

  CAMERA.reset()
  CAMERA.rotate(tilt, 0, 0)
  CAMERA.rotate(0, rot, 0)
  CAMERA.position((xm, ym, zm))

  myecube.draw()
  mymodel.draw()

  mx, my = mymouse.position()

  if mx>DISPLAY.left and mx<DISPLAY.right and my>DISPLAY.top and my<DISPLAY.bottom:
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
      print tilt
    elif k == 47:   #key /
      tilt += 2.0
    elif k == 97:   #key A
      rot -= 2
    elif k == 100:  #key D
      rot += 2
    elif k == 112:  #key P
      screenshot("BuckfastAbbey"+str(scshots)+".jpg")
      scshots += 1
    elif k == 27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
quit()
