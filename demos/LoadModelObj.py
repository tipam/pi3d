from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.Camera import Camera
from pi3d.Shader import Shader
from pi3d.context.Light import Light

from pi3d.shape.Model import Model
from pi3d.util.Matrix import Matrix
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100)
DISPLAY.setBackColour(r=0.2, g=0.4, b=0.6, alpha=1)


camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((10, 10, -20))
shader = Shader("shaders/uv_reflect")
#========================================
# load bump and reflection textures
bumptex = Texture("textures/floor_nm.jpg")
shinetex = Texture("textures/stars.jpg")


# load model_loadmodel
mymodel = Model(camera, light, 'models/teapot.obj' ,'teapot', 0, 0, 4)
mymodel.set_shader(shader)
mymodel.set_normal_shine(bumptex, 16.0, shinetex, 0.5)


# Fetch key presses
mykeys = Keyboard()

while 1:
  DISPLAY.clear()

  mymodel.draw()
  mymodel.rotateIncY(2.0)
  mymodel.rotateIncZ(0.1)
  mymodel.rotateIncX(0.3)

  k = mykeys.read()
  if k >-1:
    if k==112:
      screenshot('teapot.jpg')
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
