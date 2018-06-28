from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Lines(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self,  camera=None, light=None, vertices=[], material=(1.0,1.0,1.0),
               line_width=1, closed=False, name="", x=0.0, y=0.0, z=0.0,
               sx=1.0, sy=1.0, sz=1.0, rx=0.0, ry=0.0, rz=0.0,
               cx=0.0, cy=0.0, cz=0.0, strip=True):
    """uses standard constructor for Shape extra Keyword arguments:

      *vertices*
        array of tuples [(x0,y0,z0),(x1,y1,z1)..]
      *material*
        tuple (r,g,b)
      *line_width*
        set to 1 if absent or set to a value less than 1
      *closed*
        joins up last leg i.e. for polygons
      *strip*
        use GL_LINE_STRIP otherwise GL_LINES - needs pairs for line ends
    """
    super(Lines, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.info("Creating Lines ...")

    n_v = len(vertices)
    indices = [[a, a + 1, a + 2] for a in range(0, n_v, 3)]
    for i in range(1,3):
      last = indices[-1]
      if last[i] >= n_v:
        last[i] = n_v - 1

    self.buf = [Buffer(self, vertices, [], indices, [], smooth=False)]

    if line_width < 1:
      self.set_line_width(1, closed)
    else:
      self.set_line_width(line_width=line_width, closed=closed, strip=strip)
    self.set_material(material)

