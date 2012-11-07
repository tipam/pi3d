__version__ = '0.06'

STARTUP_MESSAGE = """
Pi3D module - version %(version)s
Copyright (c) Tim Skillman, 2012
Copyright (c) Tom Swirly, 2012
Updates available from www.github.com/rec/pi3d
Screen size %(width)d, %(height)d.
"""

VERBOSE = True

# Pick up our constants extracted from the header files with prepare_constants.py
from constants.egl import *
from constants.gl2 import *
from constants.gl2ext import *
from constants.gl import *

# Define some extra constants that the automatic extraction misses
EGL_DEFAULT_DISPLAY = 0
EGL_NO_CONTEXT = 0
EGL_NO_DISPLAY = 0
EGL_NO_SURFACE = 0
DISPMANX_PROTECTION_NONE = 0

