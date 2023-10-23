from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Plane(Shape):
  """ 3d model inherits from Shape, differs from Sprite in being two sided"""
  def __init__(self, camera=None, light=None, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *w*
        width
      *h*
        height
    """
    super(Plane, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating plane ...")

    self.width = w
    self.height = h

    ww = w / 2.0
    hh = h / 2.0

    verts = ((-ww, hh, 0.0), (ww, hh, 0.0), (ww, -hh, 0.0), (-ww, -hh, 0.0),
                  (-ww, hh, 0.0), (ww, hh, 0.0), (ww, -hh, 0.0), (-ww, -hh, 0.0))
    norms = ((0.0, 0.0, -1), (0.0, 0.0, -1),  (0.0, 0.0, -1), (0.0, 0.0, -1),
                  (0.0, 0.0, 1), (0.0, 0.0, 1),  (0.0, 0.0, 1), (0.0, 0.0, 1))
    texcoords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0),
                      (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))

    inds = ((3, 0, 1), (1, 2, 3), (7, 6, 5), (5, 4, 7))

    self.buf = [Buffer(self, verts, texcoords, inds, norms)]
