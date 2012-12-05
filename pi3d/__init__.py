import ctypes

from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short
from ctypes import c_char

from pi3d.constants import *
from pi3d.util import Log

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

