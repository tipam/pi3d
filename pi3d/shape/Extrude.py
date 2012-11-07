from pi3d import *
from pi3d import Texture

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
      py = path[p][1]
      minx = min(minx, px)
      miny = min(miny, py)
      maxx = max(maxx, px)
      maxy = max(maxy, py)

    tx = 1.0 / (maxx - minx)
    ty = 1.0 / (maxy - miny)

    for p in range (0, s):
      px = path[p][0]
      py = path[p][1]
      self.verts.append(px)
      self.verts.append(py)
      self.verts.append(-ht)
      self.norms.append(0.0)
      self.norms.append(0.0)
      self.norms.append(-1.0)
      self.tex_coords.append((px - minx) * tx)
      self.tex_coords.append((py - miny) * ty)

      for p in range (0, s):
        px = path[p][0]
        py = path[p][1]
        self.verts.append(px)
        self.verts.append(py)
        self.verts.append(ht)
        self.norms.append(0.0)
        self.norms.append(0.0)
        self.norms.append(1.0)
        self.tex_coords.append((px - minx) * tx)
        self.tex_coords.append((py - miny) * ty)

    for p in range(s):    #top face indices - triangle fan
      self.topface.append(p)

    for p in range(s):    #bottom face indices - triangle fan
        b = s + (s - p)
        if VERBOSE:
          print "bi:",b
        self.botface.append(b - 1)

    for p in range (0, s):    #sides - triangle strip
      self.sidefaces.append(p)
      self.sidefaces.append(p + s)
    self.sidefaces.append(0)
    self.sidefaces.append(s)

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

    with Texture.Loader(tex1, self.tex_coords):
      opengles.glDrawElements(GL_TRIANGLE_STRIP, self.edges * 2 + 2,
                              GL_UNSIGNED_SHORT, self.sidefaces)
      with Texture.Loader(tex2, self.tex_coords):
        opengles.glDrawElements(GL_TRIANGLE_FAN, self.edges,
                                GL_UNSIGNED_SHORT, self.topface)
        with Texture.Loader(tex3, self.tex_coords):
          opengles.glDrawElements(GL_TRIANGLE_FAN, self.edges,
                                  GL_UNSIGNED_SHORT, self.botface)

    opengles.glLoadMatrixf(mtrx)
