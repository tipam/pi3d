from math import atan

from pi3d.constants import *
from pi3d.shape.Plane import Plane

# TODO: This code isn't used anywhere else.

class Missile(object):
  def __init__(self, w=1.0, h=1.0):
    self.isActive = False
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.dx = 0.0
    self.dy = 0.0
    self.dz = 0.0
    self.w = w
    self.h = h
    self.countDown = 0
    self.picture = Plane(w, h)

  #initialise the launch of the missile
  def fire(self, x, y, z, dx, dy, dz, cnt=10):
    self.isActive = True
    self.x = x
    self.y = y
    self.z = z
    self.dx = dx
    self.dy = dy
    self.dz = dz
    self.countDown = cnt
    self.picture.position(x, y, z)
    self.picture.rotateToY(atan(dx/dz))

  #move and draw
  def move(self, tex):
    if self.countDown > 0:
      self.picture.translate(self.dx, self.dy, self.dz)
      self.picture.rotateIncY(32)
      self.picture.draw(tex)
      self.countDown -= 1
