# Setup EGL display
# Based on code by Peter de Rivaz and others

import ctypes, math, Image
# Pick up our constants extracted from the header files with prepare_constants.py
from egl import *
from gl2 import *
from gl2ext import *
from gl import *

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
eglbyte = ctypes.c_byte


		
def eglbytes(L):
    return (eglbyte*len(L))(*L)

def eglints(L):
    return (eglint*len(L))(*L)

def eglfloats(L):
    return (eglfloat*len(L))(*L)
                
def check(e):
    """Checks that error is zero"""
    if e==0: return
    if verbose:
        print 'Error code',hex(e&0xffffffff)
    raise ValueError


class glDisplay(object):

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
	
    def create(self,x,y,w,h):
	
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
	r = openegl.eglChooseConfig(self.display, ctypes.byref(attribute_list), ctypes.byref(config), 1, ctypes.byref(numconfig));
   
	if verbose: print 'numconfig=',numconfig

        self.context = openegl.eglCreateContext(self.display, config, EGL_NO_CONTEXT, 0 ) 
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
	
	#Create viewport
        opengles.glViewport (0, 0, w, h)
        #
	opengles.glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
	opengles.glEnable(GL_CULL_FACE)	
        opengles.glShadeModel(GL_FLAT);
	
	#Setup perspective view
	opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        nearp=1.0
        farp=500.0
        hht = nearp * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = hht * w / h
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(nearp), eglfloat(farp))
	opengles.glMatrixMode(GL_MODELVIEW)
	
	self.active = True
	
	
    def destroy(self):
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
    
    def clear(self):
	opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	
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
		self.rotx=0
		self.roty=0
		self.rotz=0
		
		#cuboid data

		self.cube_vertices = eglbytes(( -1,1,1, 1,1,1, 1,-1,1, -1,-1,1, -1,1,-1, 1,1,-1, 1,-1,-1, -1,-1,-1));
		#self.cube_triangles = eglbytes(( 1,0,3, 1,3,2, 2,6,5, 2,5,1, 7,4,5, 7,5,6, 0,4,7, 0,7,3, 5,4,0, 5,0,1, 3,7,6, 3,6,2));
		self.cube_colours = eglbytes(( 0,0,255,255, 0,0,0,255, 0,255,0,255, 0,255,0,255, 0,0,255,255, 255,0,0,255, 255,0,0,255, 0,0,0,255 ));
		self.cube_fan1 = eglbytes(( 1,0,3, 1,3,2, 1,2,6, 1,6,5, 1,5,4, 1,4,0 ));
		self.cube_fan2 = eglbytes(( 7,4,5, 7,5,6, 7,6,2, 7,2,3, 7,3,0, 7,0,4 ));

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
		
	def rotateToX(self,v):
		self.rotx = v
		
	def rotateToY(self,v):
		self.roty = v
		
	def rotateToZ(self,v):
		self.rotz = v
		
	def rotateIncX(self,v):
		self.rotx += v
		
	def rotateIncY(self,v):
		self.roty += v
		
	def rotateIncZ(self,v):
		self.rotz += v
		
	def draw(self):
		opengles.glEnableClientState(GL_VERTEX_ARRAY)
		opengles.glVertexPointer( 3, GL_BYTE, 0, self.cube_vertices);

		#opengles.glEnableClientState(GL_COLOR_ARRAY)
		#opengles.glColorPointer( 4, GL_UNSIGNED_BYTE, 0, self.cube_colours);

		opengles.glLoadIdentity()
		opengles.glTranslatef(eglfloat(self.x), eglfloat(self.y), eglfloat(self.z))
		
		if self.rotx <> 0:  opengles.glRotatef(eglfloat(self.roty),eglfloat(1), eglfloat(0), eglfloat(0))
		if self.roty <> 0:  opengles.glRotatef(eglfloat(self.roty),eglfloat(0), eglfloat(1), eglfloat(0))
		if self.rotz <> 0:  opengles.glRotatef(eglfloat(self.rotz),eglfloat(0), eglfloat(0), eglfloat(1))
		
		opengles.glScalef(eglfloat(self.width),eglfloat(self.height),eglfloat(self.depth))
		#opengles.glDrawElements( GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, self.triangles)
	
		opengles.glDrawElements( GL_TRIANGLE_FAN, 18, GL_UNSIGNED_BYTE, self.cube_fan1)
		opengles.glDrawElements( GL_TRIANGLE_FAN, 18, GL_UNSIGNED_BYTE, self.cube_fan2)

class create_plane(object):
	
	def __init__(self,w,h):
		self.width = w
		self.height = h
		self.x=0
		self.y=0
		self.z=0
		self.rotx=0
		self.roty=0
		self.rotz=0
		
		#plane data

		self.plane_vertices = eglbytes(( -1,1,1, 1,1,1, 1,-1,1, -1,-1,1 ));
		self.plane_fan = eglbytes(( 1,0,3, 1,3,2 ));
		self.tex_coords = eglbytes((0,0, 255,0, 255,255, 0,255));

	#this should all be done with matrices!! ... just for testing ...
	
	def scale(self,sw,sh):
		self.width = self.width * sw
		self.height = self.height * sh

	def position(self,xp,yp,zp):
		self.x=xp
		self.y=yp
		self.z=zp
	
	def translate(self,tx,ty,tz):
		self.x=self.x+tx
		self.y=self.y+ty
		self.z=self.z+tz
		
	def rotateToX(self,v):
		self.rotx = v
		
	def rotateToY(self,v):
		self.roty = v
		
	def rotateToZ(self,v):
		self.rotz = v
		
	def rotateIncX(self,v):
		self.rotx += v
		
	def rotateIncY(self,v):
		self.roty += v
		
	def rotateIncZ(self,v):
		self.rotz += v
		
	def draw(self,texID):
		opengles.glEnableClientState(GL_VERTEX_ARRAY)
		opengles.glVertexPointer( 3, GL_BYTE, 0, self.plane_vertices);

		if texID > 0:
		    opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		    opengles.glTexCoordPointer(2,GL_BYTE,0,self.tex_coords)
		    opengles.glBindTexture(GL_TEXTURE_2D,texID)
		    opengles.glEnable(GL_TEXTURE_2D)
		    
		opengles.glLoadIdentity()
		opengles.glTranslatef(eglfloat(self.x), eglfloat(self.y), eglfloat(self.z))
		
		if self.rotx <> 0:  opengles.glRotatef(eglfloat(self.roty),eglfloat(1), eglfloat(0), eglfloat(0))
		if self.roty <> 0:  opengles.glRotatef(eglfloat(self.roty),eglfloat(0), eglfloat(1), eglfloat(0))
		if self.rotz <> 0:  opengles.glRotatef(eglfloat(self.rotz),eglfloat(0), eglfloat(0), eglfloat(1))
		
		opengles.glScalef(eglfloat(self.width),eglfloat(self.height),1)
	
		opengles.glDrawElements( GL_TRIANGLE_FAN, 6, GL_UNSIGNED_BYTE, self.plane_fan)
		
		if texID > 0:
		    opengles.glBindTexture(GL_TEXTURE_2D,0)
				
class camera(object):
    
    def __init__(self,x,y,z,rx,ry,rz):
	self.x=x
	self.y=y
	self.z=z
	self.rotx=rx
	self.roty=ry
	self.rotz=rz
	
    def orthographic(self,w,h,zoom,near,far):
	opengles.glMatrixMode(GL_PROJECTION)
	opengles.glLoadIdentity()
	opengles.glOrtho(-w/zoom, w/zoom, -h/zoom, h/zoom, near, far)

    def perspective(self,w,h,zoom,nearp,farp):
	opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        hht = nearp * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = hht * w / h
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(nearp), eglfloat(farp))
	
    def position(self,x,y,z,rx,ry,rz):
	self.x=x
	self.y=y
	self.z=z
	self.rotx=rx
	self.roty=ry
	self.rotz=rz
	
	opengles.glMatrixMode(GL_MODELVIEW)
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))
	
	if rx <> 0:  opengles.glRotatef(eglfloat(ry),eglfloat(1), eglfloat(0), eglfloat(0))
	if ry <> 0:  opengles.glRotatef(eglfloat(ry),eglfloat(0), eglfloat(1), eglfloat(0))
	if rz <> 0:  opengles.glRotatef(eglfloat(rz),eglfloat(0), eglfloat(0), eglfloat(1))
	
    def pos(self,x,y,z,rx,ry,rz):
	position(x,y,z,self.rotx,self.roty,self.rotz)
	
class load_texture(object):
    
    def __init__(self,fileString):
	
	im= Image.open(fileString)
	self.iy = im.size[0]
	self.ix = im.size[1]
	image = im.convert("RGB").tostring("raw","RGB")
	self.texID = eglint()
	opengles.glGenTextures(1,ctypes.byref(self.texID))
	opengles.glBindTexture(GL_TEXTURE_2D,self.texID)
	opengles.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,self.ix,self.iy,0,GL_RGB,GL_UNSIGNED_BYTE, image)
	
    def check(self):
	e=opengles.glGetError()
	if e:
	    print hex(e)
	    raise ValueError
	    
