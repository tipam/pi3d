import ctypes
import Image

from pi3d.constants import *
from pi3d.util.Ctypes import c_ints
from pi3d.util.Loadable import Loadable

MAX_SIZE = 2048
DEFER_TEXTURE_LOADING = True

def round_up_to_power_of_2(x):
  p = 1
  while p <= x:
    p += p
  return p

class Texture(Loadable):
  """loads an image file from disk and converts it into an array that
  can be used by shaders. It inherits from Loadable in order that the
  file access work can happen in another thread. and the conversion
  to opengl format can happen just in time when tex() is first called
  """
  def __init__(self, file_string, blend=False, flip=False, size=0,
               defer=DEFER_TEXTURE_LOADING, mipmap=True):
    """
    Arguments:
      *file_string*
        path and name of image file relative to top dir
      *blend*
        controls if low alpha pixels are discarded (if False) or drawn
        by the shader. If set to true then this texture needs to be
        drawn AFTER other objects that are FURTHER AWAY
      *flip*
        flips the image
      *size*
        to resize image to
      *defer*
        can load from file in other thread and defer opengl work until
        texture needed, default True
      *mipmap*
        use linear interpolation for mipmaps, if set False then nearest
        pixel values will be used. This is needed for exact pixel represent-
        ation of images. **NB BECAUSE THIS BEHAVIOUR IS SET GLOBALLY AT
        THE TIME THAT THE TEXTURE IS LOADED IT WILL BE SET BY THE LAST
        TEXTURE TO BE LOADED PRIOR TO DRAWING**
        TODO possibly reset in Buffer.draw() each time a texture is loaded?
    """
    super(Texture, self).__init__()
    self.file_string = file_string
    self.blend = blend
    self.flip = flip
    self.size = size
    self.mipmap = mipmap
    self.byte_size = 0
    if defer:
      self.load_disk()
    else:
      self.load_opengl()

  def tex(self):
    """do the deferred opengl work and return texture"""
    self.load_opengl()
    return self._tex

  def _unload_opengl(self):
    """clear it out"""
    texture_array = c_ints([self._tex.value])
    opengles.glDeleteTextures(1, ctypes.addressof(texture_array))

  def _load_disk(self):
    """overrides method of Loadable
    Font, Ttffont and Defocus inherit from Texture but don't do all this
    so have to override this
    """
    s = self.file_string + ' '
    self.im = Image.open(self.file_string) # TODO only load this if needed because loading a Font

    self.ix, self.iy = self.im.size
    s += '(%s)' % self.im.mode
    self.alpha = (self.im.mode == 'RGBA' or self.im.mode == 'LA')

    # work out if sizes are not to the power of 2 or > MAX_SIZE
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
        print self.ix, self.iy
      if self.size > 0:
        nx, ny = self.size, self.size
      self.ix, self.iy = nx, ny
      self.im = self.im.resize((self.ix, self.iy), Image.ANTIALIAS)
      s += 'Resizing to: %d, %d' % (self.ix, self.iy)
    else:
      s += 'Bitmap size: %d, %d' % (self.ix, self.iy)

    if VERBOSE:
      print 'Loading ...', s

    if self.flip:
      self.im = self.im.transpose(Image.FLIP_TOP_BOTTOM)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()

  def _load_opengl(self):
    """overrides method of Loadable"""
    opengles.glGenTextures(1, ctypes.byref(self._tex), 0)
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          ctypes.string_at(self.image, len(self.image)))
    if self.mipmap:
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               ctypes.c_float(GL_LINEAR_MIPMAP_NEAREST))
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               ctypes.c_float(GL_LINEAR_MIPMAP_NEAREST))
    else:
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               ctypes.c_float(GL_NEAREST))
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               ctypes.c_float(GL_NEAREST))

    opengles.glGenerateMipmap(GL_TEXTURE_2D)
    opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class TextureCache(object):
  def __init__(self, max_size=None): #TODO use max_size in some way
    self.clear()

  def clear(self):
    self.cache = {}

  def create(self, file_string, blend=False, flip=False, size=0, **kwds):
    key = file_string, blend, flip, size
    texture = self.cache.get(key, None)
    if not texture:
      texture = Texture(*key, **kwds)
      self.cache[key] = texture

    return texture
