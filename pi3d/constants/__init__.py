from __future__ import absolute_import, division, print_function, unicode_literals

"""
pi3d.constants contains constant values, mainly integers, from OpenGL ES 2.0.
"""

__version__ = '2.15'

STARTUP_MESSAGE = """

  Pi3D module - version {}

  Copyright (c) Tim Skillman, 2012-2016
  Copyright (c) Patrick Gaunt, 2012-2016
  Copyright (c) Tom Ritchford, 2012-2016

  Updates available from www.github.com/tipam/pi3d
""".format(__version__)

VERBOSE = False
# TODO: get rid of verbose in favor of logging.
KIVYDEBUG = False

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
EGL_FALSE = 0
DISPMANX_PROTECTION_NONE = 0
DISPMANX_FLAGS_ALPHA_PREMULT = 1 << 16

# Is this running on a raspberry pi?
PLATFORM_PI = 0
PLATFORM_OSX = 1
PLATFORM_WINDOWS = 2
PLATFORM_LINUX = 3
PLATFORM_ANDROID = 4

# Force pygame if possible
USE_PYGAME = False

#Display 
DISPLAY_CONFIG_DEFAULT = 0
DISPLAY_CONFIG_NO_RESIZE = 1
DISPLAY_CONFIG_NO_FRAME = 2
DISPLAY_CONFIG_FULLSCREEN = 4
DISPLAY_CONFIG_MAXIMIZED = 8

# PIL module available
try:
  from PIL import Image
  PIL_OK = True
except ImportError:
  PIL_OK = False

# Lastly, load the libraries.
def _load_library(name, dll_type="C"):
  """Try to load a shared library, report an error on failure."""
  if name:
    try:
      import ctypes
      if dll_type == "Win":
        return ctypes.WinDLL(name)
      else:
        return ctypes.CDLL(name)
    except:
      from pi3d.util import Log
      Log.logger(__name__).error("Couldn't load library %s", name)

def _linux():
  platform = PLATFORM_LINUX
  
  from ctypes.util import find_library
  from os import environ
  
  bcm_name = find_library('bcm_host')
  if bcm_name:
    platform = PLATFORM_PI
    bcm = _load_library(bcm_name)
  else:
    bcm = None

  if environ.get('ANDROID_APP_PATH'):
    platform = PLATFORM_ANDROID
    opengles = _load_library('/system/lib/libGLESv2.so')
    openegl = _load_library('/system/lib/libEGL.so')
  else:
    import os
    if os.path.isfile('/opt/vc/lib/libGLESv2.so'): # raspbian
      opengles = _load_library('/opt/vc/lib/libGLESv2.so')
      openegl = _load_library('/opt/vc/lib/libEGL.so')
    elif os.path.isfile('/usr/lib/libGLESv2.so'): # ubuntu MATE (but may catch others - monitor problems)
      opengles = _load_library('/usr/lib/libGLESv2.so')
      openegl = _load_library('/usr/lib/libEGL.so')
    else:
      opengles = _load_library(find_library('GLESv2')) # has to happen first
      openegl = _load_library(find_library('EGL')) # otherwise missing symbol on pi loading egl
  
  return platform, bcm, openegl, opengles # opengles now determined by platform

def _windows():
  global USE_PYGAME
  platform = PLATFORM_WINDOWS
  USE_PYGAME = True
  bcm = None
  """ NB You will need to copy the relevant dll files for ANGLE into the
  starting directory for the python file you are running. i.e. .../pi3d_demos
  In theory you can add the path to the `Path` variable but I couldn't get
  this to work.
  
  On 32 bit python:
  -----------------
  If you have chrome or firefox installed you should be able to find the
  required files in
  C:/Program Files (x86)/Google/Chrome/Application/42.0.2311.90/
  C:/Program Files (x86)/Mozill Firefox/ ... or equivalent latest location
  use the windows search
  You need to copy *ALL* these files
  1. libglesv2.dll
  2. libegl.dll
  3. d3dcompiler_47.dll (number will change with later releases - use highest)
  [4. mozglue.dll only for firefox]
  
  On 64 bit python:
  -----------------
  As above but you have to download 64 bit versions of the dll files from
  here http://github.com/paddywwoof/pi3d_windll
  """
  import ctypes.wintypes as wt
  from ctypes import POINTER, c_void_p, c_int32, c_uint, c_float
  opengles = _load_library("libglesv2.dll", "Win")
  openegl = _load_library("libegl.dll", "Win")

  openegl.eglGetDisplay.argtypes = [wt.HDC]
  openegl.eglGetDisplay.restype = c_void_p
  openegl.eglInitialize.argtypes = [c_void_p, POINTER(c_int32), POINTER(c_int32)]
  openegl.eglChooseConfig.argtypes = [c_void_p, c_void_p, c_void_p, c_int32, POINTER(c_int32)]
  openegl.eglCreateContext.argtypes = [c_void_p, c_void_p, c_int32, c_void_p]
  openegl.eglCreateContext.restype = c_void_p
  openegl.eglCreateWindowSurface.argtypes = [c_void_p, c_void_p, c_void_p, c_int32]
  openegl.eglCreateWindowSurface.restype = c_void_p
  openegl.eglMakeCurrent.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
  openegl.eglSwapBuffers.argtypes = [c_void_p, c_void_p]

  opengles.glUniformMatrix4fv.argtypes = [c_int32, c_int32, c_int32, c_void_p]

  return platform, bcm, openegl, opengles # opengles now determined by platform

def _darwin():
  pass

_PLATFORMS = {
  'linux': _linux,
  'darwin': _darwin,
  'windows': _windows
  }

def _detect_platform_and_load_libraries():
  import platform

  platform_name = platform.system().lower()
  loader = _PLATFORMS.get(platform_name, None)
  if not loader:
    raise Exception("Couldn't understand platform %s" % platform_name)

  return loader()

PLATFORM, bcm, openegl, opengles = _detect_platform_and_load_libraries()
