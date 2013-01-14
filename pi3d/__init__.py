from echomesh.util import Log

from pi3d.constants import *

LOGGER = Log.logger(__name__)

def c_bytes(x):
  from ctypes import c_byte
  return (c_byte * len(x))(*x)

def c_chars(x):
  from ctypes import c_char
  return (c_char * len(x))(*x)

def c_floats(x):
  from ctypes import c_float
  return (c_float * len(x))(*x)

def c_ints(x):
  from ctypes import c_int
  return (c_int * len(x))(*x)

def c_shorts(x):
  from ctypes import c_short
  return (c_short * len(x))(*x)

def _load_library(name):
  """Try to load a shared library, report an error on failure."""
  try:
    import ctypes
    return ctypes.CDLL('lib%s.so' % name)
  except:
    from echomesh.util import Log
    Log.logger(__name__).error("Couldn't load library %s" % name)

bcm = _load_library('bcm_host')
opengles = _load_library('GLESv2')
openegl = _load_library('EGL')

