from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.constants import *
from pi3d.Shape import Shape

class TCone(Shape):
  """ 3d model inherits from Shape, creates truncated cone axis y direction"""
  def __init__(self, camera=None, light=None,
               radiusBot=1.2, radiusTop=0.8, height=2.0, sides=12,
               name="", x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radiusBot*
        Radius of the bottom.
      *radiusTop*
        Radius at the top.
      *height*
        Height.
      *sides*
        Number of sides to divide edges of polygons.
    """
    super(TCone, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating Truncated Cone ...")

    path = [(0, height * 0.5),
            (radiusTop * 0.999, height * 0.5),
            (radiusTop, height * 0.5),
            (radiusTop, height * 0.499),
            (radiusBot, -height * 0.499),
            (radiusBot, -height * 0.5),
            (radiusBot * 0.999, -height * 0.5),
            (0, -height * 0.5)]

    self.radiusBot = radiusBot
    self.radiusTop = radiusTop
    self.height = height
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self._lathe(path, sides))
