import math

from pi3d import Display
from pi3d.Texture import Texture
from pi3d.util import Draw
from pi3d.util import Utility

from pi3d.shape.Sprite import Sprite

class Ball(Sprite):
  def __init__(self, camera, light, shader, texture, radius, x, y, vx=0.0, vy=0.0, decay=0.001):
    super(Ball, self).__init__(camera, light, 2*radius, 2*radius, "", x, y, 450)
    if not isinstance(texture, Texture):
      texture = Texture(texture)
    self.buf[0].set_draw_details(shader, [texture], 0.0, -1.0)
    self.radius = radius
    self.unif[0] = x
    self.unif[1] = y
    self.vx = vx
    self.vy = vy
    self.mass = radius * radius
    self.decay = decay

  def _load_opengl(self):
    self.buf[0].textures[0].load_opengl()

  def move(self):
    self.unif[0] += self.vx
    self.unif[1] += self.vy

  def hit(self, otherball):
    # Used for pre-checking ball positions.
    dx = (self.unif[0] + self.vx) - (otherball.unif[0] + otherball.vx)
    dy = (self.unif[1] + self.vy) - (otherball.unif[1] + otherball.vy)
    rd = self.radius + otherball.radius
    return Utility.sqsum(dx, dy) <= (rd * rd)

  def bounce_collision(self, otherball):
    # relative positions
    dx = self.unif[0] - otherball.unif[0]
    dy = self.unif[1] - otherball.unif[1]
    rd = self.radius + otherball.radius
    # check sign of a.b to see if converging
    dotP = Utility.dotproduct(dx, dy, 0,
                              (self.vx - otherball.vx),
                              (self.vy - otherball.vy), 0)
    if dx * dx + dy * dy <= rd * rd and dotP < 0:
      R = otherball.mass / self.mass #ratio of masses
      # Glancing angle for equating angular momentum before and after collision.
      # Three more simultaneous equations for x and y components of momentum and
      # kinetic energy give:

      if dy:
        D = dx / dy
        delta2y = 2 * (D * self.vx + self.vy - D * otherball.vx - otherball.vy) / (
          (1 + D * D) * (R + 1))
        delta2x = D * delta2y
        delta1y = -1 * R * delta2y
        delta1x = -1 * R * D * delta2y
      elif dx:
        # Same code as above with x and y reversed.
        D = dy / dx
        delta2x = 2 * (D * self.vy + self.vx - D * otherball.vy - otherball.vx) / (
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
    self.bounce_wall(Display.DISPLAY.max_width, Display.DISPLAY.max_height)
    #self.draw(self.shader, [self.texture], 0.0 -1.0)
    self.draw()
    #Draw.sprite(self.texture, self.x, self.y, -1, self.radius, self.radius)
