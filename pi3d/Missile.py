from pi3d.constants import *

# TODO: This code isn't used anywhere else.

class Missile(object):
  def __init__(self):
    self.isActive = False
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.dx = 0.0
    self.dy = 0.0
    self.dz = 0.0
    self.rx = 0.0
    self.ry = 0.0
    self.rz = 0.0
    self.countDown=0

  def fire(self, x, y, z, dx, dy, dz, rx, ry, rz, cnt=0):
    self.isActive = True
    self.x = x
    self.y = y
    self.z = z
    self.dx = dx
    self.dy = dy
    self.dz = dz
    self.rx = rx
    self.ry = ry
    self.rz = rz
    self.countDown = cnt

  def move(self, missile, tex, dy=0.0, dx=0.0, dz=0.0):
    if dx == 0.0:  # TODO: this next code makes no sense.
      self.x += self.dx
    else:
      self.x = dx
    if dy == 0.0:
      self.y += self.dy
    else:
      self.y = dy
    if dz == 0.0:
      self.z += self.dz
    else:
      self.z = dz

    if self.countDown > 0:
      self.countDown -= 1
      if self.countDown == 0:
        if VERBOSE:
          print "fizzle"
        self.IsActive = False
    missile.x = self.x
    missile.y = self.y
    missile.z = self.z
    missile.rotx = self.rx
    missile.roty = self.ry
    missile.rotz = self.rz

    missile.draw(tex)  # TODO: draw method not defined.
