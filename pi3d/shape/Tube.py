from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.constants import *
from pi3d.Shape import Shape

class Tube(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, radius=1.0, thickness=0.5, height=2.0, sides=12, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        Radius of to mid point of wall.
      *thickness*
        of wall of tube.
      *height*
        Length of tube.
      *sides*
        Number of sides for Shape._lathe() to use.
    """
    super(Tube, self).__init__(camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating Tube ...")

    t = thickness * 0.5
    path = [(radius - t * 0.999, height * 0.5),
            (radius + t * 0.999, height * 0.5),
            (radius + t, height * 0.5),
            (radius + t, height * 0.4999),
            (radius + t, -height * 0.4999),
            (radius + t, -height * 0.5),
            (radius + t * 0.999, -height * 0.5),
            (radius - t * 0.999, -height * 0.5),
            (radius - t, -height * 0.5),
            (radius - t, -height * 0.499),
            (radius - t, height * 0.499),
            (radius - t, height * 0.5)]

    self.radius = radius
    self.thickness = thickness
    self.height = height
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self._lathe(path, sides))
