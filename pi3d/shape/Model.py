from pi3d import *

from pi3d import Texture

from pi3d.context.TextureLoader import TextureLoader
from pi3d.loader import loaderEgg
from pi3d.loader import loaderObj
from pi3d.shape.Shape import Shape
from pi3d.util.RotateVec import rotate_vec
from pi3d.util.Matrix import Matrix

class Model(Shape):
  def __init__(self, camera=None, light=None, file_string=None,
               name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Model, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)
    if '__clone__' in file_string:
      # Creating a copy but with pointer to buf.
      return
    self.exf = file_string[-3:].lower()
    if VERBOSE:
      print "Loading ",file_string

    if self.exf == 'egg':
      self.model = loaderEgg.loadFileEGG(self, file_string)
      return self.model
    elif self.exf == 'obj':
      self.model = loaderObj.loadFileOBJ(self, file_string)
      return self.model
    else:
      print self.exf, "file not supported"
      return None

  def clone(self, camera = None, light = None):
    newModel = Model(file_string = "__clone__",x=self.unif[0], y=self.unif[1], z=self.unif[2],
               rx=self.unif[3], ry=self.unif[4], rz=self.unif[5], sx=self.unif[6], sy=self.unif[7], sz=self.unif[8],
               cx=self.unif[9], cy=self.unif[10], cz=self.unif[11])
    newModel.buf = self.buf
    newModel.vGroup = self.vGroup
    newModel.shader = self.shader
    newModel.textures = self.textures
    return newModel

  def reparentTo(self, parent):
    if self not in parent.childModel:
      parent.childModel.append(self)

  def texSwap(self, texID, filename):
    return loaderEgg.texSwap(self, texID, filename)

