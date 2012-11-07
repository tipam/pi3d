from pi3d import *
from pi3d import Texture
from pi3d import Utility

RECT_NORMALS = c_bytes(( 0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1 ))
RECT_TEX_COORDS = c_bytes(( 0,255, 255,255, 255,0, 0,0))
RECT_TEX_COORDS2 = c_floats(( 0,1, 1,1, 1,0, 0,0))
RECT_VERTS_TL = c_bytes(( 1,0,0, 0,0,0, 0,-1,0, 1,-1,0 ))
RECT_VERTS_CT = c_bytes(( 1,1,0, -1,1,0, -1,-1,0, 1,-1,0 ))
RECT_TRIANGLES = c_bytes(( 3,0,1, 3,1,2 ))

def string(font, string, x, y, z, rot, sclx, scly):
  opengles.glNormalPointer(GL_BYTE, 0, RECT_NORMALS)
  Utility.texture_min_mag()
  opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
  opengles.glBindTexture(GL_TEXTURE_2D,font.tex)
  opengles.glEnable(GL_TEXTURE_2D)

  opengles.glDisable(GL_DEPTH_TEST)
  opengles.glDisable(GL_CULL_FACE)
  opengles.glEnable(GL_BLEND)
  opengles.glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

  mtrx =(c_float * 16)()
  opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(mtrx))
  Utility.translatef(x, y, z)
  Utility.rotatef(rot, 0, 0, 1)
  Utility.scalef(sclx, scly, 1)

  for c in range(0,len(string)):
    v = ord(string[c])-32
    w, h, texc, verts = font.chr[v]
    if v > 0:
      opengles.glVertexPointer(3, GL_FLOAT, 0,verts)
      opengles.glTexCoordPointer(2, GL_FLOAT,0,texc)
      opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, RECT_TRIANGLES)
    Utility.translatef(w, 0, 0)

  opengles.glLoadMatrixf(mtrx)
  opengles.glDisable(GL_TEXTURE_2D)
  opengles.glDisable(GL_BLEND)
  opengles.glEnable(GL_DEPTH_TEST)
  opengles.glEnable(GL_CULL_FACE)

def _draw(verts, tex, x, y, w, h, r, z):
  opengles.glNormalPointer(GL_BYTE, 0, RECT_NORMALS);
  opengles.glVertexPointer(3, GL_BYTE, 0, verts);
  Utility.load_identity()
  Utility.translatef(x, y, z)
  Utility.scalef(w, h, 1)
  if r:
    Utility.rotatef(r, 0, 0, 1)
  with Texture.Loader(tex,RECT_TEX_COORDS,GL_BYTE):
    opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, RECT_TRIANGLES)

def rectangle(tex, x, y, w, h, r=0.0, z=-1.0):
  _draw(RECT_VERTS_TL, tex, x, y, w, h, r, z)

def sprite(tex, x, y, z=-10.0, w=1.0, h=1.0, r=0.0):
  _draw(RECT_VERTS_CT, tex, x, y, w, h, r, z)

