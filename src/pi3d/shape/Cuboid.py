from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Cuboid(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self,  camera=None, light=None, w=1.0, h=1.0, d=1.0,
               name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, tw=1.0, th=1.0, td=1.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *w*
        width
      *h*
        height
      *d*
        depth
      *tw*
        scale width
      *th*
        scale height
      *td*
        scale depth

    The scale factors are the multiple of the texture to show along that
    dimension. For no distortion of the image the scale factors need to be
    proportional to the relative dimension.
    """
    super(Cuboid, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)

    LOGGER.debug("Creating cuboid ...")

    self.width = w
    self.height = h
    self.depth = d
    self.ssize = 36

    ww = w / 2.0
    hh = h / 2.0
    dd = d / 2.0

    #cuboid data - faces are separated out for texturing..

    self.vertices = ((-ww, hh, dd), (ww, hh, dd), (ww, -hh, dd), (-ww, -hh, dd),
        (ww, hh, dd),  (ww, hh, -dd),  (ww, -hh, -dd), (ww, -hh, dd),
        (-ww, hh, dd), (-ww, hh, -dd), (ww, hh, -dd),  (ww, hh, dd),
        (ww, -hh, dd), (ww, -hh, -dd), (-ww, -hh, -dd),(-ww, -hh, dd),
        (-ww, -hh, dd),(-ww, -hh, -dd),(-ww, hh, -dd), (-ww, hh, dd),
        (-ww, hh, -dd),(ww, hh, -dd),  (ww, -hh, -dd), (-ww,-hh,-dd))
    self.normals = ((0.0, 0.0, 1),    (0.0, 0.0, 1),   (0.0, 0.0, 1),  (0.0, 0.0, 1),
        (1, 0.0, 0),  (1, 0.0, 0),    (1, 0.0, 0),     (1, 0.0, 0),
        (0.0, 1, 0),  (0.0, 1, 0),    (0.0, 1, 0),     (0.0, 1, 0),
        (0.0, -1, 0), (0,- 1, 0),     (0.0, -1, 0),    (0.0, -1, 0),
        (-1, 0.0, 0),  (-1, 0.0, 0),  (-1, 0.0, 0),    (-1, 0.0, 0),
        (0.0, 0.0, -1),(0.0, 0.0, -1),(0.0, 0.0, -1),  (0.0, 0.0, -1))

    self.indices = ((1, 0, 3), (3, 2, 1), (5, 4, 7),  (7, 6, 5),
        (9, 8, 11),  (11, 10, 9), (14, 13, 12), (12, 15, 14),
        (17, 16, 19),(19, 18, 17),(20, 21, 22), (22, 23, 20))

    #texture scales (each set to 1 would stretch it over face)
    tw = tw / 2.0
    th = th / 2.0
    td = td / 2.0

    self.tex_coords = ((0.5+tw, 0.5-th),        (0.5-tw, 0.5-th),        (0.5-tw, 0.5+th),        (0.5+tw, 0.5+th), #tw x th
        (0.5+td, 0.5-th),        (0.5-td, 0.5-th),        (0.5-td, 0.5+th),        (0.5+td, 0.5+th), # td x th
        (0.5-tw, 0.5-th),        (0.5+tw, 0.5-th),        (0.5+tw, 0.5+th),        (0.5-tw, 0.5+th), # tw x th
        (0.5+tw, 0.5+td),        (0.5-tw, 0.5+td),        (0.5-tw, 0.5-td),        (0.5+tw, 0.5-td), # tw x td
        (0.5-td, 0.5+th),        (0.5+td, 0.5+th),        (0.5+td, 0.5-th),        (0.5-td, 0.5-th), # td x th
        (0.5-tw, 0.5-th),        (0.5+tw, 0.5-th),        (0.5+tw, 0.5+th),        (0.5-tw, 0.5+th)) # tw x th

    self.buf = []
    self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))

