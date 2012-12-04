from pi3d import *

from pi3d.util import Utility

def string(font, string, x, y, z, rot, sclx, scly):
  Utility.rect_normals()
  Utility.texture_min_mag()

  opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
  opengles.glBindTexture(GL_TEXTURE_2D, font.tex)
  opengles.glEnable(GL_TEXTURE_2D)

  opengles.glDisable(GL_DEPTH_TEST)
  opengles.glDisable(GL_CULL_FACE)
  opengles.glEnable(GL_BLEND)
  opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  mtrx = (c_float * 16)()
  opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
  Utility.translatef(x, y, z)
  Utility.rotatef(rot, 0, 0, 1)
  Utility.scalef(sclx, scly, 1)

  for c in range(0,len(string)):
    v = ord(string[c]) - 32
    w, h, texc, verts = font.chr[v]
    if v > 0:
      opengles.glVertexPointer(3, GL_FLOAT, 0, verts)
      opengles.glTexCoordPointer(2, GL_FLOAT, 0, texc)
      Utility.rect_triangles()
    Utility.translatef(w, 0, 0)

  opengles.glLoadMatrixf(mtrx)
  opengles.glDisable(GL_TEXTURE_2D)
  opengles.glDisable(GL_BLEND)
  opengles.glEnable(GL_DEPTH_TEST)
  opengles.glEnable(GL_CULL_FACE)

