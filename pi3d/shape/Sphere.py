import math

from pi3d.pi3dCommon import *
from pi3d import Constants
from pi3d.shape.Shape import Shape

class Sphere(Shape):
  def __init__(self, radius=1, slices=12, sides=12, hemi=0.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    super(Sphere,self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if Constants.VERBOSE:
      print "Creating sphere ..."

    path = []
    st = (math.pi * (1.0 - hemi)) / slices
    for r in range(0,slices+1):
        path.append((radius * math.sin(r * st),
                     radius * math.cos(r * st)))

    self.radius = radius
    self.slices = slices
    self.sides = sides
    self.hemi = hemi
    self.ttype = GL_TRIANGLES

    results = lathe(path, sides, True)

    self.vertices = c_floats(results[0])
    self.normals = c_floats(results[1])
    self.indices = c_shorts(results[2])
    self.tex_coords = c_floats(results[3])
    self.ssize = results[4]

  def draw(self,tex=None):
    shape_draw(self,tex)

