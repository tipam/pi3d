from pi3d.pi3dCommon import *

class Matrix(object):
  def __init__(self):
    self.mat = []
    self.mc = 0

  def identity(self):
    opengles.glLoadIdentity()
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
    opengles.glTranslatef(c_float(x),c_float(y),c_float(z))

  def rotate(self,rx,ry,rz):
    if rz:
      opengles.glRotatef(c_float(rz), c_float(0), c_float(0), c_float(1))
    if rx:
      opengles.glRotatef(c_float(rx), c_float(1), c_float(0), c_float(0))
    if ry:
      opengles.glRotatef(c_float(ry), c_float(0), c_float(1), c_float(0))

  def scale(self,sx,sy,sz):
    opengles.glScalef(c_float(sx), c_float(sy), c_float(sz))

