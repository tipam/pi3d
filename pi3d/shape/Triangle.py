from pi3d.constants import *
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape

class Triangle(Shape):
  """ 3d model inherits from Shape. The simplest possible shape: a single
  triangle
  """
  def __init__(self,  camera=None, light=None, name="", 
                corners=((-0.5, -0.28868), (0.0, 0.57735), (0.5, -0.28868)),
                x=0.0, y=0.0, z=0.0, sx=1.0, sy=1.0, sz=1.0,
                rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0):
    """Uses standard constructor for Shape with ability to position corners.
    The corners must be arranged clockwise (for the Triangle to face -z direction)
    The uv mapping is taken from an equilateral triangles base 0,0 to 1,0
    peak at 0.5, 0.86603 Keyword argument:

      *corners*
        A tuple of three (xy) tuples defining the corners
    """
    super(Triangle, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)
    self.ttype = GL_TRIANGLES
    self.verts = []
    self.norms = []
    self.texcoords = []
    self.inds = []
    c = corners # alias for convenience

    self.verts = ((c[0][0], c[0][1], 0.0), (c[1][0], c[1][1], 0.0), (c[2][0], c[2][1], 0.0))
    self.norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1))
    self.texcoords = ((0.0, 0.0), (0.5, 0.86603), (1.0, 0.0))

    self.inds = ((0, 1, 2), ) #python quirk: comma for tuple with only one val

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))
