from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.util import Utility
from pi3d.Shape import Shape
import logging
import math
import numpy as np

LOGGER = logging.getLogger(__name__)

def is_in_triangle(p, p0, p1, p2):
  ''' is p inside the triangle formed by p0, p1, p2 '''
  p1 = [p1[0] - p0[0], p1[1] - p0[1]]
  p2 = [p2[0] - p0[0], p2[1] - p0[1]]
  den = p1[0] * p2[1] - p1[1] * p2[0]
  a = (p[0] * p2[1] - p[1] * p2[0] - p0[0] * p2[1] + p0[1] * p2[0]) / den if den != 0.0 else 0.0
  if a <= 0:
    return False
  b = -(p[0] * p1[1] - p[1] * p1[0] - p0[0] * p1[1] + p0[1] * p1[0]) / den if den != 0.0 else 0.0
  if b <= 0 or (a + b) >= 1:
    return False
  return True


def is_convex(p, prior, post, return_angle=False):
  '''checks if this corner is convex (turns right for a clockwise polygon or left for an anticlockwise
  polygon, arguments are two tuples for this vertex and the one before and after. Can return the
  angle turned'''
  p0 = [p[0] - prior[0], p[1] - prior[1]] # vector from prior to p
  p1 = [post[0] - p[0], post[1] - p[1]] # vector from p to post
  cross = p0[0] * p1[1] - p0[1] * p1[0]
  convex = 1
  if cross < 0:
    convex = -1
  if return_angle:
    dot = p0[0] * p1[0] + p0[1] * p1[1]
    angle = math.atan2(cross, dot)
    return convex, angle
  return convex, None

class Polygon(Shape):
  """ 3d model inherits from Shape. N.B. There is no check that lines do not cross."""
  def __init__(self, camera=None, light=None, path=[], horizontal=False, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *path*
        list of (x,y) values
      *horizontal*
        default False. If set to True then y values of path will be
        used as z values so the polygon is horizontal.

    """
    super(Polygon, self).__init__(camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz,
                               cx, cy, cz)

    LOGGER.debug("Creating disk ...")

    path = list(path) # in case fed a tuple rather than a list
    verts = np.zeros((len(path), 3))
    verts[:,0:2] = path
    maxv = verts[:,0:2].max(axis=0)
    minv = verts[:,0:2].min(axis=0)
    texcoords = (verts[:,0:2] - minv) / (maxv - minv)
    norms = np.ones((len(path), 3)) * [0.0, 0.0, -1.0]
    if horizontal:
      verts[:,[1,2]] = verts[:,[2,1]] #TODO flip z values?
      norms[:,[1,2]] = norms[:,[2,1]] #TODO flip?
    inds = []

    n = len(verts)
    cumangle = 0.0
    cw = 1 # i.e. clockwise is true
    for i in range(n):
      conv, angle = is_convex(verts[i], verts[i-1], verts[(i+1)%n], True)
      cumangle += angle
    if cumangle > 0:
      cw = -1 # clockwise false

    ## NB TODO this doesn't yet check for lines crossing
    vlist = list(range(n))
    i = 0
    while n > 3:
      conv, _ = is_convex(path[i], path[i-1], path[(i+1)%n])
      conv *= cw
      if conv < 0: # this is an ear so test if it includes another point
        abort = False
        for ix in range(n - 3):
          ixwrap = (i + 2 + ix) % n
          if is_in_triangle(path[ixwrap], path[i], path[i-1], path[(i+1)%n]):
            abort = True
            break
        if not abort:
          inds.append((vlist[i], vlist[(i+cw)%n], vlist[(i-cw)%n]))
          path.pop(i)
          vlist.pop(i)
          n -= 1
      i = 0 if i >= (n - 1) else i + 1

    inds.append((vlist[1-cw], vlist[1], vlist[1+cw]))

    self.buf = [Buffer(self, verts, texcoords, inds, norms)]
