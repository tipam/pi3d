import ctypes
import demo
import pi3d
from pi3d.constants import *
DISPLAY = pi3d.Display.create(w=400, h=300)
shader = pi3d.Shader("shaders/2d_flat")
sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader)
maxtex = ctypes.c_int(0)
opengles.glGetIntegerv(GL_MAX_TEXTURE_SIZE, ctypes.byref(maxtex))
print(maxtex)
while DISPLAY.loop_running():
  sprite.draw()

