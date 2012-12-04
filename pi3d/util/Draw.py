import math

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

def distance(x1, y1, z1, x2, y2, z2):
  dx = x1 - x2
  dy = y1 - y2
  dz = z1 - z2
  return math.sqrt(dx * dx + dy * dy + dz * dz)

def lodDraw3(px, py, pz, dist1, model1,
             dist2=1000, model2=None,
             dist3=1500, model3=None):
  dist = distance(px, py, pz, model1.x, model1.y, model1.z)
  if dist <= dist3:
    return

  if dist < dist1:
    model1.draw()
    return

  if not model2:
    if dist < dist2:
      model2.draw()
      return

  if model3:
    model3.draw()

# TODO: this isn't the right signature for model so this code won't work.
def lodDraw3xyz(px, py, pz,
                mx, my, mz,
                dist1, model1,
                dist2=1000, model2=None,
                dist3=1500, model3=None):
  def draw(model):
    model.x = mx
    model.y = my
    model.y = mx
    model.draw()

  dist = distance(px, py, pz, mx, my, mz)
  if dist > dist3:
    return

  if dist < dist1:
    draw(model1)
    return

  if model2:
    if dist < dist2:
      draw(model2)
      return

  if model3:
    draw(model3)
