from __future__ import print_function

import ctypes
import sys, os
import numpy as np
import logging

from six_mod.moves import xrange

from pi3d.constants import (opengles, PIL_OK, GL_ALPHA, GL_LUMINANCE,
          GL_LUMINANCE_ALPHA, GL_RGB, GL_RGBA, GL_MIRRORED_REPEAT, GL_REPEAT,
          GL_LINEAR, GL_NEAREST, GL_LINEAR_MIPMAP_NEAREST, GL_NEAREST_MIPMAP_NEAREST,
          GL_TEXTURE_MIN_FILTER, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
          GL_TEXTURE_MAG_FILTER, GL_UNSIGNED_BYTE, GL_OUT_OF_MEMORY)
from pi3d.util.Ctypes import c_ints
from pi3d.util.Loadable import Loadable

if PIL_OK:
  from PIL import Image

LOGGER = logging.getLogger(__name__)
MAX_SIZE = 1920
DEFER_TEXTURE_LOADING = True
WIDTHS = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256,
           288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920]
FILE = 0
PIL_IMAGE = 1
NUMPY = 2
FORMAT_MODES = {GL_ALPHA: 'L',
                GL_LUMINANCE: 'L',
                GL_LUMINANCE_ALPHA: 'LA',
                GL_RGB: 'RGB',
                GL_RGBA: 'RGBA'}

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
               free_after_load=False, i_format=None, filter=None,
               normal_map=None):
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
        flips the image [not used for numpy arrays]. Now this parameter could
        be an integer value. If bit #0 is 1, a up-down flip is perfomed,
        also if bit #1 is set, a left-right flip occurs

      *size*
        to resize image to [not used for numpy arrays]
      *defer*
        can load from file in other thread and defer opengl work until
        texture needed, default True
      *mipmap*
        create and use mipmaps for this texture
        (if true - linear interpolation will be used by default, else nearest interpolation).
        see filter to control this behavior
        **NB BECAUSE THIS BEHAVIOUR IS SET GLOBALLY AT
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
      *filter*
        interpolation to use for for textures: GL_NEAREST or GL_LINEAR.
        if mipmap is true: NEAREST_MIPMAP_NEAREST or LINEAR_MIPMAP_NEAREST (default) will be used as minfilter 
        if mipmap is false: NEAREST (default) or LINEAR will be used as filter
      *normal_map*
        if a value is not None then the image file will be converted into a 
        normal map where Luminance value is proportional to height. The 
        value of nomral_map is used the scale the effect (see _normal_map())
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
    self.filter = filter
    self.normal_map = normal_map
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
    except Exception as _e:
      # possible for self to have already been deleted here, logger won't work!
      #print('Texture.__del__ failed with exception "{}" and OpenGL ES error={}'.format(
      #                  _e, opengles.glGetError()))
      pass

  def tex(self):
    """do the deferred opengl work and return texture"""
    self.load_opengl()
    return self._tex

  def _get_format_from_array(self, arr, req_format):
    """get GL format depending on channels in array. doesn't verify if #channels
    is consistent with the GL format"""
    channels = min(arr.shape[2], 4) if len(arr.shape) == 3 else 1
    if req_format == GL_ALPHA:
      return GL_ALPHA

    modes = [GL_LUMINANCE, GL_LUMINANCE_ALPHA, GL_RGB, GL_RGBA]
    return modes[channels - 1]

  def _img_to_array(self, im):
    """convert image to numpy.array.
    if i_format is specified and the image isn't in an adequate format, convert image.
    if no i_format is specified, choose the most adequate OpenGL format depending
    on image mode."""
    if self.i_format:
      # if format is specified, convert the image accordingly
      expected_mode = FORMAT_MODES[self.i_format]
      if im.mode != expected_mode:
        im = im.convert(expected_mode)
    elif im.mode not in ['RGBA', 'RGB', 'LA', 'L']:
        # other image types are converted to rgba
        im = im.convert('RGBA')

    if im.mode == 'LA':
      # convert LA image to array directly doesn't work
      # convert to rgba and strip rg channel - seems to be the fastest way
      rgba = im.convert('RGBA')
      arr = np.array(rgba)[:,:,2:4].astype(np.uint8)
    else:
      arr = np.array(im)

    if self.normal_map is not None:
      arr = self._normal_map(arr, self.normal_map)

    return arr

  def _load_disk(self):
    """overrides method of Loadable
    Pngfont, Font, Defocus and ShadowCaster inherit from Texture but
    don't do all this so have to override this
    """
    
    # If already loaded, abort
    if self._loaded:
      return

    if self.string_type == FILE and PIL_OK:
      s = self.file_string + ' '
      im = Image.open(self.file_string)
    elif self.string_type == PIL_IMAGE and PIL_OK:
      s = 'PIL.Image '
      im = self.file_string
    else:
      if self.string_type == NUMPY:
        s = 'numpy.ndarray '
        self.image = self.file_string
      else: # i.e. FILE but not PIL_OK
        ''' NB this has to be a compressed numpy array saved using something like
              im = np.array(Image.open('{}.png'.format(FNAME)))
              np.savez_compressed('{}'.format(FNAME), im)
        which will produce a file with extension .npz '''
        s = self.file_string + ' '
        self.image = np.load(self.file_string)['arr_0'] # has to be saved with default key

      self.iy, self.ix, _mode = self.image.shape
      self._tex = ctypes.c_uint()
      self._loaded = True
      return # skip the rest for numpy arrays - faster but no size checking

    # only do this if loading from disk or PIL image
    self.ix, self.iy = im.size
    s += '(%s)' % im.mode

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

    LOGGER.debug('Loading ...%s', s)

    if isinstance(self.flip, bool):
      # Old behaviour
      if self.flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    else:
      if self.flip & 1:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
      if self.flip & 2:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)

    #self.image = im.tostring('raw', RGBs) # TODO change to tobytes WHEN Pillow is default PIL in debian (jessie becomes current)
    self.image = self._img_to_array(im)
    self._tex = ctypes.c_uint()
    if self.string_type == FILE and 'fonts/' in self.file_string:
      self.im = im
      
    self._loaded = True

  def _load_opengl(self):
    """overrides method of Loadable"""
    try:
      opengles.glGenTextures(1, ctypes.byref(self._tex))
    except: # TODO windows throws exceptions just for this call!
      LOGGER.debug("[warning glGenTextures() on windows only!]")
    from pi3d.Display import Display
    if Display.INSTANCE is not None:
      Display.INSTANCE.textures_dict[str(self._tex)] = [self._tex, 0]
    self.update_ndarray()

  def _get_filter(self, t):
    f = self.filter
    if f is None:
      # default for mipmap is linear
      f = GL_LINEAR if self.mipmap else GL_NEAREST

    if t == GL_TEXTURE_MIN_FILTER and self.mipmap:
      # use mipmaps for min filter if requested requested
      f = GL_LINEAR_MIPMAP_NEAREST if f == GL_LINEAR else GL_NEAREST_MIPMAP_NEAREST

    return f

  def update_ndarray(self, new_array=None):
    """to allow numpy arrays to be patched in to textures without regenerating
    new glTextureBuffers i.e. for movie textures"""
    if new_array is not None:
      self.image = new_array
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    # set filters according to mipmap and filter request
    for t in [GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER]:
      opengles.glTexParameteri(GL_TEXTURE_2D, t, self._get_filter(t))

    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                             self.m_repeat)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                             self.m_repeat)

    iformat = self._get_format_from_array(self.image, self.i_format)
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, iformat, self.ix, self.iy, 0, iformat,
                          GL_UNSIGNED_BYTE,
                          self.image.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)))
    if opengles.glGetError() == GL_OUT_OF_MEMORY:
      LOGGER.critical('Out of GPU memory')
    #opengles.glEnable(GL_TEXTURE_2D) # invalid in OpenGLES 2
    if self.mipmap:
      opengles.glGenerateMipmap(GL_TEXTURE_2D)

    if self.free_after_load:
        self.image = None
        self._loaded = False

  def _normal_map(self, image, factor=1.0):
    ''' takes a numpy array and returns a normal map (as np array using
    lightness as height map. Argument factor can scale the effect
    '''
    if image.shape[2] > 2:
      gray = (image[:,:,:3] * [0.2989, 0.5870, 0.1140]).sum(axis=2) # grayscale
    else:
      gray = image[:,:,0]
    grdnt = np.gradient(gray) # a tuple of two arrays x and y gradients
    grdnt[0] = 128.0 - grdnt[0] * 0.5 * factor # range -256 to +256 converted to
    grdnt[1] = 128.0 + grdnt[1] * 0.5 * factor # 0-255. x swapped r to l
    z = np.maximum(0, 65025 - grdnt[0]**2 - grdnt[1]**2) # ensure +ve for sqrt
    n_map = np.zeros(image.shape[:2] + (3,), dtype=np.uint8) # RGB same size
    n_map[:,:,0] = grdnt[0].astype(np.uint8) # R
    n_map[:,:,1] = grdnt[1].astype(np.uint8) # G
    n_map[:,:,2] = (z**0.5).astype(np.uint8) # B
    return n_map


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
      'image': self.image,
      '_tex': self._tex,
      '_loaded': self._loaded,
      'opengl_loaded': False,
      'disk_loaded': self.disk_loaded,
      'm_repeat': self.m_repeat,
      'i_format': self.i_format,
      'free_after_load': self.free_after_load,
      'filter': self.filter
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
