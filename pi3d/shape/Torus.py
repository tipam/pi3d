import math

from pi3d import *
from pi3d.util import Utility
from pi3d.shape.Shape import Shape

class Torus(Shape):
  def __init__(self, camera, light, radius=2.0, thickness=0.5, ringrots=6, sides=12, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    super(Torus,self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                               sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print "Creating Torus ..."

    path = []
    st = (math.pi * 2)/ringrots
    for r in range(ringrots + 1):
      x, y = Utility.from_polar_rad(r * st, thickness)
      path.append((radius + y, x))  # TODO: why the reversal?

    self.radius = radius
    self.thickness = thickness
    self.ringrots = ringrots
    self.sides = sides
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self.lathe(path))
