#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import print_function

import ctypes
import sys, os
import numpy as np

from six.moves import xrange

from PIL import Image

from pi3d.constants import *
from pi3d.util.Ctypes import c_ints
from pi3d.util.Loadable import Loadable

MAX_SIZE = 1920
DEFER_TEXTURE_LOADING = True
WIDTHS = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256,
           288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920]
FILE = 0
PIL_IMAGE = 1
NUMPY = 2

def round_up_to_power_of_2(x):
  p = 1
  while p <= x:
    p += p
  return p

class Texture(Loadable):
  """loads an image file from disk and converts it into an array that
  can be used by shaders. It inherits from Loadable in order that the
  file access work can happen in another thread. and the conversion
  to opengl format can happen just in time when tex() is first called.

  NB images loaded as textures can cause distortion effects unless they
  are certain sizes (below). **If the image width is a value not in this
  list then it will be rescaled with a resulting loss of clarity**

  Allowed widths 4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256, 288,
  384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920
  """
  def __init__(self, file_string, blend=False, flip=False, size=0,
               defer=DEFER_TEXTURE_LOADING, mipmap=True, m_repeat=False,
               free_after_load=False, i_format=None):
    """
    Arguments:
      *file_string*
        path and name of image file relative to top dir. Can now pass an
        already created PIL.Image object or a numpy array instead. The alpha
        value of Texture willl be set according to the 'mode' of Image objects
        or the size of the last dimension of numpy arrays (4 -> alpha is True)
      *blend*
        controls if low alpha pixels are discarded (if False) or drawn
        by the shader. If set to true then this texture needs to be
        drawn AFTER other objects that are FURTHER AWAY
      *flip*
        flips the image [not used for numpy arrays]
      *size*
        to resize image to [not used for numpy arrays]
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
      *m_repeat*
        if the texture is repeated (see umult and vmult in Shape.set_draw_details)
        then this can be used to make a non-seamless texture tile
      *free_after_load*
        release image memory after loading it in opengl
      *i_format*
        opengl internal format for the texture - see glTexImage2D
    """
    super(Texture, self).__init__()
    try:
      # should jump out of try/except if not a string when startswith() called
      self.string_type = FILE # read image from file
      if file_string.startswith('/') or file_string.startswith('C:'): #absolute address
        self.file_string = file_string
      else:
        for p in sys.path:
          self.file_string = os.path.join(p, file_string)
          if os.path.isfile(os.path.join(p, file_string)): # this could theoretically get different files with same name
            break
    except:
      self.file_string = file_string
      if isinstance(self.file_string, np.ndarray):
        self.string_type = NUMPY # file_string is a numpy array
      else:
        self.string_type = PIL_IMAGE # file_string is a PIL Image
    self.blend = blend
    self.flip = flip
    self.size = size
    self.mipmap = mipmap
    self.m_repeat = GL_MIRRORED_REPEAT if m_repeat else GL_REPEAT
    self.byte_size = 0
    self.free_after_load = free_after_load
    self.i_format = i_format
    self._loaded = False
    if defer:
      self.load_disk()
    else:
      self.load_opengl()

  def __del__(self):
    super(Texture, self).__del__()
    try:
      from pi3d.Display import Display
      if Display.INSTANCE is not None:
        Display.INSTANCE.textures_dict[str(self._tex)][1] = 1
        Display.INSTANCE.tidy_needed = True
    except:
      pass #many reasonable reasons why this might fail

  def tex(self):
    """do the deferred opengl work and return texture"""
    self.load_opengl()
    return self._tex

  def _load_disk(self):
    """overrides method of Loadable
    Pngfont, Font, Defocus and ShadowCaster inherit from Texture but
    don't do all this so have to override this
    """
    
    # If already loaded, abort
    if self._loaded:
      return

    if self.string_type == FILE:
      s = self.file_string + ' '
      im = Image.open(self.file_string)
    elif self.string_type == PIL_IMAGE:
      s = 'PIL.Image '
      im = self.file_string
    else:
      s = 'numpy.ndarray '
      self.iy, self.ix, mode = self.file_string.shape
      self.alpha = (mode == 4)
      self.image = self.file_string
      self._tex = ctypes.c_int()
      self._loaded = True
      return # skip the rest for numpy arrays - faster but no size checking

    # only do this if loading from disk or PIL image
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
        im = im.resize((WIDTHS[i], int((WIDTHS[i] * self.iy) / self.ix)),
                        resize_type)
        self.ix, self.iy = im.size
        break

    if VERBOSE:
      print('Loading ...{}'.format(s))

    if self.flip:
      im = im.transpose(Image.FLIP_TOP_BOTTOM)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    if im.mode != RGBs:
      im = im.convert(RGBs)
    #self.image = im.tostring('raw', RGBs) # TODO change to tobytes WHEN Pillow is default PIL in debian (jessie becomes current)
    self.image = np.array(im)
    self._tex = ctypes.c_int()
    if self.string_type == FILE and 'fonts/' in self.file_string:
      self.im = im
      
    self._loaded = True

  def _load_opengl(self):
    """overrides method of Loadable"""
    try:
      opengles.glGenTextures(1, ctypes.byref(self._tex), 0)
    except: # TODO windows throws exceptions just for this call!
      print("[warning glGenTextures() on windows only!]")
    from pi3d.Display import Display
    if Display.INSTANCE is not None:
      Display.INSTANCE.textures_dict[str(self._tex)] = [self._tex, 0]
    self.update_ndarray()

  def update_ndarray(self, new_array=None):
    """to allow numpy arrays to be patched in to textures without regenerating
    new glTextureBuffers i.e. for movie textures"""
    if new_array is not None:
      self.image = new_array
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    iformat = self.i_format if self.i_format else RGBv
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, iformat, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          self.image.ctypes.data_as(ctypes.POINTER(ctypes.c_short)))
    opengles.glEnable(GL_TEXTURE_2D)
    if self.mipmap:
      opengles.glGenerateMipmap(GL_TEXTURE_2D)
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
                             self.m_repeat)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                             self.m_repeat)
    if self.free_after_load:
        self.image = None
        self._loaded = False


  def _unload_opengl(self):
    """clear it out"""
    opengles.glDeleteTextures(1, ctypes.byref(self._tex))

    
  # Implement pickle/unpickle support
  def __getstate__(self):
    # Make sure the image is actually loaded
    if not self._loaded:
      self._load_disk()
      
    return {
      'blend': self.blend,
      'flip': self.flip,
      'size': self.size,
      'mipmap': self.mipmap,
      'file_string': self.file_string,
      'ix': self.ix,
      'iy': self.iy,
      'alpha': self.alpha,
      'image': self.image,
      '_tex': self._tex,
      '_loaded': self._loaded,
      'opengl_loaded': False,
      'disk_loaded': self.disk_loaded,
      'm_repeat': self.m_repeat
      }

class TextureCache(object):
  def __init__(self, max_size=None): #TODO use max_size in some way
    self.clear()

  def clear(self):
    self.cache = {}

  def create(self, file_string, blend=False, flip=False, size=0, **kwds):
    key = file_string, blend, flip, size
    texture = self.cache.get(key, None)
    if texture is None:
      texture = Texture(*key, **kwds)
      self.cache[key] = texture

    return texture
