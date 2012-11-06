from pi3d.pi3dCommon import *
from pi3d import Constants

class Disk(Shape):
  def __init__(self,radius=1,sides=12,name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
    super(Disk, self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

    print "Creating disk ..."

    self.verts=[]
    self.norms=[]
    self.inds=[]
    self.texcoords=[]
    self.ttype = GL_TRIANGLES
    self.sides = sides


    st = math.pi/slices
    addVertex(self.verts,x,y,z,self.norms,0,1,0,self.texcoords,0.5,0.5)
    for r in range(0,sides+1):
      ca=math.sin(r*st)
      sa=math.cos(r*st)
      addVertex(self.verts, x + radius * ca, y, z + radius * sa,
                self.norms, 0, 1, 0,
                self.texcoords, ca * 0.5 + 0.5, sa * 0.5 + 0.5)

    for r in range(0,sides):
      addTri(self.inds,0,r+1,r+2)

    self.vertices = eglfloats(self.verts);
    self.indices = eglshorts(self.inds);
    self.normals = eglfloats(self.norms);
    self.tex_coords = eglfloats(self.texcoords);
    self.ssize = sides * 3

  def draw(self,tex=None):
    shape_draw(self,tex)

