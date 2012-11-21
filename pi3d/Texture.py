import ctypes
import Image

from pi3d import *
from pi3d.util import Utility

MAX_SIZE = 1024

def round_up_to_power_of_2(x):
  p = 1
  while p <= x:
    p += p
  return p

class _Texture(object):
  def __init__(self, file_string, flip=False, size=0, blend=False):
    self.file_string = file_string
    self.flip = flip
    self.size = size
    self.blend = blend
    self.loaded = self.preloaded = False

  def preload(self):
    if self.preloaded:
      return

    s = self.file_string + ' '
    im = Image.open(self.file_string)
    self.ix, self.iy = im.size
    s += '(%s)' % im.mode
    self.alpha = (im.mode == 'RGBA' or im.mode == 'LA')

    # work out if sizes are not to the power of 2 or >512
    # TODO: why must texture sizes be a power of 2?
    xx = 0
    yy = 0
    nx, ny = self.ix, self.iy
    while (2 ** xx) < nx:
      xx += 1
    while (2 ** yy) < ny:
      yy += 1
    if (2 ** xx) > nx:
      nx = 2 ** xx
    if (2 ** yy) > ny:
      ny = 2 ** yy
    nx = min(nx, MAX_SIZE)
    ny = min(ny, MAX_SIZE)

    if nx != self.ix or ny != self.iy or self.size > 0:
      if VERBOSE:
        print self.self.ix, self.iy
      if self.size > 0:
        nx, ny = self.size, self.size
      self.ix, self.iy = nx, ny
      im = im.resize((self.ix, self.iy), Image.ANTIALIAS)
      s += 'Resizing to: %d, %d' % (self.ix, self.iy)
    else:
      s += 'Bitmap size: %d, %d' % (self.ix, self.iy)

    if VERBOSE:
      print 'Loading ...',s

    if self.flip:
      im = im.transpose(Image.FLIP_TOP_BOTTOM)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = im.convert(RGBs).tostring('raw',RGBs)
    self.tex = ctypes.c_int()
    self.preloaded = True

  def load_on_display_thread(self):
    if self.loaded:
      return

    self.preload()
    opengles.glGenTextures(1, ctypes.byref(self.tex))
    opengles.glBindTexture(GL_TEXTURE_2D, self.tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE, ctypes.string_at(self.image,
                                                             len(self.image)))
    self.loaded = True


class Textures(object):
  def __init__(self):
    # maximum of 1024 textures (just to be safe!)
    self.texs = (ctypes.c_int * 1024)()
    self.tc = 0

  def loadTexture(self, fileString, blend=False, flip=False, size=0):
    # TODO: why are all these textures 'cached' without being retrievable?
    # If they are cached at all, it should be keyed by the fileString.
    texture = _Texture(fileString, flip, size, blend)
    texture.load_on_display_thread()
    self.texs[self.tc] = texture.tex.value
    self.tc += 1
    return texture

  def deleteAll(self):
    if VERBOSE:
      print '[Exit] Deleting textures ...'
      opengles.glDeleteTextures(self.tc, addressof(self.texs))

# TODO: this should move to context
class Loader(object):
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
      opengles.glBindTexture(GL_TEXTURE_2D, self.texture.tex)
      opengles.glEnable(GL_TEXTURE_2D)
      if self.texture.alpha:
        if self.texture.blend:
          #opengles.glDisable(GL_DEPTH_TEST)
          opengles.glEnable(GL_BLEND)
          opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        else:
          opengles.glAlphaFunc(GL_GREATER, c_float(0.6))
          opengles.glEnable(GL_ALPHA_TEST)
      Loader.TEXTURE_SET = True

  def __exit__(self, type, value, traceback):
    if Loader.TEXTURE_SET:
      opengles.glDisable(GL_TEXTURE_2D)
      opengles.glDisable(GL_ALPHA_TEST)
      opengles.glDisable(GL_BLEND)
      opengles.glEnable(GL_DEPTH_TEST)

      Loader.TEXTURE_SET = False
      # This is why we have Loader.TEXTURE_SET - so that we can nest
      # Loaders without calling the _exit__ function twice.

