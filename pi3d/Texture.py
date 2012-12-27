import ctypes
import Image

from pi3d import *
from pi3d.util.Loadable import Loadable

MAX_SIZE = 1024
DEFER_TEXTURE_LOADING = True

def round_up_to_power_of_2(x):
  p = 1
  while p <= x:
    p += p
  return p

class Texture(Loadable):
  def __init__(self, file_string, blend=False, flip=False, size=0,
               defer=DEFER_TEXTURE_LOADING):
    super(Texture, self).__init__()
    self.file_string = file_string
    self.blend = blend
    self.flip = flip
    self.size = size
    if defer:
      self.load_disk()
    else:
      self.load_opengl()

  def tex(self):
    self.load_opengl()
    return self._tex

  def _unload_opengl(self):
    texture_array = c_ints([self._tex.value])
    opengles.glDeleteTextures(1, ctypes.addressof(texture_array))

  def _load_disk(self):
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
    self._tex = ctypes.c_int()

  def _load_opengl(self):
    opengles.glGenTextures(1, ctypes.byref(self._tex), 0)
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          ctypes.string_at(self.image, len(self.image)))
    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                             c_float(GL_LINEAR_MIPMAP_LINEAR))
    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                             c_float(GL_LINEAR))
    opengles.glGenerateMipmap(GL_TEXTURE_2D)
    opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class Cache(object):
  def __init__(self):
    self.clear()

  def clear(self):
    self.cache = {}

  def create(self, file_string, blend=False, flip=False, size=0):
    texture = self.cache.get((file_string, blend, flip, size), None)
    if not texture:
      texture = Texture(file_string, blend=blend, flip=flip, size=size)
      self.cache[file_string] = texture
    return texture
