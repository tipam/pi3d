from pi3d import *
from pi3d import Texture

from pi3d.context.TextureLoader import TextureLoader

from pi3d.shape.Shape import Shape

class Extrude(Shape):
  def __init__(self, path, height=1.0, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Extrude, self).__init__(name, x, y, z, rx, ry, rz,
                                  sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print "Creating Extrude ..."

    s = len(path)
    ht = height * 0.5

    self.verts=[]
    self.norms=[]
    self.botface=[]
    self.topface=[]
    self.sidefaces=[]
    self.tex_coords=[]
    self.edges = s
    self.ttype = GL_TRIANGLES

    minx = path[0][0]
    maxx = path[0][0]
    miny = path[0][1]
    maxy = path[0][1]

    #find min/max values for texture coords
    for p in range(0, s):
      px = path[p][0]
      pz = path[p][1]
      minx = min(minx, px)
      minz = min(miny, pz)
      maxx = max(maxx, px)
      maxz = max(maxy, pz)

    tx = 1.0 / (maxx - minx)
    tz = 1.0 / (maxy - minz)

    #vertices for sides
    for p in range(s):
      px = path[p][0]
      pz = path[p][1]
      dx = path[(p+1)%s][0] - px
      dz = path[(p+1)%s][1] - pz
      #TODO normalize these vector components, not needed for shadows
      for i in (-1, 1):
        self.verts.append(px)
        self.verts.append(i*ht)
        self.verts.append(pz)

        self.norms.append(-dz)
        self.norms.append(0.0)
        self.norms.append(dx)

        self.tex_coords.append(1.0*p/s)
        self.tex_coords.append(i*0.5)

    #vertices for edges of top and bottom, bottom first (n=2s to 3s-1) then top (3s to 4s-1)
    for i in (-1, 1):
      for p in range(s):
        px = path[p][0]
        pz = path[p][1]
        self.verts.append(px)
        self.verts.append(i*ht)
        self.verts.append(pz)

        self.norms.append(0.0)
        self.norms.append(i)
        self.norms.append(0.0)

        self.tex_coords.append((px - minx) * tx)
        self.tex_coords.append((pz - minz) * tz)

    #top and bottom face mid points verts number 4*s and 4*s+1 (bottom and top respectively)
    for i in (-1, 1):
      self.verts.append((minx+maxx)/2)
      self.verts.append(i*ht)
      self.verts.append((minz+maxz)/2)

      self.norms.append(0)
      self.norms.append(i)
      self.norms.append(0)

      self.tex_coords.append(0.5)
      self.tex_coords.append(0.5)


    for p in range(s):    #sides - triangle strip
      v1, v2, v3, v4 = 2*p, 2*p+1, (2*p+2)%(2*s), (2*p+3)%(2*s)
      self.sidefaces.append(v1)
      self.sidefaces.append(v3)
      self.sidefaces.append(v2)

      self.sidefaces.append(v2)
      self.sidefaces.append(v4)
      self.sidefaces.append(v3)

    for p in range(s):    #bottom face indices - triangle fan
      p0 = 4*s #middle vertex
      p1 = 2*s
      self.botface.append(p0)
      self.botface.append(p1 + (p+1)%s)
      self.botface.append(p1 + p)

    for p in range(s):    #top face indices - triangle fan
      p0 = 4*s+1 #middle vertex
      p1 = 3*s
      self.topface.append(p0)
      self.topface.append(p1 + p)
      self.topface.append(p1 + (p+1)%s)

    self.verts = c_floats(self.verts)
    self.norms = c_floats(self.norms)
    self.tex_coords = c_floats(self.tex_coords)
    self.topface = c_shorts(self.topface)
    self.botface = c_shorts(self.botface)
    self.sidefaces = c_shorts(self.sidefaces)


  def draw(self, tex1 = None, tex2 = None, tex3 = None):
    # TODO: shadows Shape.draw
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.verts)
    opengles.glNormalPointer(GL_FLOAT, 0, self.norms)
    mtrx =(ctypes.c_float * 16)()
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
    self.transform()

    with TextureLoader(tex1, self.tex_coords):
      opengles.glDrawElements(GL_TRIANGLE_STRIP, self.edges * 6,
                              GL_UNSIGNED_SHORT, self.sidefaces)
      with TextureLoader(tex2, self.tex_coords):
        opengles.glDrawElements(GL_TRIANGLE_FAN, self.edges * 3,
                                GL_UNSIGNED_SHORT, self.topface)
        with TextureLoader(tex3, self.tex_coords):
          opengles.glDrawElements(GL_TRIANGLE_FAN, self.edges * 3,
                                  GL_UNSIGNED_SHORT, self.botface)

    opengles.glLoadMatrixf(mtrx)
