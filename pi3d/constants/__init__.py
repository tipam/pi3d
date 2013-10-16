from __future__ import absolute_import, division, print_function, unicode_literals

"""
pi3d.constants contains constant values, mainly integers, from OpenGL ES 2.0.
"""

VERSION = '1.4'

STARTUP_MESSAGE = """

  Pi3D module - version %(version)s

  Copyright (c) Tim Skillman, 2012-2013
  Copyright (c) Patrick Gaunt, 2012-2013
  Copyright (c) Tom Ritchford, 2012-2013

  Updates available from www.github.com/tipam/pi3d
""" % {'version': VERSION}

VERBOSE = False
# TODO: get rid of verbose in favor of logging.

# Pick up our constants extracted from the header files with prepare_constants.py
from pi3d.constants.egl import *
from pi3d.constants.gl2 import *
from pi3d.constants.gl2ext import *
from pi3d.constants.gl import *

# Define some extra constants that the automatic extraction misses.
EGL_DEFAULT_DISPLAY = 0
EGL_NO_CONTEXT = 0
EGL_NO_DISPLAY = 0
EGL_NO_SURFACE = 0
DISPMANX_PROTECTION_NONE = 0

# Is this running on a raspberry pi?
PLATFORM_PI = 0
PLATFORM_OSX = 1
PLATFORM_WINDOWS = 2
PLATFORM_LINUX = 3

# Lastly, load the libraries.
def _load_library(name):
  """Try to load a shared library, report an error on failure."""
  if name:
    try:
      import ctypes
      return ctypes.CDLL(name)
    except:
      from pi3d.util import Log
      Log.logger(__name__).error("Couldn't load library %s", name)

def _linux():
  platform = PLATFORM_LINUX
  
  from ctypes.util import find_library
  
  bcm_name = find_library('bcm_host')
  if bcm_name:
    platform = PLATFORM_PI
  gles_name = find_library('GLESv2')
  egl_name = find_library('EGL')

  return platform, bcm_name, gles_name, egl_name

def _darwin():
  pass

_PLATFORMS = {
  'linux': _linux,
  'darwin': _darwin
  }

def _detect_platform_and_load_libraries():
  import platform

  platform_name = platform.system().lower()
  loader = _PLATFORMS.get(platform_name, None)
  if not loader:
    raise Exception("Couldn't understand platform %s" % platform_name)

  plat, bcm_name, gles_name, egl_name = loader()
  bcm = _load_library(bcm_name)
  opengles = _load_library(gles_name)
  openegl = _load_library(egl_name)
  return plat, bcm, opengles, openegl

PLATFORM, bcm, opengles, openegl = _detect_platform_and_load_libraries()
