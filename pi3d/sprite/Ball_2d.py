import ctypes
from numpy import dot

from pi3d.constants import *

from pi3d.Display import Display

class Ball_2d(object):
  """ This class is used to take some of the functionality of the CollisionBalls
  demo out of the main file. It inherits from the ImageSprite class that is
  passed (in addition to standard Shape constructor arguments) the Shader and
  the [Texture] to use.
  In order to fit the Display dimensions the z value has to be set to 1000
  This allows the Ball dimensions to be set in approximately pixel sizes
  """
  def __init__(self, canvas=None, texture=None, radius=0.0,
                x=0.0, y=0.0, vx=0.0, vy=0.0):
    self.canvas = canvas
    self.texture = texture
    self.radius = radius
    self.x = x
    self.y = y
    self.w = 2.0 * radius
    self.h = 2.0 * radius
    self.vx = vx
    self.vy = vy
    self.mass = radius * radius
    opengles.glEnable(GL_SCISSOR_TEST)

  def move(self):
    self.translateX(self.vx)
    self.translateY(self.vy)

  def hit(self, otherball):
    """Used for pre-checking ball positions."""
    dx = (self.x + self.vx) - (otherball.x + otherball.vx)
    dy = (self.y + self.vy) - (otherball.y + otherball.vy)
    rd = self.radius + otherball.radius
    return dot(dx, dy) <= (rd * rd)

  def bounce_collision(self, otherball):
    """work out resultant velocities using 17th.C phsyics"""
    # relative positions
    dx = self.x - otherball.x
    dy = self.y - otherball.y
    rd = self.radius + otherball.radius
    # check sign of a.b to see if converging
    dotP = dot([dx, dy, 0],
               [self.vx - otherball.vx, self.vy - otherball.vy, 0])
    if dx * dx + dy * dy <= rd * rd and dotP < 0:
      R = otherball.mass / self.mass #ratio of masses
      """Glancing angle for equating angular momentum before and after collision.
      Three more simultaneous equations for x and y components of momentum and
      kinetic energy give:
      """
      if dy:
        D = dx / dy
        delta2y = 2 * (D * self.vx + self.vy -
                       D * otherball.vx - otherball.vy) / (
          (1 + D * D) * (R + 1))
        delta2x = D * delta2y
        delta1y = -1 * R * delta2y
        delta1x = -1 * R * D * delta2y
      elif dx:
        # Same code as above with x and y reversed.
        D = dy / dx
        delta2x = 2 * (D * self.vy + self.vx -
                       D * otherball.vy - otherball.vx) / (
          (1 + D * D) * (R + 1))
        delta2y = D * delta2x
        delta1x = -1 * R * delta2x
        delta1y = -1 * R * D * delta2x
      else:
        delta1x = delta1y = delta2x = delta2y = 0

      self.vx += delta1x
      self.vy += delta1y
      otherball.vx += delta2x
      otherball.vy += delta2y

  def bounce_wall(self, width, height):
    left, right, top, bottom = 0.0, width, 0.0, height
    if self.x > (right - self.radius):
      self.vx = -abs(self.vx)
    elif self.x < (left + self.radius):
      self.vx = abs(self.vx)

    if self.y < (top + self.radius):
      self.vy = abs(self.vy)
    elif self.y > (bottom - self.radius):
      self.vy = -abs(self.vy)

  def repaint(self, t):
    self.bounce_wall(Display.INSTANCE.width, Display.INSTANCE.height)
    self.canvas.set_2d_size(self.w, self.h, self.x - self.radius, self.y - self.radius)
    if t == 0: #TODO this is not good but there needs to be a way to say last ball!
      opengles.glScissor(0, 0, ctypes.c_int(int(Display.INSTANCE.width)), 
                        ctypes.c_int(int(Display.INSTANCE.height)))
      #NB the screen coordinates for glScissor have origin in BOTTOM left
    else:
      opengles.glScissor(ctypes.c_int(int(self.x - self.radius - 5)),
                        ctypes.c_int(int(Display.INSTANCE.height - self.y - self.radius - 5)),
                        ctypes.c_int(int(self.w + 10)), ctypes.c_int(int(self.h + 10)))
    
    self.canvas.set_texture(self.texture)
    self.canvas.draw()
    self.x += self.vx
    self.y += self.vy
