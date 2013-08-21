from __future__ import absolute_import, division, print_function, unicode_literals

"""
pi3d.constants contains constant values, mainly integers, from OpenGL ES 2.0.
"""
import subprocess

VERSION = '1.0'

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


def _linux(platform):
  gles_name = ''
  egl_name = ''

  # run command and return
  def _run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

  COMMAND = ['ldconfig', '-p']

  for line in _run_command(COMMAND):
    if b'libbcm_host.so' in line:
      platform = PLATFORM_PI
    elif b'libGLESv2.so' in line:
      gles_name = line.split()[0]
    elif b'libEGL.so' in line:
      egl_name = line.split()[0]

  bcm_name = None
  #May need to use system() and linux_distribution()
  bcm_name = platform == PLATFORM_PI and 'libbcm_host.so'

  opengles = _load_library(gles_name)
  openegl = _load_library(egl_name)
  return platform, bcm_name, gles_name, egl_name

def _detect_platform_and_load_libraries():
  platform, bcm_name, gles_name, egl_name = _linux(PLATFORM_LINUX)
  bcm = _load_library(bcm_name)
  opengles = _load_library(gles_name)
  openegl = _load_library(egl_name)
  return platform, bcm, opengles, openegl

PLATFORM, bcm, opengles, openegl = _detect_platform_and_load_libraries()
