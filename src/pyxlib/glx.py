from ctypes import (CDLL, Structure, Union, c_char, c_short, c_int, c_int64, c_uint,
    c_long, c_ulong, CFUNCTYPE, POINTER)
from ctypes.util import find_library
from pi3d.constants import PLATFORM, PLATFORM_OSX
from .x import XID, VisualID, Colormap
from pyxlib import xlib

if PLATFORM == PLATFORM_OSX:
    glx_name = find_library('GL')
else:
    glx_name = find_library('GLX')
libGLX = CDLL(glx_name)

GLX_VERSION_1_1 = 1
GLX_VERSION_1_2 = 1
GLX_VERSION_1_3 = 1
GLX_VERSION_1_4 = 1

GLX_EXTENSION_NAME = "GLX"

'''/*
 * Tokens for glXChooseVisual and glXGetConfig:
 */'''
GLX_USE_GL = 1
GLX_BUFFER_SIZE = 2
GLX_LEVEL = 3
GLX_RGBA = 4
GLX_DOUBLEBUFFER = 5
GLX_STEREO = 6
GLX_AUX_BUFFERS = 7
GLX_RED_SIZE = 8
GLX_GREEN_SIZE = 9
GLX_BLUE_SIZE = 10
GLX_ALPHA_SIZE = 11
GLX_DEPTH_SIZE = 12
GLX_STENCIL_SIZE = 13
GLX_ACCUM_RED_SIZE = 14
GLX_ACCUM_GREEN_SIZE = 15
GLX_ACCUM_BLUE_SIZE = 16
GLX_ACCUM_ALPHA_SIZE = 17

'''/*
 * Error codes returned by glXGetConfig:
 */'''
GLX_BAD_SCREEN = 1
GLX_BAD_ATTRIBUTE = 2
GLX_NO_EXTENSION = 3
GLX_BAD_VISUAL = 4
GLX_BAD_CONTEXT = 5
GLX_BAD_VALUE = 6
GLX_BAD_ENUM = 7

'''/*
 * GLX 1.1 and later:
 */'''
GLX_VENDOR = 1
GLX_VERSION = 2
GLX_EXTENSIONS = 3

'''/*
* GLX 1.3 and later:
*/ '''
GLX_CONFIG_CAVEAT = 0x2
GLX_DONT_CARE = 0xFFFFFFFF
GLX_X_VISUAL_TYPE = 0x22
GLX_TRANSPARENT_TYPE = 0x23
GLX_TRANSPARENT_INDEX_VALUE = 0x24
GLX_TRANSPARENT_RED_VALUE = 0x25
GLX_TRANSPARENT_GREEN_VALUE = 0x26
GLX_TRANSPARENT_BLUE_VALUE = 0x27
GLX_TRANSPARENT_ALPHA_VALUE = 0x28
GLX_WINDOW_BIT = 0x00000001
GLX_PIXMAP_BIT = 0x00000002
GLX_PBUFFER_BIT = 0x00000004
GLX_AUX_BUFFERS_BIT = 0x00000010
GLX_FRONT_LEFT_BUFFER_BIT = 0x00000001
GLX_FRONT_RIGHT_BUFFER_BIT = 0x00000002
GLX_BACK_LEFT_BUFFER_BIT = 0x00000004
GLX_BACK_RIGHT_BUFFER_BIT = 0x00000008
GLX_DEPTH_BUFFER_BIT = 0x00000020
GLX_STENCIL_BUFFER_BIT = 0x00000040
GLX_ACCUM_BUFFER_BIT = 0x00000080
GLX_NONE = 0x8000
GLX_SLOW_CONFIG = 0x8001
GLX_TRUE_COLOR = 0x8002
GLX_DIRECT_COLOR = 0x8003
GLX_PSEUDO_COLOR = 0x8004
GLX_STATIC_COLOR = 0x8005
GLX_GRAY_SCALE = 0x8006
GLX_STATIC_GRAY = 0x8007
GLX_TRANSPARENT_RGB = 0x8008
GLX_TRANSPARENT_INDEX = 0x8009
GLX_VISUAL_ID = 0x800B
GLX_SCREEN = 0x800C
GLX_NON_CONFORMANT_CONFIG = 0x800D
GLX_DRAWABLE_TYPE = 0x8010
GLX_RENDER_TYPE = 0x8011
GLX_X_RENDERABLE = 0x8012
GLX_FBCONFIG_ID = 0x8013
GLX_RGBA_TYPE = 0x8014
GLX_COLOR_INDEX_TYPE = 0x8015
GLX_MAX_PBUFFER_WIDTH = 0x8016
GLX_MAX_PBUFFER_HEIGHT = 0x8017
GLX_MAX_PBUFFER_PIXELS = 0x8018
GLX_PRESERVED_CONTENTS = 0x801B
GLX_LARGEST_PBUFFER = 0x801C
GLX_WIDTH = 0x801D
GLX_HEIGHT = 0x801E
GLX_EVENT_MASK = 0x801F
GLX_DAMAGED = 0x8020
GLX_SAVED = 0x8021
GLX_WINDOW = 0x8022
GLX_PBUFFER = 0x8023
GLX_PBUFFER_HEIGHT = 0x8040
GLX_PBUFFER_WIDTH = 0x8041
GLX_RGBA_BIT = 0x00000001
GLX_COLOR_INDEX_BIT = 0x00000002
GLX_PBUFFER_CLOBBER_MASK = 0x08000000

'''/*
* GLX 1.4 and later:
*/ '''
GLX_SAMPLE_BUFFERS = 0x186a0 #/*100000*/
GLX_SAMPLES = 0x186a1 #/*100001*/


'''
typedef struct __GLXcontextRec *GLXContext;
typedef XID GLXPixmap;
typedef XID GLXDrawable;
/* GLX 1.3 and later */
typedef struct __GLXFBConfigRec *GLXFBConfig;
typedef XID GLXFBConfigID;
typedef XID GLXContextID;
typedef XID GLXWindow;
typedef XID GLXPbuffer;
'''

'''/*
** Events.
** __GLX_NUMBER_EVENTS is set to 17 to account for the BufferClobberSGIX
**  event - this helps initialization if the server supports the pbuffer
**  extension and the client doesn't.
*/ '''
GLX_PbufferClobber = 0
GLX_BufferSwapComplete = 1

__GLX_NUMBER_EVENTS = 17

class _GLXcontextRec(Structure):
    __slots__ = [
    ]
_GLXcontextRec._fields_ = [
    ('_opaque_struct', c_int)
]
GLXContext = POINTER(_GLXcontextRec)

GLXPixmap = XID
GLXDrawable = XID

class _GLXFBConfigRec(Structure):
    __slots__ = [
    ]
_GLXFBConfigRec._fields_ = [
    ('_opaque_struct', c_int)
]
GLXFBConfig = POINTER(_GLXFBConfigRec) 	# /usr/include/GL/glx.h:182

GLXFBConfigID = XID 	# /usr/include/GL/glx.h:183
GLXContextID = XID 	# /usr/include/GL/glx.h:184
GLXWindow = XID 	# /usr/include/GL/glx.h:185
GLXPbuffer = XID 	# /usr/include/GL/glx.h:186
GLXPbufferSGIX = XID
GLXVideoSourceSGIX = XID


'''class _anon_18(Structure):
    __slots__ = [
        'ext_data',
        'visualid',
        'class',
        'red_mask',
        'green_mask',
        'blue_mask',
        'bits_per_rgb',
        'map_entries',
    ]'''
'''class _XExtData(Structure):
    __slots__ = [
        'number',
        'next',
        'free_private',
        'private_data',
    ]
_XExtData._fields_ = [
    ('number', c_int),
    ('next', POINTER(_XExtData)),
    ('free_private', POINTER(CFUNCTYPE(c_int, POINTER(_XExtData)))),
    ('private_data', xlib.XPointer),
]
XExtData = _XExtData 	# /usr/include/X11/Xlib.h:163
'''
'''_anon_18._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('visualid', VisualID),
    ('class', c_int),
    ('red_mask', c_ulong),
    ('green_mask', c_ulong),
    ('blue_mask', c_ulong),
    ('bits_per_rgb', c_int),
    ('map_entries', c_int),
]
Visual = _anon_18 	# /usr/include/X11/Xlib.h:246'''

class _anon_103(Structure):
    __slots__ = [
        'visual',
        'visualid',
        'screen',
        'depth',
        'class',
        'red_mask',
        'green_mask',
        'blue_mask',
        'colormap_size',
        'bits_per_rgb',
    ]
_anon_103._fields_ = [
    ('visual', POINTER(xlib.Visual)),
    ('visualid', VisualID),
    ('screen', c_int),
    ('depth', c_int),
    ('class', c_int),
    ('red_mask', c_ulong),
    ('green_mask', c_ulong),
    ('blue_mask', c_ulong),
    ('colormap_size', c_int),
    ('bits_per_rgb', c_int),
]
XVisualInfo = _anon_103 	# /usr/include/X11/Xutil.h:294
'''
class _XDisplay(Structure):
    __slots__ = [
    ]
_XDisplay._fields_ = [
    ('_opaque_struct', c_int)
]
Display = _XDisplay 	# /usr/include/X11/Xlib.h:495
'''
#Pixmap = XID 	# /usr/include/X11/X.h:102
#Font = XID 	# /usr/include/X11/X.h:100
#Window = XID 	# /usr/include/X11/X.h:96
GLX_ARB_get_proc_address = 1 #constant.Constant( 'GLX_ARB_get_proc_address', 1 )
__GLXextFuncPtr = CFUNCTYPE(None) 	# /usr/include/GL/glx.h:330

# EXT_texture_from_pixmap (/usr/include/GL/glx.h:436)
class _anon_111(Structure):
    __slots__ = [
        'event_type',
        'draw_type',
        'serial',
        'send_event',
        'display',
        'drawable',
        'buffer_mask',
        'aux_buffer',
        'x',
        'y',
        'width',
        'height',
        'count',
    ]
_anon_111._fields_ = [
    ('event_type', c_int),
    ('draw_type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(xlib.Display)),
    ('drawable', GLXDrawable),
    ('buffer_mask', c_uint),
    ('aux_buffer', c_uint),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('count', c_int),
]
GLXPbufferClobberEvent = _anon_111 	# /usr/include/GL/glx.h:502
class _anon_112(Structure):
    __slots__ = [
        'type',
        'serial',
        'send_event',
        'display',
        'drawable',
        'event_type',
        'ust',
        'msc',
        'sbc',
    ]
_anon_112._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(xlib.Display)),
    ('drawable', GLXDrawable),
    ('event_type', c_int),
    ('ust', c_int64),
    ('msc', c_int64),
    ('sbc', c_int64),
]
GLXBufferSwapComplete = _anon_112 	# /usr/include/GL/glx.h:514
class _GLXEvent(Union):
    __slots__ = [
        'glxpbufferclobber',
        'glxbufferswapcomplete',
        'pad',
    ]
_GLXEvent._fields_ = [
    ('glxpbufferclobber', GLXPbufferClobberEvent),
    ('glxbufferswapcomplete', GLXBufferSwapComplete),
    ('pad', c_long * 24),
]
GLXEvent = _GLXEvent 	# /usr/include/GL/glx.h:520

class GLXHyperpipeConfigSGIX( Structure ):
    _fields_ = [
        ('pipeName', c_char * 80),
        ('channel',c_int),
        ('participationType',c_uint),
        ('timeSlice',c_int),
    ]

if glx_name:
    glXChooseFBConfig = libGLX.glXChooseFBConfig
    glXChooseFBConfig.restype = POINTER(GLXFBConfig)
    glXChooseFBConfig.argtypes = [POINTER(xlib.Display), c_int, POINTER(c_int), POINTER(c_int)]

    glXGetVisualFromFBConfig = libGLX.glXGetVisualFromFBConfig
    glXGetVisualFromFBConfig.restype = POINTER(XVisualInfo)
    glXGetVisualFromFBConfig.argtypes = [POINTER(xlib.Display), GLXFBConfig]

    glXCreateNewContext = libGLX.glXCreateNewContext
    glXCreateNewContext.restype = GLXContext
    glXCreateNewContext.argtypes = [POINTER(xlib.Display), GLXFBConfig, c_int, GLXContext, xlib.Bool]

    '''glXCreateContextAttribsARB = libGLX.glXCreateContextAttribsARB
    glXCreateContextAttribsARB.restype = GLXContext
    glXCreateContextAttribsARB.argtypes = [POINTER(xlib.Display), GLXFBConfig, GLXContext, xlib.Bool,
                                        POINTER(c_int)]'''

    glXQueryExtension = libGLX.glXQueryExtension
    glXQueryExtension.restype = xlib.Bool
    glXQueryExtension.argtypes = [POINTER(xlib.Display), POINTER(c_int), POINTER(c_int)]

    glXMakeContextCurrent = libGLX.glXMakeContextCurrent
    glXMakeContextCurrent.restype = xlib.Bool
    glXMakeContextCurrent.argtypes = [POINTER(xlib.Display), GLXDrawable, GLXDrawable, GLXContext]

    glXSwapBuffers = libGLX.glXSwapBuffers
    glXSwapBuffers.restype = None
    glXSwapBuffers.argtypes = [POINTER(xlib.Display), GLXDrawable]

#####################################
####### Xrender extension ###########
xrender_name = find_library('Xrender')
libXrender = CDLL(xrender_name)

PictFormat = c_ulong

class _XRenderDirectFormat(Structure):
    __slots__ = [
	    'red',
	    'redMask',
	    'green',
	    'greenMask',
	    'blue',
	    'blueMask',
	    'alpha',
	    'alphaMask',
	]
_XRenderDirectFormat._fields_= [
	    ('red', c_short),
	    ('redMask', c_short),
	    ('green', c_short),
	    ('greenMask', c_short),
	    ('blue', c_short),
	    ('blueMask', c_short),
	    ('alpha', c_short),
	    ('alphaMask', c_short),
	]
XRenderDirectFormat = _XRenderDirectFormat

class _XRenderPictFormat(Structure):
        __slots__ = [
        'id',
        'type',
        'depth',
        'direct',
        'colormap',
    ]
_XRenderPictFormat._fields_ = [
    ('id', PictFormat),
    ('type', c_int),
    ('depth', c_int),
    ('direct', XRenderDirectFormat),
    ('colormap', Colormap),
]
XRenderPictFormat = _XRenderPictFormat

if xrender_name:
    XRenderFindVisualFormat = libXrender.XRenderFindVisualFormat
    XRenderFindVisualFormat.restype = POINTER(XRenderPictFormat)
    XRenderFindVisualFormat.argtypes = [POINTER(xlib.Display), POINTER(xlib.Visual)]
