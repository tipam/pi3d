import ctypes
import math

from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short

from pi3d.constants import *

# Open the libraries
bcm = ctypes.CDLL('libbcm_host.so')
opengles = ctypes.CDLL('libGLESv2.so')
openegl = ctypes.CDLL('libEGL.so')

def ctypes_array(ct, x):
  return (ct * len(x))(*x)

def c_bytes(x):
  return ctypes_array(c_byte, x)

def c_ints(x):
  return ctypes_array(c_int, x)

def c_floats(x):
  return ctypes_array(c_float, x)

def c_shorts(x):
  return ctypes_array(c_short, x)

# TODO: not exact sure what this does but we do it a lot.
def texture_min_mag():
  for f in [GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER]:
    opengles.glTexParameterf(GL_TEXTURE_2D, f, c_float(GL_LINEAR))

def sqsum(*args):
  return sum(x * x for x in args)

def magnitude(*args):
  return math.sqrt(sqsum(*args))

def from_polar(direction=0.0, magnitude=1.0):
  return from_polar_rad(math.radians(direction), magnitude)

def from_polar_rad(direction=0.0, magnitude=1.0):
  return magnitude * math.cos(direction), magnitude * math.sin(direction)

def rotatef(angle, x, y, z):
  if angle:
    opengles.glRotatef(c_float(angle), c_float(x), c_float(y), c_float(z))

def translatef(x, y, z):
  opengles.glTranslatef(c_float(x), c_float(y), c_float(z))

def scalef(sx, sy, sz):
  opengles.glScalef(c_float(sx), c_float(sy), c_float(sz))

def load_identity():
  opengles.glLoadIdentity()
