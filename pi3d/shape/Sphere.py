from __future__ import absolute_import, division, print_function, unicode_literals

import math

from pi3d.constants import *
from pi3d.util import Utility
from pi3d.Shape import Shape

class Sphere(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None,
               radius=1, slices=12, sides=12, hemi=0.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        radius of sphere
      *slices*
        number of latitude edges
      *hemi*
        if set to 0.5 it will only construct the top half of sphere
      *sides*
        number of sides for Shape._lathe() to use
    """
    super(Sphere, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating sphere ...")

    path = []
    st = (math.pi * (1.0 - hemi)) / slices
    for r in range(slices + 1):
      x, y = Utility.from_polar_rad(r * st, radius)
      path.append((y, x))  # TODO: why is the reversal here?

    self.radius = radius
    self.slices = slices
    self.hemi = hemi
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self._lathe(path, sides))
