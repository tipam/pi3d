import ctypes
import Image

from pi3d import *
from pi3d.util import Utility

class TextureLoader(object):
  ALPHA_VALUE = c_float(0.6)  # TODO: where does this come from?
  TEXTURE_SET = False

  def __init__(self, texture, coords, vtype=GL_FLOAT):
    self.texture = texture
    self.coords = coords
    self.vtype = vtype

  def __enter__(self):
    if self.texture:
      Utility.texture_min_mag()
      opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
      opengles.glTexCoordPointer(2, self.vtype, 0, self.coords)
      opengles.glBindTexture(GL_TEXTURE_2D, self.texture.tex())
      opengles.glEnable(GL_TEXTURE_2D)
      if self.texture.alpha:
        if self.texture.blend:
          #opengles.glDisable(GL_DEPTH_TEST)
          opengles.glEnable(GL_BLEND)
          opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        else:
          opengles.glAlphaFunc(GL_GREATER, c_float(0.6))
          opengles.glEnable(GL_ALPHA_TEST)
      TextureLoader.TEXTURE_SET = True

  def __exit__(self, type, value, traceback):
    if TextureLoader.TEXTURE_SET:
      opengles.glDisable(GL_TEXTURE_2D)
      opengles.glDisable(GL_ALPHA_TEST)
      opengles.glDisable(GL_BLEND)
      opengles.glEnable(GL_DEPTH_TEST)

      TextureLoader.TEXTURE_SET = False
      # This is why we have TextureLoader.TEXTURE_SET - so that we can nest
      # Loaders without calling the _exit__ function twice.

