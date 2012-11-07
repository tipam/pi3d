from pi3d import *
from pi3d import Utility
from pi3d.shape.Shape import Shape

class Disk(Shape):
  def __init__(self, radius=1, sides=12, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Disk, self).__init__(name, x, y, z, rx, ry, rz, sx, sy, sz,
                               cx, cy, cz)

    if VERBOSE:
      print "Creating disk ..."

    self.verts = []
    self.norms = []
    self.inds = []
    self.texcoords = []
    self.ttype = GL_TRIANGLES
    self.sides = sides

    st = math.pi / slices
    self.add_vertex(x, y, z, 0, 1, 0, 0.5, 0.5)
    for r in range(sides+1):
      ca, sa = Utility.from_polar_rad(r * st)
      self.add_vertex(x + radius * sa, y, z + radius * ca,
                      0, 1, 0, sa * 0.5 + 0.5, ca * 0.5 + 0.5)
      # TODO: why the reversal?

    for r in range(sides):
      self.add_tri(0, r + 1, r + 2)

    self.vertices = c_floats(self.verts);
    self.indices = c_shorts(self.inds);
    self.normals = c_floats(self.norms);
    self.tex_coords = c_floats(self.texcoords);
    self.ssize = sides * 3

