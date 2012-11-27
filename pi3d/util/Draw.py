from pi3d import *
from pi3d.context.TextureLoader import TextureLoader
from pi3d.util import Utility

RECT_TEX_COORDS = c_bytes((0, 255,
                           255, 255,
                           255, 0,
                           0, 0))

RECT_TEX_COORDS2 = c_floats((0, 1,
                             1, 1,
                             1, 0,
                             0, 0))

RECT_VERTS_TL = c_bytes((1, 0, 0,
                         0, 0, 0,
                         0, -1, 0,
                         1, -1, 0))

RECT_VERTS_CT = c_bytes((1, 1, 0,
                         -1, 1, 0,
                         -1, -1, 0,
                         1, -1, 0))

def draw(verts, tex, x, y, w, h, r, z):
  Utility.rect_normals()
  opengles.glVertexPointer(3, GL_BYTE, 0, verts);
  Utility.load_identity()
  Utility.translatef(x, y, z)
  Utility.scalef(w, h, 1)
  if r:
    Utility.rotatef(r, 0, 0, 1)
  with TextureLoader(tex, RECT_TEX_COORDS, GL_BYTE):
    Utility.rect_triangles()

def rectangle(tex, x, y, w, h, r=0.0, z=-1.0):
  draw(RECT_VERTS_TL, tex, x, y, w, h, r, z)

def sprite(tex, x, y, z=-10.0, w=1.0, h=1.0, r=0.0):
  draw(RECT_VERTS_CT, tex, x, y, w, h, r, z)

