import math

from pi3d import *
from pi3d import Utility

class Ball(object):
  def __init__(self, radius, x, y, vx=0.0, vy=0.0, decay=0.001):
    self.radius = radius
    self.x = x
    self.y = y
    self.x = x
    self.vx = vx
    self.vy = vy
    self.mass = radius * 2
    self.decay = decay

  def hit(self, otherball):
    #used for pre-checking ball positions
    dx = (self.x + self.vx) - (otherball.x + otherball.vx)
    dy = (self.y + self.vy) - (otherball.y + otherball.vy)
    rd = self.radius + otherball.radius
    return Utility.sqsum(dx, dy) <= (rd * rd)

  def collisionBounce(self,otherball):
    dx = self.x - otherball.x
    dy = self.y - otherball.y
    rd = self.radius + otherball.radius

    if Utility.sqsum(dx, dy) <= (rd * rd):
      cangle = math.atan2(dy, dx)
      mag1 = Utility.magnitude(self.vx, self.vy)
      mag2 = Utility.magnitude(otherball.vx, otherball.vy)
      dir1 = math.atan2(self.vy, self.vx)
      dir2 = math.atan2(otherball.vy, otherball.vx)
      nspx1, nspy1 = Utility.from_polar_rad(dir1 - cangle, mag1)
      nspx2, nspy2 = Utility.from_polar_rad(dir2 - cangle, mag2)
      fspx1 = (((self.mass - otherball.mass) * nspx1 +
                (otherball.mass * 2) * nspx2) / (self.mass + otherball.mass))
      fspx2 = (((self.mass * 2) * nspx1 +
                (otherball.mass - self.mass) * nspx2) /
               (self.mass + otherball.mass))
      fspy1 = nspy1
      fspy2 = nspy2
      def normal_pair(fx1, fx2):
        x1, y1 = Utility.from_polar_rad(cangle, fx1)
        x2, y2 = Utility.from_polar_rad(cangle + math.pi / 2, fx2)
        return x1 + x2, y1 + y2

      self.vx, self.vy = normal_pair(fspx1, fspy1)
      otherball.vx, otherball.vy = normal_pair(fspx2, fspy2)

