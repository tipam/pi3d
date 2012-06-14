# pi3D module
# ===========
# By Tim Skillman & Peter de Rivaz, Copyright (c) 2012
# www.github.com/tipam/pi3d
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import ctypes, math, Image, curses
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
eglchar = ctypes.c_char

def eglbytes(L): return (eglbyte*len(L))(*L)
def eglchars(L): return (eglchar*len(L))(*L)
def eglints(L): return (eglint*len(L))(*L)
def eglfloats(L): return (eglfloat*len(L))(*L)
                
def check(e):
    """Checks that error is zero"""
    if e==0: return
    if verbose:
        print 'Error code',hex(e&0xffffffff)
    raise ValueError

#load a texture specifying RGB or RGBA
def load_tex(fileString,RGBv,RGBs):
	print "Loading ...",fileString
	im = Image.open(fileString)
	iy = im.size[0]
	ix = im.size[1]

	if (ix<>8 and ix<>16 and ix<>32 and ix<>64 and ix<>128 and ix<>256 and ix<>512 and ix<>1024) or ix<>iy:
	    im = im.resize((256,256),Image.ANTIALIAS)
	    iy = im.size[0]
	    ix = im.size[1]
	    print "Resizing to :",ix,iy
	    
	image = eglchars(im.convert(RGBs).tostring("raw",RGBs))
	tex=eglint()
        opengles.glGenTextures(1,ctypes.byref(tex))
	opengles.glBindTexture(GL_TEXTURE_2D,tex)
	opengles.glTexImage2D(GL_TEXTURE_2D,0,RGBv,ix,iy,0,RGBv,GL_UNSIGNED_BYTE, ctypes.byref(image))
	return (ix,iy,tex)

#turn texture on before drawing arrays
def texture_on(tex, tex_coords):
	opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
	opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
	opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
	opengles.glTexCoordPointer(2,GL_BYTE,0,ctypes.byref(tex_coords))
	opengles.glBindTexture(GL_TEXTURE_2D,tex.tex)
	opengles.glEnable(GL_TEXTURE_2D)
	if tex.alpha:
	    opengles.glDisable(GL_DEPTH_TEST)
	    opengles.glEnable(GL_BLEND)
	    opengles.glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

#turn texture off after drawing arrays
def texture_off():
	opengles.glDisable(GL_TEXTURE_2D)
	opengles.glDisable(GL_BLEND)
	opengles.glEnable(GL_DEPTH_TEST)
		    
#position, rotate and scale an object
def transform(x,y,z,rotx,roty,rotz,sx,sy,sz):
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))		
	if rotx <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(1), eglfloat(0), eglfloat(0))
	if roty <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(0), eglfloat(1), eglfloat(0))
	if rotz <> 0: opengles.glRotatef(eglfloat(rotz),eglfloat(0), eglfloat(0), eglfloat(1))
	opengles.glScalef(eglfloat(sx),eglfloat(sy),eglfloat(sz))

rect_normals = eglbytes(( 0,0,1, 0,0,1, 0,0,1, 0,0,1 ))
rect_tex_coords = eglbytes((0,0, 255,0, 255,255, 0,255))
rect_vertsTL = eglbytes(( 1,0,0, 0,0,0, 0,1,0, 1,1,0 ))
rect_vertsCT = eglbytes(( -1,-1,0, 1,-1,0, 1,1,0, -1,1,0 ))
rect_triangles = eglbytes(( 1,0,3, 1,3,2 ))

def rectangle(tex,x,y,w,h,r=0.0,z=-1.0):
	opengles.glNormalPointer( GL_BYTE, 0, rect_normals);
	opengles.glVertexPointer( 3, GL_BYTE, 0, rect_vertsTL);
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))
	opengles.glScalef(eglfloat(w), eglfloat(h), eglfloat(1))
	if r <> 0.0: opengles.glRotatef(eglfloat(r),eglfloat(0), eglfloat(0), eglfloat(1))
	if tex > 0: texture_on(tex,rect_tex_coords)
	opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, rect_triangles)
	if tex > 0: texture_off()

def sprite(tex,x,y,z=-10.0,w=1.0,h=1.0,r=0.0):
	opengles.glNormalPointer( GL_BYTE, 0, rect_normals);
	opengles.glVertexPointer( 3, GL_BYTE, 0, rect_vertsCT);
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))
	opengles.glScalef(eglfloat(w), eglfloat(h), eglfloat(1))
	if r <> 0.0: opengles.glRotatef(eglfloat(r),eglfloat(0), eglfloat(0), eglfloat(1))
	if tex > 0: texture_on(tex,rect_tex_coords)
	opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, rect_triangles)
	if tex > 0: texture_off()

class key():
    
    def __init__(self):
	self.key = curses.initscr()
	self.key.nodelay(1)

    def read(self):
	return (self.key.getch())

#=====================================================================================================================================================================================	
# Setup EGL display
    
class glDisplay(object):

    def __init__(self):
        """Opens up the OpenGL library and prepares a window for display"""
        b = bcm.bcm_host_init()
	
	#Get the width and height of the screen
        width = eglint() 
        height = eglint() 
        s = bcm.graphics_get_display_size(0,ctypes.byref(width),ctypes.byref(height))
        assert s>=0

        self.max_width = width.value
        self.max_height = height.value
        print self.max_width, self.max_height
		
    def create(self,x=0,y=0,w=0,h=0,depth=24):
	
        self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
	assert self.display != EGL_NO_DISPLAY
	
	if w <= 0 or h <= 0:
	    w = self.max_width
	    h = self.max_height
	
        r = openegl.eglInitialize(self.display,0,0)
	#assert r == EGL_FALSE
	
        attribute_list = eglints(     (EGL_RED_SIZE, 8,
                                      EGL_GREEN_SIZE, 8,
                                      EGL_BLUE_SIZE, 8,
                                      EGL_ALPHA_SIZE, 8,
				      EGL_DEPTH_SIZE, 24,
				      EGL_BUFFER_SIZE, 32,
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

        nativewindow = eglints((self.dispman_element,w,h+1));
        bcm.vc_dispmanx_update_submit_sync( self.dispman_update )
    
        nw_p = ctypes.pointer(nativewindow)
        self.nw_p = nw_p
        
        self.surface = openegl.eglCreateWindowSurface( self.display, config, nw_p, 0)
        assert self.surface != EGL_NO_SURFACE
        
        r = openegl.eglMakeCurrent(self.display, self.surface, self.surface, self.context)
        assert r
	
	#Create viewport
        opengles.glViewport (0, 0, w, h)
	#Setup perspective view
	opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        nearp=1.0
        farp=500.0
        hht = nearp * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = hht * w / h
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(nearp), eglfloat(farp))
	opengles.glMatrixMode(GL_MODELVIEW)

        #
	opengles.glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
	#opengles.glEnable(GL_CULL_FACE)	
        opengles.glShadeModel(GL_FLAT)
	opengles.glEnable(GL_NORMALIZE)
	opengles.glEnable(GL_DEPTH_TEST)
	
	#switches off alpha blending problem with desktop (is there a bug in the driver?)
	#Thanks to Roland Humphries who sorted this one!!
	opengles.glColorMask(1,1,1,0)  
	
	opengles.glEnableClientState(GL_VERTEX_ARRAY)
	opengles.glEnableClientState(GL_NORMAL_ARRAY)
	
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
        opengles.glFlush()
	#opengles.glClear()
        opengles.glFinish()
	openegl.eglSwapBuffers(self.display, self.surface)
    
    def clear(self):
	opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	
    def setBackColour(self,r,g,b,a):
	self.backColour=(r,g,b,a)
	opengles.glClearColor ( eglfloat(r), eglfloat(g), eglfloat(b), eglfloat(a) )
	if a<1.0:
	    opengles.glColorMask(1,1,1,1)  #switches off alpha blending with desktop (is there a bug in the driver?)
	else:
	    opengles.glColorMask(1,1,1,0)




class create_cuboid(object):
	
	def __init__(self,w,d,h,x=0,y=0,z=0,rx=0,ry=0,rz=0):
		self.width = w
		self.depth = d
		self.height = h
		self.x=x
		self.y=y
		self.z=z
		self.rotx=rx
		self.roty=ry
		self.rotz=rz
		
		#cuboid data - faces are separated out for texturing..

		self.vertices = eglbytes(( -1,1,1, 1,1,1, 1,-1,1, -1,-1,1,
					  1,1,1, 1,1,-1, 1,-1,-1, 1,-1,1,
					  -1,1,1, -1,1,-1, 1,1,-1, 1,1,1,
					  1,-1,1, 1,-1,-1, -1,-1,-1, -1,-1,1,
					  -1,-1,1, -1,-1,-1, -1,1,-1, -1,1,1,
					  -1,1,-1, 1,1,-1, 1,-1,-1, -1,-1,-1));
		self.normals = eglbytes(( 0,0,1, 0,0,1, 0,0,1, 0,0,1,
					  1,0,0, 1,0,0, 1,0,0, 1,0,0, 
					  0,1,0, 0,1,0, 0,1,0, 0,1,0,
					  0,-1,0, 0,-1,0, 0,-1,0, 0,-1,0, 
					  -1,0,0, -1,0,0, -1,0,0, -1,0,0, 
					  0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1))
		self.triangles = eglbytes(( 1,0,3, 1,3,2, 5,4,7, 5,7,6, 9,8,11, 9,11,10, 13,12,15, 13,15,14, 17,16,19, 17,19,18, 21,22,23, 21,23,20));
		self.tex_coords = eglbytes(( 0,0, 255,0, 255,255, 0,255,
					  0,0, 255,0, 255,255, 0,255,
					  0,0, 255,0, 255,255, 0,255,
					  0,0, 255,0, 255,255, 0,255,
					  0,0, 255,0, 255,255, 0,255,
					  0,0, 255,0, 255,255, 0,255))					  
		#self.cube_colours = eglbytes(( 0,0,255,255, 0,0,0,255, 0,255,0,255, 0,255,0,255, 0,0,255,255, 255,0,0,255, 255,0,0,255, 0,0,0,255 ));
		#self.cube_fan1 = eglbytes(( 1,0,3, 1,3,2, 1,2,6, 1,6,5, 1,5,4, 1,4,0 ));
		#self.cube_fan2 = eglbytes(( 7,4,5, 7,5,6, 7,6,2, 7,2,3, 7,3,0, 7,0,4 ));

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
		
	def draw(self,texID):
		opengles.glVertexPointer( 3, GL_BYTE, 0, self.vertices);
		opengles.glNormalPointer( GL_BYTE, 0, self.normals);
		
		if texID > 0: texture_on(texID,self.tex_coords)

		#opengles.glEnableClientState(GL_COLOR_ARRAY)
		#opengles.glColorPointer( 4, GL_UNSIGNED_BYTE, 0, self.cube_colours);
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.width,self.height,self.depth)
		
		opengles.glDrawElements( GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, self.triangles)
		
		if texID > 0: texture_off()


class create_plane(object):
	
	def __init__(self,w,h,x=0,y=0,z=0,rx=0,ry=0,rz=0):
		self.width = w
		self.height = h
		self.x=x
		self.y=y
		self.z=z
		self.rotx=rx
		self.roty=ry
		self.rotz=rz
		
		#plane data - this could be stored locally so that vertices / tex coords an be altered in real-time

		#self.vertices = eglbytes(( -1,1,0, 1,1,0, 1,-1,0, -1,-1,0 ));
		#self.triangles = eglbytes(( 1,0,3, 1,3,2 ));
		#self.normals = eglbytes(( 0,0,1, 0,0,1, 0,0,1, 0,0,1 ));
		#self.tex_coords = eglbytes((0,255, 255,255, 255,0, 0,0));

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
		opengles.glVertexPointer( 3, GL_BYTE, 0, rect_vertsCT);
		opengles.glNormalPointer( GL_BYTE, 0, rect_normals);

		if texID > 0: texture_on(texID,rect_tex_coords)
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.width,self.height,1)    
		opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, rect_triangles)
		if texID > 0: texture_off()
				
class camera(object):
    
    def __init__(self,x=0.0,y=0.0,z=0.0,rx=0.0,ry=0.0,rz=0.0):
	self.x=x
	self.y=y
	self.z=z
	self.rotx=rx
	self.roty=ry
	self.rotz=rz
	
    def orthographic(self,left,right,bottom,top,zoom=1,near=-1,far=10):
	opengles.glMatrixMode(GL_PROJECTION)
	opengles.glLoadIdentity()
	#opengles.glOrthof(eglfloat(-10), eglfloat(10), eglfloat(10), eglfloat(-10.0), eglfloat(near), eglfloat(far))
	opengles.glOrthof(eglfloat(left/zoom), eglfloat(right/zoom), eglfloat(bottom/zoom), eglfloat(top/zoom), eglfloat(near), eglfloat(far))
	opengles.glMatrixMode(GL_MODELVIEW)
	opengles.glLoadIdentity()

    def perspective(self,w,h,zoom,near=1,far=500):
	opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        hht = near * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = hht * w / h
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(near), eglfloat(far))
	opengles.glMatrixMode(GL_MODELVIEW)
	
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
	position(x,y,z,self.rotx,self.roty,self.rotz) #THIS AINT GOING TO WORK!
	
class load_texture(object):
    
    def __init__(self,fileString):
	xyt=load_tex(fileString,GL_RGB,"RGB")
	self.ix=xyt[0]
	self.iy=xyt[1]
	self.tex=xyt[2]
	self.alpha=False	

class load_textureAlpha(object):
    
    def __init__(self,fileString):	
	xyt=load_tex(fileString,GL_RGBA,"RGBA")
	self.ix=xyt[0]
	self.iy=xyt[1]
	self.tex=xyt[2]
	self.alpha=True
		    
class light(object):
    
    def __init__(self,no,x,y,z,red=1,grn=1,blu=1):
	self.ambient = eglfloats((0.2,0.2,0.2,1))
	self.diffuse = eglfloats((red,grn,blu,1))
	self.specular = eglfloats((red,grn,blu,1))
	self.xyz = eglfloats((x,y,z,1))
	self.no = eglint(no)
	self.lighton = True
	
	#opengles.glLightModelf(GL_LIGHT_MODEL_COLOUR_CONTROL, GL_SEPERATE_SPECULAR_COLOR)   #Turns on specular highlights for textures
	opengles.glLightModelf(GL_LIGHT_MODEL_AMBIENT, self.ambient)
	opengles.glLightf(self.no,GL_DIFFUSE,self.diffuse)
	opengles.glLightf(self.no,GL_SPECULAR,self.specular)
	opengles.glLightf(self.no,GL_POSITION,self.xyz)

    def position(self,x,y,z):
	self.xyz = eglfloats((x,y,z,1))
	opengles.glLoadIdentity()
	opengles.glLightf(self.no,GL_POSITION,self.xyz)
    
    def on(self):
	opengles.glEnable(GL_LIGHTING)
	opengles.glEnable(GL_LIGHT0)
	opengles.glDisable(GL_COLOR_MATERIAL)

    def off(self):
	opengles.glDisable(GL_LIGHTING)
	opengles.glDisable(GL_LIGHT0)
	opengles.glEnable(GL_COLOR_MATERIAL)

class piText3D(object):
    
    def __init__(self,font,scx,scy,colour):
	self.font=font
	xyt = load_tex(font+".png",GL_RGBA,"RGBA")
	
    def draw(self,tstring):
	s = tstring.split()
	
	
def showerror():
    e=opengles.glGetError()
    print hex(e)
    
