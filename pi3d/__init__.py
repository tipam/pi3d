import ctypes

from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short

from pi3d.constants import *

# Open the libraries
bcm = ctypes.CDLL('libbcm_host.so')
opengles = ctypes.CDLL('libGLESv2.so')
openegl = ctypes.CDLL('libEGL.so')

def _ctypes_array(ct, x):
  return (ct * len(x))(*x)

def c_bytes(x):
  return _ctypes_array(ctypes.c_byte, x)

def c_ints(x):
  return _ctypes_array(ctypes.c_int, x)

def c_floats(x):
  return _ctypes_array(ctypes.c_float, x)

def c_shorts(x):
  return _ctypes_array(ctypes.c_short, x)
