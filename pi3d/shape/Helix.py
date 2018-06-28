from __future__ import absolute_import, division, print_function, unicode_literals

import math

from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Helix(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self, camera=None, light=None, radius=1.0, thickness=0.2, ringrots=6, sides=12, rise=1.0,
               loops=2.0, name="", x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *radius*
        Radius of helix.
      *thickness*
        Radius of 'bar' being 'bent' to form the helical shape.
      *ringrots*
        Number of sides for the circlular secon of the 'bar'.
      *sides*
        Number of sides for Shape._lathe() to use.
      *rise*
        Distance between 'threads'.
      *loops*
        Number of turns that the helix makes.
    """
    super(Helix, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.info("Creating Helix r{}, t{}, rr{}, s{}".format(radius, thickness, ringrots, sides))

    path = []
    st = (math.pi * 2) / ringrots
    hr = rise * 0.5
    for r in range(ringrots + 1):
      path.append((radius + thickness * math.sin(r * st),
                   thickness * math.cos(r * st) - hr))
      LOGGER.info("path: {} {}".format(path[r][0], path[r][1]))

    self.radius = radius
    self.thickness = thickness
    self.ringrots = ringrots
 
    self.buf = [self._lathe(path, sides, rise=rise, loops=loops)]
