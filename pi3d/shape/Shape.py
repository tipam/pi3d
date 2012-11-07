from pi3d import Texture
from pi3d.pi3dCommon import *

class Shape(object):
  def __init__(self, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz):
    self.name = name
    self.x = x                #position
    self.y = y
    self.z = z
    self.rotx = rx                #rotation
    self.roty = ry
    self.rotz = rz
    self.sx = sx                #scale
    self.sy = sy
    self.sz = sz
    self.cx = cx                #center
    self.cy = cy
    self.cz = cz

        #this should all be done with matrices!! ... just for testing ...

  def draw(self, tex=None, shl=GL_UNSIGNED_SHORT):
    opengles.glShadeModel(GL_SMOOTH)
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.vertices)
    opengles.glNormalPointer(GL_FLOAT, 0, self.normals)
    with Texture.Loader(tex, self.tex_coords):
      mtrx = (c_float * 16)()
      opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
      transform(self.x, self.y, self.z, self.rotx, self.roty, self.rotz,
                self.sx, self.sy, self.sz, self.cx, self.cy, self.cz)
      opengles.glDrawElements( self.ttype, self.ssize, shl , self.indices)
      opengles.glLoadMatrixf(mtrx)

  def scale(self, sx, sy, sz):
    self.sx = sx
    self.sy = sy
    self.sz = sz

  def position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def translate(self, dx, dy, dz):
    self.x = self.x + dx
    self.y = self.y + dy
    self.z = self.z + dz

  def rotateToX(self, v):
    self.rotx = v

  def rotateToY(self, v):
    self.roty = v

  def rotateToZ(self, v):
    self.rotz = v

  def rotateIncX(self,v):
    self.rotx += v

  def rotateIncY(self,v):
    self.roty += v

  def rotateIncZ(self,v):
    self.rotz += v

