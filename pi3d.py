# Setup EGL display
# Based on code by Peter de Rivaz and others

import ctypes
# Pick up our constants extracted from the header files with prepare_constants.py
from egl import *
from gl2 import *
from gl2ext import *

# Define verbose=True to get debug messages
verbose = True

# Define some extra constants that the automatic extraction misses
EGL_DEFAULT_DISPLAY = 0
EGL_NO_CONTEXT = 0
EGL_NO_DISPLAY = 0
EGL_NO_SURFACE = 0
DISPMANX_PROTECTION_NONE = 0

# Open the libraries
bcm = ctypes.CDLL('libbcm_host.so')
opengles = ctypes.CDLL('libGLESv2.so')
openegl = ctypes.CDLL('libEGL.so')

eglint = ctypes.c_int
eglshort = ctypes.c_short
eglfloat = ctypes.c_float

def eglints(L):
    """Converts a tuple to an array of eglints (would a pointer return be better?)"""
    return (eglint*len(L))(*L)

def eglfloats(L):
    return (eglfloat*len(L))(*L)
                
def check(e):
    """Checks that error is zero"""
    if e==0: return
    if verbose:
        print 'Error code',hex(e&0xffffffff)
    raise ValueError

class init_display(object):

    def __init__(self):
        """Opens up the OpenGL library and prepares a window for display"""
        b = bcm.bcm_host_init()
	
	#Get the width and height of the screen
        width = eglint() 
        height = eglint() 
        s = bcm.graphics_get_display_size(0,ctypes.byref(width),ctypes.byref(height))
        assert s>=0
        print width, height

        self.max_width = width
        self.max_height = height
	
	
    def make_display(self,x,y,w,h):
	
        self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
	assert self.display != EGL_NO_DISPLAY
	
        r = openegl.eglInitialize(self.display,0,0)
	#assert r == EGL_FALSE
	
        attribute_list = eglints(     (EGL_RED_SIZE, 8,
                                      EGL_GREEN_SIZE, 8,
                                      EGL_BLUE_SIZE, 8,
                                      EGL_ALPHA_SIZE, 8,
                                      EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
                                      EGL_NONE) )
        numconfig = eglint()
        config = ctypes.c_void_p()
        r = openegl.eglChooseConfig(self.display,
                                     ctypes.byref(attribute_list),
                                     ctypes.byref(config), 1,
                                     ctypes.byref(numconfig));
                                     
        r = openegl.eglBindAPI(EGL_OPENGL_ES_API)

        if verbose:
            print 'numconfig=',numconfig

        context_attribs = eglints( (EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE) )
        self.context = openegl.eglCreateContext(self.display, config,
                                        EGL_NO_CONTEXT,
                                        ctypes.byref(context_attribs))
                                        
        assert self.context != EGL_NO_CONTEXT
        
        
        
        #Set the viewport position and size

        dst_rect = eglints( (x,y,w,h) ) #width.value,height.value) )
        src_rect = eglints( (x,y,w<<16, h<<16) ) #width.value<<16, height.value<<16) )

        self.dispman_display = bcm.vc_dispmanx_display_open( 0 ) #LCD setting
        self.dispman_update = bcm.vc_dispmanx_update_start( 0 )
        self.dispman_element = bcm.vc_dispmanx_element_add ( self.dispman_update, self.dispman_display,
                                  0, ctypes.byref(dst_rect), 0,
                                  ctypes.byref(src_rect),
                                  DISPMANX_PROTECTION_NONE,
                                  0 , 0, 0)

        nativewindow = eglints((self.dispman_element,w,h));
        bcm.vc_dispmanx_update_submit_sync( self.dispman_update )
    
        nw_p = ctypes.pointer(nativewindow)
        self.nw_p = nw_p
        
        self.surface = openegl.eglCreateWindowSurface( self.display, config, nw_p, 0)
        assert self.surface != EGL_NO_SURFACE
        
        r = openegl.eglMakeCurrent(self.display, self.surface, self.surface, self.context)
        assert r
	
	self.active = True
	
	
    def destroy_display(self):
	if self.active:
	    openegl.eglSwapBuffers(self.display, self.surface);
	    openegl.eglMakeCurrent(self.display, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT)
	    openegl.eglDestroySurface(self.display, self.surface)
	    openegl.eglDestroyContext(self.display, self.context)
	    openegl.eglTerminate(self.display)
	    bcm.vc_dispmanx_display_close(self.dispman_display)
	    bcm.vc_dispmanx_element_remove(self.dispman_update,self.dispman_element)
	    self.active = False	
	
        
    def swap_buffers(self):
	openegl.eglSwapBuffers(self.display, self.surface);
	
    def setBackColour(self,r,g,b,a):
	self.backColour=(r,g,b,a)
	opengles.glClearColor ( eglfloat(r), eglfloat(g), eglfloat(b), eglfloat(a) );


class create_cuboid(object):
	
	def __init__(self,w,d,h):
		self.width = w
		self.depth = d
		self.height = h
		self.x=0
		self.y=0
		self.z=0
		
	#this should all be done with matrices!! ... just for testing ...
	
	def scale(self,sw,sd,sh):
		self.width = self.width * sw
		self.depth = self.depth * sd
		self.height = self.height * sh

	def position(self,xp,yp,zp):
		self.x=xp
		self.y=yp
		self.z=zp
	
	def translate(self,tx,ty,tz):
		self.x=self.x+tx
		self.y=self.y+ty
		self.z=self.z+tz
		
