import ctypes

from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short

from pi3d.constants import *
from pi3d.util import Log

LOGGER = Log.logger(__name__)

def _ctypes_array(ct, x):
  return (ct * len(x))(*x)

def c_bytes(x):
  return _ctypes_array(c_byte, x)

def c_chars(x):
  return _ctypes_array(c_char, x)

def c_ints(x):
  return _ctypes_array(c_int, x)

def c_floats(x):
  return _ctypes_array(c_float, x)

def c_shorts(x):
  return _ctypes_array(c_short, x)

def call(ctype, f, *args):
  return f(*(ctype(a) for a in args))

def call_float(f, *args):
  return f(*(c_float(a) for a in args))

def _load_library(name):
  """Try to load a shared library, report an error on failure."""
  try:
    return ctypes.CDLL('lib%s.so' % name)
  except:
    LOGGER.error("Couldn't load library %s" % name)

bcm = _load_library('bcm_host')
opengles = _load_library('GLESv2')
openegl = _load_library('EGL')

