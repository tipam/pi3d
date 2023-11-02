from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Slice(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, inner=0.5, outer=1, sides=12, name="",
               start=0.0, end=60, x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """Slice with outer and inner radius. NB this is in the xy plane rather than the
    xz plane that Disk produces and is only one sided. It uses standard constructor
    for Shape extra with the following Keyword arguments:

      *inner*
        Inner radius of slice.
      *outer*
        Outer radius.
      *sides*
        Number of sides on outside and inside of polygon.
      *start*
        Angle in degrees clockwise from vertical up, to start slice.
      *end*
        Angle to end slice.
    """
    super(Slice, self).__init__(camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz,
                               cx, cy, cz)

    LOGGER.debug("Creating slice ...")

    self.inner = inner
    self.outer = outer
    self.start = start
    self.end = end
    self.n = sides + 1
    (verts, texcoords) = self.make_verts()
    norms = np.zeros_like(verts)
    norms[:,2] = -1.0
    inds = np.array([[2 * i + u, 2 * i + v, 2 * i + w] for i in range(0, sides)
                                    for (u, v, w) in [(0, 1, 3), (3, 2, 0)]], dtype=int)
    verts[:,2] = z
    self.buf = [Buffer(self, verts, texcoords, inds, norms)]

  def make_verts(self):
    angles = np.deg2rad(np.linspace(self.start, self.end, self.n))
    s = np.sin(angles)
    c = np.cos(angles)
    verts = np.zeros((2 * self.n, 3))
    verts[::2, 0] = s * self.inner
    verts[1::2, 0] = s * self.outer
    verts[::2, 1] = c * self.inner
    verts[1::2, 1] = c * self.outer
    texcoords = (verts[:,:2] / (2 * self.outer)) * [1, -1] + 0.5
    return (verts, texcoords)

  def reset_verts(self, inner=None, outer=None, start=None, end=None):
    if inner is not None:
      self.inner = inner
    if outer is not None:
      self.outer = outer
    if start is not None:
      self.start = start
    if end is not None:
      self.end = end
    (verts, texcoords) = self.make_verts()
    buf = self.buf[0]
    buf.array_buffer[:,0:3] = verts
    buf.array_buffer[:,6:8] = texcoords
    buf.re_init()