from pi3d.pi3dCommon import *
from pi3d import Constants
from pi3d import loaderEgg
from pi3d.shape.Shape import Shape

class Model(Shape):
  def __init__(self, fileString, texs, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Model, self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    self.exf = fileString[-3:].lower()
    self.texs = texs
    if Constants.VERBOSE:
      print "Loading ",fileString

    if self.exf == 'egg':
      self.model = loaderEgg.loadFileEGG(self, fileString, texs)
      return self.model
    else:
      print self.exf, "file not supported"
      return None

  def draw(self,tex=None,n=None):
    if self.exf == 'egg':
      loaderEgg.draw(self, tex, n)

  def clone(self):
    newLM = loadModel("__clone__." + self.exf, self.texs)
    newLM.vGroup = self.vGroup
    return newLM

  def reparentTo(self, parent):
    if not(self in parent.childModel):
      parent.childModel.append(self)

  def texSwap(self, texID, filename):
    return loaderEgg.texSwap(self, texID, filename)

