from pi3d.pi3dCommon import *
from pi3d import Constants

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
  # TODO: why does this have to happen?
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
    if Constants.VERBOSE:
      print ix, iy
    if size > 0:
      nx, ny = size, size
    ix, iy = nx, ny
    im = im.resize((ix, iy), Image.ANTIALIAS)
    s += 'Resizing to: %d, %d' % (ix, iy)
  else:
    s += 'Bitmap size: %d, %d' % (ix, iy)

  if Constants.VERBOSE:
    print 'Loading ...',s

  if flip:
    im = im.transpose(Image.FLIP_TOP_BOTTOM)

  image = im.convert(RGBs).tostring('raw',RGBs)
  tex = eglint()
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
    self.texs = (eglint * 1024)()   #maximum of 1024 textures (just to be safe!)
    self.tc = 0

  def loadTexture(self, fileString, blend=False, flip=False, size=0):
    # TODO: why are all these textures 'cached' without being retrievable?
    # If they are cached at all, it should be keyed by the fileString.
    texture = _Texture(fileString, flip, size, blend)
    self.texs[self.tc] = texture.tex.value
    self.tc += 1
    return texture

  def deleteAll(self):
    if Constants.VERBOSE:
      print '[Exit] Deleting textures ...'
      opengles.glDeleteTextures(self.tc, addressof(self.texs))
