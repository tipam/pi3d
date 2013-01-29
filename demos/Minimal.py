import demo
import pi3d
DISPLAY = pi3d.Display.create(x=100, y=100)
shader = pi3d.Shader("shaders/2d_flat")
sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader)
mkeys = pi3d.Keyboard()
while DISPLAY.loop_running():
  sprite.draw()
  k = mkeys.read()
  if k > -1:
    mykeys.close()
    DISPLAY.destroy()
    break

