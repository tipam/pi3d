from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Points(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self,  camera=None, light=None, vertices=[], material=(1.0,1.0,1.0),
               point_size = 1, name="", x=0.0, y=0.0, z=0.0, sx=1.0, sy=1.0, sz=1.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, normals=[], tex_coords=[]):
    """uses standard constructor for Shape extra Keyword arguments:

      *vertices*
        array of tuples [(x0,y0,z0),(x1,y1,z1)..]
      *material*
        tuple (r,g,b)
      *point_size*
        set to 1 if absent or set to a value less than 1
    """
    super(Points, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating Points ...")

    n_v = len(vertices)
    indices = [[a, a + 1, a + 2] for a in range(0, n_v, 3)]
    for i in range(1,3):
      last = indices[-1]
      if last[i] >= n_v:
        last[i] = n_v - 1
    if len(normals) == 0 and len(tex_coords) == 0:
      normals = [[0.0, 0.0, 0.0] for i in range(n_v)] #used for rgb in mat_pointsprite
      tex_coords = [[1.0, 0.0] for i in range(n_v)] # [:,0] used for alpha in mat_pointsprite
    self.buf = [Buffer(self, vertices, tex_coords, indices, normals, smooth=False)]

    if point_size < 1:
      self.set_point_size(1)
    else:
      self.set_point_size(point_size)
    self.set_material(material)

