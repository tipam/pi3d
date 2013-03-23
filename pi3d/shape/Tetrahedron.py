from pi3d.constants import *
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape

class Tetrahedron(Shape):
  """ 3d model inherits from Shape. The simplest 3D shape
  """
  def __init__(self,  camera=None, light=None, name="", 
                corners=((-1.0, -0.57735, -0.57735),
                         (1.0, -0.57735, -0.57735),
                         (0.0, -0.57735, 1.15470),
                         (0.0, 1.15470, 0.0)),
                x=0.0, y=0.0, z=0.0, sx=1.0, sy=1.0, sz=1.0,
                rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0):
    """Uses standard constructor for Shape with ability to position corners.
    The uv mapping is taken from four equilateral triangles arranged on a
    square forming an upwards pointing arrow ^. Starting at the left bottom
    corner of the image the first three triangles are unwrapped from around
    the top of the tetrahedron and the right bottom triangle is the base
    (if the corners are arranged as per the default) Keyword argument:

      *corners*
        A tuple of four (xyz) tuples defining the corners
    """
    super(Tetrahedron, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)
    self.ttype = GL_TRIANGLES
    c = corners # alias
    self.verts = (c[0], c[3], c[1], c[2], c[3], c[0],
                  c[1], c[3], c[2], c[0], c[1], c[2])
    self.texcoords = ((0.0, 0.0), (0.0, 0.57735), (0.5, 0.288675),
                      (0.0, 0.57735), (0.5, 0.866025), (0.5, 0.288675),
                      (0.5, 0.866025), (1.0, 0.57735), (0.5, 0.288675),
                      (0.5, 0.288675), (1.0, 0.57735), (1.0, 0.0))
    self.inds = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11))

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, normals=None, smooth=False))
