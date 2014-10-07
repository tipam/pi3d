from pi3d.Display import Display
from numpy import dot

from pi3d.shape.Sprite import ImageSprite

class Ball(ImageSprite):
  """ This class is used to take some of the functionality of the CollisionBalls
  demo out of the main file. It inherits from the ImageSprite class that is
  passed (in addition to standard Shape constructor arguments) the Shader and
  the [Texture] to use.
  In order to fit the Display dimensions the z value has to be set to 1000
  This allows the Ball dimensions to be set in approximately pixel sizes
  """
  def __init__(self, camera=None, light=None, shader=None, texture=None,
               radius=0.0, x=0.0, y=0.0, z=1000, vx=0.0, vy=0.0, decay=0.001):
    super(Ball, self).__init__(texture=texture, shader=shader,
                              camera=camera, light=light, w=2.0*radius,
                              h=2.0*radius, name="",x=x, y=y, z=z)
    self.radius = radius
    #self.unif[0] = x
    #self.unif[1] = y
    #self.unif[2] = z
    self.vx = vx
    self.vy = vy
    self.mass = radius * radius
    self.decay = decay

  def move(self):
    self.translateX(self.vx)
    self.translateY(self.vy)

  def hit(self, otherball):
    """Used for pre-checking ball positions."""
    dx = (self.unif[0] + self.vx) - (otherball.unif[0] + otherball.vx)
    dy = (self.unif[1] + self.vy) - (otherball.unif[1] + otherball.vy)
    rd = self.radius + otherball.radius
    return dot(dx, dy) < (rd * rd)

  def bounce_collision(self, otherball):
    """work out resultant velocities using 17th.C phsyics"""
    # relative positions
    rd = self.radius + otherball.radius
    dx = self.unif[0] - otherball.unif[0]
    if abs(dx) > rd:
      return
    dy = self.unif[1] - otherball.unif[1]
    if dx * dx + dy * dy > rd * rd:
      return
    # check sign of a.b to see if converging
    dotP = dx * (self.vx - otherball.vx) + dy * (self.vy - otherball.vy)
    if dotP >= 0:
      return
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
    left, right, top, bottom = -width/2.0, width/2.0, height/2.0, -height/2.0
    if self.unif[0] > (right - self.radius):
      self.vx = -abs(self.vx)
    elif self.unif[0] < (left + self.radius):
      self.vx = abs(self.vx)

    if self.unif[1] > (top - self.radius):
      self.vy = -abs(self.vy)
    elif self.unif[1] < (bottom + self.radius):
      self.vy = abs(self.vy)

  def repaint(self, t):
    self.move()
    self.bounce_wall(Display.INSTANCE.width, Display.INSTANCE.height)
    self.draw()
