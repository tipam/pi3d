from pi3d.pi3dCommon import *
from pi3d import Constants
from pi3d.shape.Shape import Shape

class Plane(Shape):
  def __init__(self, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Plane, self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    if Constants.VERBOSE:
      print "Creating plane ..."

    self.width = w
    self.height = h
    self.ttype = GL_TRIANGLES
    self.vertices = []
    self.normals = []
    self.tex_coords = []
    self.indices = []
    ww = w / 2.0
    hh = h / 2.0

    addVertex(self.vertices, -ww + x, hh + y, z,
              self.normals, 0, 0, 1, self.tex_coords, 0.0, 0.0)
    addVertex(self.vertices, ww + x, hh + y, z,
              self.normals, 0, 0, 1, self.tex_coords, 1.0, 0.0)
    addVertex(self.vertices, ww + x, -hh + y, z,
              self.normals, 0, 0, 1, self.tex_coords, 1.0, 1.0)
    addVertex(self.vertices, -ww + x,-hh + y, z,
              self.normals, 0, 0, 1, self.tex_coords, 0.0 ,1.0)
    addTri(self.indices, 1, 0, 3)
    addTri(self.indices, 1, 3, 2)
    # plane data - this could be stored locally so that vertices / tex coords an
    # be altered in real-time

    self.verts = eglfloats(self.vertices);
    self.inds = eglshorts(self.indices);
    self.norms = eglfloats(self.normals);
    self.texcoords = eglfloats(self.tex_coords);

  def draw(self, tex=0):
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.verts);
    opengles.glNormalPointer(GL_FLOAT, 0, self.norms);
    if tex > 0:
      texture_on(tex, self.texcoords, GL_FLOAT)
    transform(self.x, self.y, self.z, self.rotx, self.roty, self.rotz,
              self.sx, self.sy, 1.0, self.cx, self.cy, self.cz)
    opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, self.inds)
    if tex > 0:
      texture_off()


