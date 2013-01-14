from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short
from ctypes import c_char

from echomesh.util import Log

from pi3d.constants import *

LOGGER = Log.logger(__name__)

def c_bytes(x):
  return (c_byte * len(x))(*x)

def c_chars(x):
  return (c_char * len(x))(*x)

def c_ints(x):
  return (c_int * len(x))(*x)

def c_floats(x):
  return (c_float * len(x))(*x)

def c_shorts(x):
  return (c_short * len(x))(*x)

def _load_library(name):
  """Try to load a shared library, report an error on failure."""
  try:
    import ctypes
    return ctypes.CDLL('lib%s.so' % name)
  except:
    import echomesh.util.Log
    Log.logger(__name__).error("Couldn't load library %s" % name)

bcm = _load_library('bcm_host')
opengles = _load_library('GLESv2')
openegl = _load_library('EGL')

