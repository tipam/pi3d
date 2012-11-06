from pi3d.pi3dCommon import *
from pi3d import Constants

class Texture(object):
  def __init__(self, fileString, flip=False, size=0, blend=False):
    t = load_tex(fileString, flip, size, blend)
    self.ix, self.iy, self.tex, self.alpha, self.blend = t

class Textures(object):
  def __init__(self):
    self.texs = (eglint * 1024)()   #maximum of 1024 textures (just to be safe!)
    self.tc = 0

  def loadTexture(self, fileString, blend=False, flip=False, size=0):
    texture = Texture(fileString, flip, size, blend)
    self.texs[self.tc] = texture.tex.value
    self.tc += 1
    return texture

  def deleteAll(self):
    if Constants.VERBOSE:
      print "[Exit] Deleting textures ..."
      opengles.glDeleteTextures(self.tc, addressof(self.texs))
