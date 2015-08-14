from __future__ import absolute_import, division, print_function, unicode_literals

import math

from pi3d.constants import *
from pi3d.util import Utility
from pi3d.Shape import Shape

class Torus(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, radius=2.0, thickness=0.5, ringrots=6, sides=12, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        Major radius of torus
      *thickness*
        Minor radius, section through one side of torus
      *ringrots*
        Sides around minor radius circle
      *sides*
        Number of sides for Shape._lathe() to use
    """
    super(Torus,self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                               sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating Torus ...")

    #path = []
    st = (math.pi * 2)/ringrots
    #for r in range(ringrots + 1):
    #  x, y = Utility.from_polar_rad(r * st, thickness)
    #  path.append((radius + y, x))  # TODO: why the reversal?
    path = [(radius - thickness * math.cos(i * st),
             thickness * math.sin(i * st)) for i in range(ringrots + 1)]

    self.radius = radius
    self.thickness = thickness
    self.ringrots = ringrots
    self.ttype = GL_TRIANGLES

    self.buf = []
    self.buf.append(self._lathe(path, sides))
