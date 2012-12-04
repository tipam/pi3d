from pi3d import *
from pi3d.util import Utility

class Matrix(object):
  def __init__(self):
    self.mat = []
    self.mc = 0

  def identity(self):
    Utility.load_identity()
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
    Utility.translatef(x, y, z)

  def rotate(self, rx, ry, rz):
    if rz:
      Utility.rotatef(rz, 0, 0, 1)
    if rx:
      Utility.rotatef(rx, 1, 0, 0)
    if ry:
      Utility.rotatef(ry, 0, 1, 0)

  def scale(self, sx, sy, sz):
    # TODO: get rid of this.
    Utility.scalef(sx, sy, sz)

