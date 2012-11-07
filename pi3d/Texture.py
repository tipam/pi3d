import ctypes
import Image

from pi3d import *
from pi3d import Utility

MAX_SIZE = 1024

#load a texture specifying RGB or RGBA
def _load_tex(fileString,flip,size,blend):
  s = fileString + ' '
  im = Image.open(fileString)
  ix, iy = im.size
  s += '(%s)' % im.mode
  if im.mode == 'RGBA' or im.mode == 'LA':
    RGBv = GL_RGBA
    RGBs = 'RGBA'
  else:
    RGBv = GL_RGB
    RGBs = 'RGB'

  # work out if sizes are not to the power of 2 or >512
  # TODO: why must texture sizes be a power of 2?
  xx = 0
  yy = 0
  nx, ny = ix, iy
  while (2**xx) < nx:
    xx += 1
  while (2**yy) < ny:
    yy+=1
  if (2 ** xx) > nx:
    nx = 2 ** xx
  if (2 ** yy) > ny:
    ny=2 ** yy
  nx = min(nx, MAX_SIZE)
  ny = min(ny, MAX_SIZE)

  if nx != ix or ny != iy or size>0:
    if VERBOSE:
      print ix, iy
    if size > 0:
      nx, ny = size, size
    ix, iy = nx, ny
    im = im.resize((ix, iy), Image.ANTIALIAS)
    s += 'Resizing to: %d, %d' % (ix, iy)
  else:
    s += 'Bitmap size: %d, %d' % (ix, iy)

  if VERBOSE:
    print 'Loading ...',s

  if flip:
    im = im.transpose(Image.FLIP_TOP_BOTTOM)

  image = im.convert(RGBs).tostring('raw',RGBs)
  tex = ctypes.c_int()
  opengles.glGenTextures(1, ctypes.byref(tex))
  opengles.glBindTexture(GL_TEXTURE_2D, tex)
  opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, ix, iy, 0, RGBv,
                        GL_UNSIGNED_BYTE, ctypes.string_at(image, len(image)))
  return ix, iy, tex, RGBs=='RGBA', blend

class _Texture(object):
  def __init__(self, fileString, flip=False, size=0, blend=False):
    t = _load_tex(fileString, flip, size, blend)
    self.ix, self.iy, self.tex, self.alpha, self.blend = t

class Textures(object):
  def __init__(self):
    self.texs = (ctypes.c_int * 1024)()   #maximum of 1024 textures (just to be safe!)
    self.tc = 0

  def loadTexture(self, fileString, blend=False, flip=False, size=0):
    # TODO: why are all these textures 'cached' without being retrievable?
    # If they are cached at all, it should be keyed by the fileString.
    texture = _Texture(fileString, flip, size, blend)
    self.texs[self.tc] = texture.tex.value
    self.tc += 1
    return texture

  def deleteAll(self):
    if VERBOSE:
      print '[Exit] Deleting textures ...'
      opengles.glDeleteTextures(self.tc, addressof(self.texs))

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
          opengles.glDisable(GL_DEPTH_TEST)
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

