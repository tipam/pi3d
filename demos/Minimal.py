import demo
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50)
shader = pi3d.Shader("shaders/2d_flat")
sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader, w=10.0, h=10.0, z=1.0)

mykeys = pi3d.Keyboard()
while DISPLAY.loop_running():
  sprite.draw()
  
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break

