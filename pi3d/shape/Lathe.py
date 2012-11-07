from pi3d import *
from pi3d.shape.Shape import Shape

class Lathe(Shape):
  def __init__(self,path, sides=12, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Lathe, self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print "Creating lathe ..."

    self.path = path
    self.sides = sides
    self.ttype = GL_TRIANGLES

    results = self.lathe(path)

    self.vertices = c_floats(results[0])
    self.normals = c_floats(results[1])
    self.indices = c_shorts(results[2])
    self.tex_coords = c_floats(results[3])
    self.ssize = results[4]

  def draw(self, tex=None, shl=GL_UNSIGNED_SHORT):
    opengles.glDisable(GL_CULL_FACE)
    super(Lathe, self).draw(tex, shl)
    opengles.glEnable(GL_CULL_FACE)

