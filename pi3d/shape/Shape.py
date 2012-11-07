import math

from pi3d import *
from pi3d import Texture
from pi3d import Utility

class Shape(object):
  def __init__(self, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz):
    self.name = name
    self.x = x                #position
    self.y = y
    self.z = z
    self.rotx = rx                #rotation
    self.roty = ry
    self.rotz = rz
    self.sx = sx                #scale
    self.sy = sy
    self.sz = sz
    self.cx = cx                #center
    self.cy = cy
    self.cz = cz

        #this should all be done with matrices!! ... just for testing ...

  def draw(self, tex=None, shl=GL_UNSIGNED_SHORT):
    opengles.glShadeModel(GL_SMOOTH)
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.vertices)
    opengles.glNormalPointer(GL_FLOAT, 0, self.normals)
    with Texture.Loader(tex, self.tex_coords):
      mtrx = (c_float * 16)()
      opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
      self.transform()
      opengles.glDrawElements( self.ttype, self.ssize, shl , self.indices)
      opengles.glLoadMatrixf(mtrx)

  def scale(self, sx, sy, sz):
    self.sx = sx
    self.sy = sy
    self.sz = sz

  def position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def translate(self, dx, dy, dz):
    self.x = self.x + dx
    self.y = self.y + dy
    self.z = self.z + dz

  def rotateToX(self, v):
    self.rotx = v

  def rotateToY(self, v):
    self.roty = v

  def rotateToZ(self, v):
    self.rotz = v

  def rotateIncX(self,v):
    self.rotx += v

  def rotateIncY(self,v):
    self.roty += v

  def rotateIncZ(self,v):
    self.rotz += v

  # TODO: should be a method on Shape.
  def add_vertex(self, x, y, z, nx, ny, nz, tx, ty):
  # add vertex,normal and tex_coords ...
    self.verts.extend([x, y, z])
    self.norms.extend([nx, ny, nz])
    self.texcoords.extend([tx, ty])

  # TODO: should be a method on Shape.
  def add_tri(self, x, y, z):
  # add triangle refs.
    self.inds.extend([x, y, z])

  # position, rotate and scale an object
  def transform(self):
    Utility.translatef(self.x - self.cx, self.y - self.cy, self.z - self.cz)

    # TODO: why the reverse order?
    Utility.rotatef(self.rotz, 0, 0, 1)
    Utility.rotatef(self.roty, 0, 1, 0)
    Utility.rotatef(self.rotx, 1, 0, 0)
    Utility.scalef(self.sx, self.sy, self.sz)
    Utility.translatef(self.cx, self.cy, self.cz)

  def lathe(self, path, rise=0.0, loops=1.0, tris=True):
    s = len(path)
    rl = int(self.sides * loops)
    if tris:
      ssize = rl * 6 * (s - 1)
    else:
      ssize = rl * 2 * (s - 1) + (s * 2) - 2

    pn = 0
    pp = 0
    tcx = 1.0 / self.sides
    pr = (math.pi / self.sides) * 2
    rdiv = rise / rl
    ss = 0

    # Find largest and smallest y of the path used for stretching the texture over
    p = [i[1] for i in path]
    miny = min(*p)
    maxy = max(*p)

    verts = []
    norms = []
    idx = []
    tex_coords = []

    opx = path[0][0]
    opy = path[0][1]

    for p in range(s):
      px = path[p][0]
      py = path[p][1]

      tcy = 1.0 - ((py - miny) / (maxy - miny))

      #normal between path points
      dx, dy = normalize_vector((opx, opy), (px, py))

      for r in range (0, rl):
        cosr, sinr = Utility.from_polar_rad(pr * r)
        # TODO: why the reversal?

        verts.extend([px * sinr, py, px * cosr])
        norms.extend([-sinr * dy, dx, -cosr * dy])
        tex_coords.extend([tcx * r, tcy])
        py += rdiv

      #last path profile (tidies texture coords)
      verts.extend([0, py, px])
      norms.extend([0, dx, -dy])
      tex_coords.extend([1.0, tcy])

      if p < s-1:
        if tris:
          # Create indices for GL_TRIANGLES
          pn += (rl + 1)
          for r in range(rl):
            idx.extend([pp + r + 1, pp + r,
                        pn + r, pn + r,
                        pn + r + 1, pp + r + 1])
            ss += 6
          pp += (rl + 1)
        else:
          #Create indices for GL_TRIANGLE_STRIP
          pn += (rl + 1)
          for r in range(rl):
            idx.extend([pp + r, pn + r])
            ss += 2
          idx.extend([pp + self.sides, pn + self.sides])
          ss += 2
          pp += (rl + 1)

      opx = px
      opy = py

    if VERBOSE:
      print ssize, ss

    return (verts, norms, idx, tex_coords, ssize)

def normalize_vector(begin, end):
  diff = [e - b for b, e in zip(begin, end)]
  mag = Utility.magnitude(*diff)
  mult = 1 / mag if mag > 0.0 else 0.0
  return [x * mult for x in diff]

