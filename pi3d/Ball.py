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
    self.mass = radius ** 2
    self.decay = decay

  def hit(self, otherball):
    #used for pre-checking ball positions
    dx = (self.x + self.vx) - (otherball.x + otherball.vx)
    dy = (self.y + self.vy) - (otherball.y + otherball.vy)
    rd = self.radius + otherball.radius
    return Utility.sqsum(dx, dy) <= (rd * rd)

  def collisionBounce(self,otherball):
    # relative positions
    dx = self.x-otherball.x
    dy = self.y-otherball.y
    rd = self.radius+otherball.radius
    # check sign of a.b to see if converging
    dotP = Utility.dotproduct(dx, dy, 0, (self.vx - otherball.vx), (self.vy - otherball.vy), 0)
    if dx**2+dy**2 <= rd**2 and dotP < 0:
      R = otherball.mass/self.mass #ratio of masses
      D = dx/dy #glancing angle for equating angular momentum before and after collision
      #three more simultaneous equations for x and y components of momentum and k.e. give:
      delta2y = 2 * (D*self.vx + self.vy - D*otherball.vx - otherball.vy)/(1 + D*D + D*D*R + R)
      delta2x = D * delta2y
      delta1y = -1 * R * delta2y
      delta1x = -1 * R * D * delta2y

      self.vx += delta1x
      self.vy += delta1y
      otherball.vx += delta2x
      otherball.vy += delta2y
