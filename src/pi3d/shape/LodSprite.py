from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape

class LodSprite(Shape):
  """ 3d model inherits from Shape, differs from Plane in being single sided
  Also has the ability to divide into more triangle (than 2) to allow some
  post processing in the vertex shader"""
  def __init__(self, camera=None, light=None, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=20.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0, n=1):
    """Uses standard constructor for Shape. Extra Keyword arguments:

      *w*
        Width.
      *h*
        Height.
      *n*
        How many cells to divide the plane into
    """
    super(LodSprite, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                 sx, sy, sz, cx, cy, cz)
    self.width = w
    self.height = h
    verts = []
    norms = []
    texcoords = []
    inds = []

    ww = w / 2.0
    hh = h / 2.0

    for a in range(n):
      j = float(a)
      for b in range(n):
        i = float(b)
        c = [[i / n, (n - j) / n],
            [(i + 1.0) / n, (n - j) / n],
            [(i + 1.0) / n, (n - 1.0 - j) / n],
            [i / n, (n - 1.0 - j) / n]]
        verts.extend([[-ww + c[0][0] * w, -hh + c[0][1] * h, 0.0],
                          [-ww + c[1][0] * w, -hh + c[1][1] * h, 0.0],
                          [-ww + c[2][0] * w, -hh + c[2][1] * h, 0.0],
                          [-ww + c[3][0] * w, -hh + c[3][1] * h, 0.0]])
        norms.extend([[0.0, 0.0, -1.0],
                          [0.0, 0.0, -1.0],
                          [0.0, 0.0, -1.0],
                          [0.0, 0.0, -1.0]])
        texcoords.extend([[c[0][0], 1.0 - c[0][1]],
                          [c[1][0], 1.0 - c[1][1]],
                          [c[2][0], 1.0 - c[2][1]],
                          [c[3][0], 1.0 - c[3][1]]])
        tri_n = (a * n + b) * 4 # integers
        inds.extend([[tri_n , tri_n + 1, tri_n + 3],
                          [tri_n + 1, tri_n + 2, tri_n + 3]])
    self.buf = [Buffer(self, verts, texcoords, inds, norms)]

  def repaint(self, t):
    self.draw()
