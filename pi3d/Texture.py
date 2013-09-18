#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import print_function

import ctypes
import sys

from six.moves import xrange

from PIL import Image

from pi3d.constants import *
from pi3d.util.Ctypes import c_ints
from pi3d.util.Loadable import Loadable

MAX_SIZE = 1920
DEFER_TEXTURE_LOADING = True
WIDTHS = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256,
           288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920]

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
    if file_string[0] == '/': #absolute address
      self.file_string = file_string
    else:
      self.file_string = sys.path[0] + '/' + file_string
    self.blend = blend
    self.flip = flip
    self.size = size
    self.mipmap = mipmap
    self.byte_size = 0
    if defer:
      self.load_disk()
    else:
      self.load_opengl()

  def __del__(self):
    super(Texture, self).__del__()
    try:
      from pi3d.Display import Display
      if Display.INSTANCE:
        Display.INSTANCE.textures_dict[str(self._tex)][1] = 1
        Display.INSTANCE.tidy_needed = True
    except:
      print("couldn't set to delete") #TODO debug messages here

  def tex(self):
    """do the deferred opengl work and return texture"""
    self.load_opengl()
    return self._tex

  def _load_disk(self):
    """overrides method of Loadable
    Pngfont, Font, Defocus and ShadowCaster inherit from Texture but
    don't do all this so have to override this
    """
    s = self.file_string + ' '
    im = Image.open(self.file_string)

    self.ix, self.iy = im.size
    s += '(%s)' % im.mode
    self.alpha = (im.mode == 'RGBA' or im.mode == 'LA')

    if self.mipmap:
      resize_type = Image.BICUBIC
    else:
      resize_type = Image.NEAREST

    # work out if sizes > MAX_SIZE or coerce to golden values in WIDTHS
    if self.iy > self.ix and self.iy > MAX_SIZE: # fairly rare circumstance
      im = im.resize((int((MAX_SIZE * self.ix) / self.iy), MAX_SIZE))
      self.ix, self.iy = im.size
    n = len(WIDTHS)
    for i in xrange(n-1, 0, -1):
      if self.ix == WIDTHS[i]:
        break # no need to resize as already a golden size
      if self.ix > WIDTHS[i]:
        im = im.resize((WIDTHS[i-1], int((WIDTHS[i-1] * self.iy) / self.ix)),
                        resize_type)
        self.ix, self.iy = im.size
        break

    if VERBOSE:
      print('Loading ...{}'.format(s))

    if self.flip:
      im = im.transpose(Image.FLIP_TOP_BOTTOM)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()
    if 'fonts/' in self.file_string:
      self.im = im

  def _load_opengl(self):
    """overrides method of Loadable"""
    opengles.glGenTextures(4, ctypes.byref(self._tex), 0)
    from pi3d.Display import Display
    if Display.INSTANCE:
      Display.INSTANCE.textures_dict[str(self._tex)] = [self._tex, 0]
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          ctypes.string_at(self.image, len(self.image)))
    opengles.glEnable(GL_TEXTURE_2D)
    opengles.glGenerateMipmap(GL_TEXTURE_2D)
    opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if self.mipmap:
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               GL_LINEAR_MIPMAP_NEAREST)
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               GL_LINEAR)
    else:
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               GL_NEAREST)
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               GL_NEAREST)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                             GL_MIRRORED_REPEAT)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                             GL_MIRRORED_REPEAT)


  def _unload_opengl(self):
    """clear it out"""
    opengles.glDeleteTextures(1, ctypes.byref(self._tex))


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
