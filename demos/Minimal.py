import demo
import pi3d

DISPLAY = pi3d.Display.create(w=400, h=300)
shader = pi3d.Shader("shaders/2d_flat")
sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader)

while DISPLAY.loop_running():
  sprite.draw()

