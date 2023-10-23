from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Shape import Shape
from pi3d.Buffer import Buffer
import logging
import math

LOGGER = logging.getLogger(__name__)

class Tube(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, radius=1.0, thickness=0.5, height=2.0, sides=12, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0, use_lathe=True):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        Radius of to mid point of wall.
      *thickness*
        of wall of tube.
      *height*
        Length of tube.
      *sides*
        Number of sides for Shape._lathe() to use.
      *use_lathe*
        Default to using Shape._lathe() for backwards compatibility but
        actually better to set this false, especially for washer like tubes.
    """
    super(Tube, self).__init__(camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating Tube ...")

    if use_lathe:
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

      self.buf = [self._lathe(path, sides)]
    else:
      step = math.pi * 2.0 / sides
      otr = radius + thickness * 0.5
      inr = radius - thickness * 0.5
      ht = height * 0.5
      verts = []
      norms = []
      uvs = []
      faces = []

      normdirs = ((0, 1), (1, 0), (0, -1), (-1, 0)) # up, out, down, in
      for i in range(sides + 1):
        for j, (xz, y) in enumerate(((inr, ht), (otr, ht), # up
                         (otr, ht), (otr, -ht), # out
                         (otr, -ht), (inr, -ht), # down
                         (inr, -ht), (inr, ht))): # in
          s = math.sin(i * step)
          c = math.cos(i * step)
          verts += [(xz * s, y, xz * c)]
          n = normdirs[j // 2]
          norms += [(n[0] * s, n[1], n[0] * c)]
          if n[0] == 0: # top or bottom
            uvs += [(0.5 * (1.0 + verts[-1][0] / otr), 0.5 * (1.0 + verts[-1][2] / otr))]
          else:
            uvs += [(i / sides, 0.5 * (1.0 + y / ht))]
        if i < (sides):
          for a, b, c in ((0, 1, 8), (1, 9, 8), (2, 3, 10), (3, 11, 10),
                          (4, 5, 12), (12, 5, 13), (6, 7, 14) , (7, 15, 14)):
            f_off = i * 8
            faces += [(a + f_off, b + f_off, c + f_off)]

      self.buf = [Buffer(self, verts, uvs, faces, norms)]
