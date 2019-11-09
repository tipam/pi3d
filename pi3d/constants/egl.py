"""
This module contains integer constants from a C header file named something
like egl.h.
"""
from ctypes import Structure, POINTER, c_void_p, c_int32, c_int
from pyxlib.x import Window

EGL_SUCCESS = 0x3000
EGL_NOT_INITIALIZED = 0x3001
EGL_BAD_ACCESS = 0x3002
EGL_BAD_ALLOC = 0x3003
EGL_BAD_ATTRIBUTE = 0x3004
EGL_BAD_CONFIG = 0x3005
EGL_BAD_CONTEXT = 0x3006
EGL_BAD_CURRENT_SURFACE = 0x3007
EGL_BAD_DISPLAY = 0x3008
EGL_BAD_MATCH = 0x3009
EGL_BAD_NATIVE_PIXMAP = 0x300A
EGL_BAD_NATIVE_WINDOW = 0x300B
EGL_BAD_PARAMETER = 0x300C
EGL_BAD_SURFACE = 0x300D
EGL_CONTEXT_LOST = 0x300E
EGL_BUFFER_SIZE = 0x3020
EGL_ALPHA_SIZE = 0x3021
EGL_BLUE_SIZE = 0x3022
EGL_GREEN_SIZE = 0x3023
EGL_RED_SIZE = 0x3024
EGL_DEPTH_SIZE = 0x3025
EGL_STENCIL_SIZE = 0x3026
EGL_CONFIG_CAVEAT = 0x3027
EGL_CONFIG_ID = 0x3028
EGL_LEVEL = 0x3029
EGL_MAX_PBUFFER_HEIGHT = 0x302A
EGL_MAX_PBUFFER_PIXELS = 0x302B
EGL_MAX_PBUFFER_WIDTH = 0x302C
EGL_NATIVE_RENDERABLE = 0x302D
EGL_NATIVE_VISUAL_ID = 0x302E
EGL_NATIVE_VISUAL_TYPE = 0x302F
EGL_SAMPLES = 0x3031
EGL_SAMPLE_BUFFERS = 0x3032
EGL_SURFACE_TYPE = 0x3033
EGL_TRANSPARENT_TYPE = 0x3034
EGL_TRANSPARENT_BLUE_VALUE = 0x3035
EGL_TRANSPARENT_GREEN_VALUE = 0x3036
EGL_TRANSPARENT_RED_VALUE = 0x3037
EGL_NONE = 0x3038
EGL_BIND_TO_TEXTURE_RGB = 0x3039
EGL_BIND_TO_TEXTURE_RGBA = 0x303A
EGL_MIN_SWAP_INTERVAL = 0x303B
EGL_MAX_SWAP_INTERVAL = 0x303C
EGL_LUMINANCE_SIZE = 0x303D
EGL_ALPHA_MASK_SIZE = 0x303E
EGL_COLOR_BUFFER_TYPE = 0x303F
EGL_RENDERABLE_TYPE = 0x3040
EGL_MATCH_NATIVE_PIXMAP = 0x3041
EGL_CONFORMANT = 0x3042
EGL_SLOW_CONFIG = 0x3050
EGL_NON_CONFORMANT_CONFIG = 0x3051
EGL_TRANSPARENT_RGB = 0x3052
EGL_RGB_BUFFER = 0x308E
EGL_LUMINANCE_BUFFER = 0x308F
EGL_NO_TEXTURE = 0x305C
EGL_TEXTURE_RGB = 0x305D
EGL_TEXTURE_RGBA = 0x305E
EGL_TEXTURE_2D = 0x305F
EGL_PBUFFER_BIT = 0x0001
EGL_PIXMAP_BIT = 0x0002
EGL_WINDOW_BIT = 0x0004
EGL_VG_COLORSPACE_LINEAR_BIT = 0x0020
EGL_VG_ALPHA_FORMAT_PRE_BIT = 0x0040
EGL_MULTISAMPLE_RESOLVE_BOX_BIT = 0x0200
EGL_SWAP_BEHAVIOR_PRESERVED_BIT = 0x0400
EGL_OPENGL_ES_BIT = 0x0001
EGL_OPENVG_BIT = 0x0002
EGL_OPENGL_ES2_BIT = 0x0004
EGL_OPENGL_BIT = 0x0008
EGL_VENDOR = 0x3053
EGL_VERSION = 0x3054
EGL_EXTENSIONS = 0x3055
EGL_CLIENT_APIS = 0x308D
EGL_HEIGHT = 0x3056
EGL_WIDTH = 0x3057
EGL_LARGEST_PBUFFER = 0x3058
EGL_TEXTURE_FORMAT = 0x3080
EGL_TEXTURE_TARGET = 0x3081
EGL_MIPMAP_TEXTURE = 0x3082
EGL_MIPMAP_LEVEL = 0x3083
EGL_RENDER_BUFFER = 0x3086
EGL_VG_COLORSPACE = 0x3087
EGL_VG_ALPHA_FORMAT = 0x3088
EGL_HORIZONTAL_RESOLUTION = 0x3090
EGL_VERTICAL_RESOLUTION = 0x3091
EGL_PIXEL_ASPECT_RATIO = 0x3092
EGL_SWAP_BEHAVIOR = 0x3093
EGL_MULTISAMPLE_RESOLVE = 0x3099
EGL_BACK_BUFFER = 0x3084
EGL_SINGLE_BUFFER = 0x3085
EGL_VG_COLORSPACE_sRGB = 0x3089
EGL_VG_COLORSPACE_LINEAR = 0x308A
EGL_VG_ALPHA_FORMAT_NONPRE = 0x308B
EGL_VG_ALPHA_FORMAT_PRE = 0x308C
EGL_BUFFER_PRESERVED = 0x3094
EGL_BUFFER_DESTROYED = 0x3095
EGL_OPENVG_IMAGE = 0x3096
EGL_CONTEXT_CLIENT_TYPE = 0x3097
EGL_CONTEXT_CLIENT_VERSION = 0x3098
EGL_MULTISAMPLE_RESOLVE_DEFAULT = 0x309A
EGL_MULTISAMPLE_RESOLVE_BOX = 0x309B
EGL_OPENGL_ES_API = 0x30A0
EGL_OPENVG_API = 0x30A1
EGL_OPENGL_API = 0x30A2
EGL_DRAW = 0x3059
EGL_READ = 0x305A
EGL_CORE_NATIVE_ENGINE = 0x305B

class _EGLDisplay(Structure):
    __slots__ = [
    ]
_EGLDisplay._fields_ = [
    ('_opaque_struct', c_int)
]
EGLDisplay = POINTER(_EGLDisplay)

class _EGLConfig(Structure):
    __slots__ = [
    ]
_EGLConfig._fields_ = [
    ('_opaque_struct', c_int)
]
EGLConfig = POINTER(_EGLConfig)

class _EGLSurface(Structure):
    __slots__ = [
    ]
_EGLSurface._fields_ = [
    ('_opaque_struct', c_int)
]
EGLSurface = POINTER(_EGLSurface)

class _EGLContext(Structure):
    __slots__ = [
    ]
_EGLContext._fields_ = [
    ('_opaque_struct', c_int)
]
EGLContext = POINTER(_EGLContext)

def set_egl_function_args(egl):
  '''
  typedef int EGLBoolean;
  typedef int32_t EGLint;
  typedef void *EGLDisplay;
  typedef void *EGLConfig;
  typedef void *EGLSurface;
  typedef void *EGLContext;
  '''

  #(_cs.EGLBoolean,_cs.EGLDisplay,arrays.GLintArray,arrays.GLvoidpArray,_cs.EGLint,arrays.GLintArray)
  egl.eglChooseConfig.argtypes = [EGLDisplay, POINTER(c_int32), c_void_p, c_int32, POINTER(c_int32)]
  egl.eglChooseConfig.restype = c_int #EGLBoolean

  #(_cs.EGLContext,_cs.EGLDisplay,_cs.EGLConfig,_cs.EGLContext,arrays.GLintArray)
  egl.eglCreateContext.argtypes = [EGLDisplay, EGLConfig, EGLContext, POINTER(c_int32)]
  egl.eglCreateContext.restype = EGLContext

  #(_cs.EGLSurface,_cs.EGLDisplay,_cs.EGLConfig,_cs.EGLNativeWindowType,arrays.GLintArray)
  egl.eglCreateWindowSurface.argtypes = [EGLDisplay, EGLConfig, Window, c_int32]
  egl.eglCreateWindowSurface.restype = EGLSurface

  #(_cs.EGLBoolean,_cs.EGLDisplay,_cs.EGLContext)
  egl.eglDestroyContext.argtypes = [EGLDisplay, EGLContext]
  egl.eglDestroySurface.argtypes = [EGLDisplay, EGLSurface]

  egl.eglGetCurrentSurface.argtypes = [c_int32]
  egl.eglGetCurrentSurface.restype = EGLSurface

  egl.eglGetDisplay.restype = EGLDisplay

  #(_cs.EGLBoolean,_cs.EGLDisplay,arrays.GLintArray,arrays.GLintArray)
  egl.eglInitialize.argtypes = [EGLDisplay, POINTER(c_int32), POINTER(c_int32)]

  #(_cs.EGLBoolean,_cs.EGLDisplay,_cs.EGLSurface,_cs.EGLSurface,_cs.EGLContext)
  egl.eglMakeCurrent.argtypes = [EGLDisplay, EGLSurface, EGLSurface, EGLContext]

  egl.eglSwapBuffers.argtypes = [EGLDisplay, EGLSurface]

  egl.eglQuerySurface.argtypes = [EGLDisplay, EGLSurface, c_int32, POINTER(c_int32)]

  egl.eglTerminate.argtypes = [EGLDisplay]
