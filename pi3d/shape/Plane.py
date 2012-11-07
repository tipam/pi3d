from pi3d import *
from pi3d import Texture
from pi3d.shape.Shape import Shape

class Plane(Shape):
  def __init__(self, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Plane, self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print "Creating plane ..."

    self.width = w
    self.height = h
    self.ttype = GL_TRIANGLES
    self.verts = []
    self.norms = []
    self.texcoords = []
    self.inds = []

    ww = w / 2.0
    hh = h / 2.0

    self.add_vertex(-ww + x, hh + y, z, 0, 0, 1, 0.0, 0.0)
    self.add_vertex(ww + x, hh + y, z, 0, 0, 1, 1.0, 0.0)
    self.add_vertex(ww + x, -hh + y, z, 0, 0, 1, 1.0, 1.0)
    self.add_vertex(-ww + x,-hh + y, z, 0, 0, 1, 0.0 ,1.0)
    self.add_tri(1, 0, 3)
    self.add_tri(1, 3, 2)
    # plane data - this could be stored locally so that vertices / tex coords an
    # be altered in real-time

    self.vertices = c_floats(self.verts)
    self.indices = c_shorts(self.inds)
    self.normals = c_floats(self.norms)
    self.tex_coords = c_floats(self.texcoords)

  def draw(self, tex=0):
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.vertices);
    opengles.glNormalPointer(GL_FLOAT, 0, self.normals);
    with Texture.Loader(tex, self.tex_coords):
      self.transform()
      opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, self.indices)

