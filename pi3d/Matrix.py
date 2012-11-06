import pi3d

from pi3d.pi3dCommon import *

class Matrix(object):
  def __init__(self):
    self.mat = []
    self.mc = 0

  def identity(self):
    pi3d.load_identity()
    self.mc = 0

  def push(self):
    self.mat.append((c_float * 16)())
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(self.mat[self.mc]))
    self.mc += 1

  def pop(self):
    opengles.glMatrixMode(GL_MODELVIEW)
    if self.mc > 0:
      self.mc -= 1
      opengles.glLoadMatrixf(self.mat[self.mc])

  def translate(self,x,y,z):
    # TODO: get rid of this.
    pi3d.translatef(x, y, z)

  def rotate(self,rx,ry,rz):
    if rz:
      pi3d.rotatef(rz, 0, 0, 1)
    if rx:
      pi3d.rotatef(rx, 1, 0, 0)
    if ry:
      pi3d.rotatef(ry, 0, 1, 0)

  def scale(self, sx, sy, sz):
    # TODO: get rid of this.
    pi3d.scalef(sx, sy, sz)

