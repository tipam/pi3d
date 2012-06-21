# pi3D module
# ===========
# Version 0.02
#
# Copyright (c) 2012, Tim Skillman.
# (Some code initially based on Peter de Rivaz pyopengles example.)
#
#    www.github.com/tipam/pi3d
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
from array import *
from ctypes import *


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
eglshort = ctypes.c_short

def eglbytes(L): return (eglbyte*len(L))(*L)
def eglchars(L): return (eglchar*len(L))(*L)
def eglints(L): return (eglint*len(L))(*L)
def eglfloats(L): return (eglfloat*len(L))(*L)
def eglshorts(L): return (eglshort*len(L))(*L)

pipi = 3.1415926
mtrx_stack = 0

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
def texture_on(tex, tex_coords, vtype):
	opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
	opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
	opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
	opengles.glTexCoordPointer(2,vtype,0,tex_coords)
	opengles.glBindTexture(GL_TEXTURE_2D,tex.tex)
	opengles.glEnable(GL_TEXTURE_2D)
	if tex.alpha:
	    #opengles.glDisable(GL_DEPTH_TEST)
	    opengles.glEnable(GL_BLEND)
	    opengles.glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

#turn texture off after drawing arrays
def texture_off():
	opengles.glDisable(GL_TEXTURE_2D)
	opengles.glDisable(GL_BLEND)
	#opengles.glEnable(GL_DEPTH_TEST)
		    
#position, rotate and scale an object
def transform(x,y,z,rotx,roty,rotz,sx,sy,sz,cx,cy,cz):
	#opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x-cx), eglfloat(y-cy), eglfloat(z-cz))		
	if rotx <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(1), eglfloat(0), eglfloat(0))
	if roty <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(0), eglfloat(1), eglfloat(0))
	if rotz <> 0: opengles.glRotatef(eglfloat(rotz),eglfloat(0), eglfloat(0), eglfloat(1))
	opengles.glScalef(eglfloat(sx),eglfloat(sy),eglfloat(sz))
	opengles.glTranslatef(eglfloat(cx), eglfloat(cy), eglfloat(cz))

def rotate(rotx,roty,rotz):
	opengles.glPushMatrix()
	#mtrx_stack+=1
	if rotx <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(1), eglfloat(0), eglfloat(0))
	if roty <> 0: opengles.glRotatef(eglfloat(roty),eglfloat(0), eglfloat(1), eglfloat(0))
	if rotz <> 0: opengles.glRotatef(eglfloat(rotz),eglfloat(0), eglfloat(0), eglfloat(1))

def position(x,y,z):
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))		

def intersectTriangle(v1,v2,v3,pos):
	#Function calculates the y intersection of a point on a triangle
	
	#Z order triangle
	if v1[2]>v2[2]:
	    v=v1
	    v1=v2
	    v2=v
	if v1[2]>v3[2]:
	    v=v1
	    v1=v3
	    v3=v
	if v2[2]>v3[2]:
	    v=v2
	    v2=v3
	    v3=v

	#print "pos:",pos[0],pos[2]
	#print "v1:",v1[0],v1[1],v1[2]
	#print "v2:",v2[0],v2[1],v2[2]
	#print "v3:",v3[0],v3[1],v3[2]
	
	if pos[2]>v2[2]:
	    #test bottom half of triangle
	    if pos[2]>v3[2]:
		#print "z below triangle"
		return -100000  # point completely out
	    za = (pos[2]-v1[2])/(v3[2]-v1[2])
	    dxa = v1[0]+(v3[0]-v1[0])*za
	    dya = v1[1]+(v3[1]-v1[1])*za
	    
	    zb = (v3[2]-pos[2])/(v3[2]-v2[2])
	    dxb = v3[0]-(v3[0]-v2[0])*zb
	    dyb = v3[1]-(v3[1]-v2[1])*zb
	    if (pos[0]<dxa and pos[0]<dxb) or (pos[0]>dxa and pos[0]>dxb):
		#print "outside of bottom triangle range"
		return -100000
	else:
	    #test top half of triangle
	    if pos[2]<v1[2]:
		#print "z above triangle",pos[2],v1[2]
		return -100000  # point completely out
	    za = (pos[2]-v1[2])/(v3[2]-v1[2])
	    dxa = v1[0]+(v3[0]-v1[0])*za
	    dya = v1[1]+(v3[1]-v1[1])*za
	    
	    zb = (v2[2]-pos[2])/((v2[2]+0.00001)-v1[2])  #get rid of FP error!
	    dxb = v2[0]-(v2[0]-v1[0])*zb
	    dyb = v2[1]-(v2[1]-v1[1])*zb
	    if (pos[0]<dxa and pos[0]<dxb) or (pos[0]>dxa and pos[0]>dxb):
		#print "outside of top triangle range"
		return -100000
	
	#return resultant intersecting height
	return dya+(dyb-dya)*((pos[0]-dxa)/(dxb-dxa))
	    
def addVertex(v,x,y,z,n,nx,ny,nz,t,tx,ty):
# add vertex,normal and tex_coords ...
    	v.append(x)
	v.append(y)
	v.append(z)
    	n.append(nx)
	n.append(ny)
	n.append(nz)
    	t.append(tx)
	t.append(ty)

def addTri(v,x,y,z):
# add triangle refs.
    	v.append(x)
	v.append(y)
	v.append(z)
		
def resetMatrices():
	opengles.glLoadIdentity()

rect_normals = eglbytes(( 0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1 ))
rect_tex_coords = eglbytes(( 0,255, 255,255, 255,0, 0,0))
rect_vertsTL = eglbytes(( 1,0,0, 0,0,0, 0,-1,0, 1,-1,0 ))
rect_vertsCT = eglbytes(( 1,1,0, -1,1,0, -1,-1,0, 1,-1,0 ))
rect_triangles = eglbytes(( 3,0,1, 3,1,2 ))

def rectangle(tex,x,y,w,h,r=0.0,z=-1):
	opengles.glNormalPointer( GL_BYTE, 0, rect_normals);
	opengles.glVertexPointer( 3, GL_BYTE, 0, rect_vertsTL);
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))
	opengles.glScalef(eglfloat(w), eglfloat(h), eglfloat(1))
	if r <> 0.0: opengles.glRotatef(eglfloat(r),eglfloat(0), eglfloat(0), eglfloat(1))
	if tex > 0: texture_on(tex,rect_tex_coords,GL_BYTE)
	opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, rect_triangles)
	if tex > 0: texture_off()

def sprite(tex,x,y,z=-10.0,w=1.0,h=1.0,r=0.0):
	opengles.glNormalPointer( GL_BYTE, 0, rect_normals);
	opengles.glVertexPointer( 3, GL_BYTE, 0, rect_vertsCT);
	opengles.glLoadIdentity()
	opengles.glTranslatef(eglfloat(x), eglfloat(y), eglfloat(z))
	opengles.glScalef(eglfloat(w), eglfloat(h), eglfloat(1))
	if r <> 0.0: opengles.glRotatef(eglfloat(r),eglfloat(0), eglfloat(0), eglfloat(1))
	if tex > 0: texture_on(tex,rect_tex_coords,GL_BYTE)
	opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, rect_triangles)
	if tex > 0: texture_off()

def lathe(path, sides = 12, rise = 0.0, coils = 1.0):	    
	s = len(path)
	rl = int(sides * coils)
	ssize = rl * 2 * (s-1) +((s-1) * 2)
	    
	pn = 0
	pp = 0
	tcx = 1.0 / sides
	pr = (pipi / sides) * 2
	rdiv = rise / rl
	
	#find largest and smallest y of the path used for stretching the texture over
	miny = path[0][1]
	maxy = path[s-1][1]
	for p in range (0, s):
	    if path[p][1] < miny:
		miny = path[p][1]
	    if path[p][1] > maxy:
		maxy = path[p][1]
	
	verts=[]
	norms=[]
	idx=[]
	tex_coords=[]
	
	for p in range (0, s):
	    px = path[p][0]
	    py = path[p][1]
	    tcy = 1.0 - ((py - miny)/(maxy - miny))
	    
	    for r in range (0, rl):
		verts.append(px * math.sin(pr * r))
		verts.append(py)
		verts.append(px * math.cos(pr * r))
		norms.append(0.0)
		norms.append(1.0)
		norms.append(0.0)
		tex_coords.append(tcx * r)
		tex_coords.append(tcy)
		py = py + rdiv
	    #last path profile (tidies texture coords)
	    verts.append(0)
	    verts.append(py)
	    verts.append(px)
	    norms.append(0.0)
	    norms.append(1.0)
	    norms.append(0.0)
	    tex_coords.append(1.0)
	    tex_coords.append(tcy)

	    if p > 0:
		pn += (rl+1)
		for r in range (0, rl):
		    idx.append(pp+r)
		    idx.append(pn+r)
		idx.append(pp+sides)
		idx.append(pn+sides)
		pp += (rl+1)

	return (verts, norms, idx, tex_coords, ssize)

def shape_draw(self,tex,shl=GL_UNSIGNED_SHORT):
	    opengles.glVertexPointer( 3, GL_FLOAT, 0, self.vertices)
	    opengles.glNormalPointer( GL_FLOAT, 0, self.normals)
	    if tex > 0: texture_on(tex,self.tex_coords,GL_FLOAT)
	    transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,self.sz,self.cx,self.cy,self.cz)
	    opengles.glDrawElements( GL_TRIANGLE_STRIP, self.ssize, shl , self.indices)
	    if tex > 0: texture_off()

def create_display(self,x=0,y=0,w=0,h=0,depth=24):
    
        self.display = openegl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
	assert self.display != EGL_NO_DISPLAY
	
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
	
	#Setup default hints
	opengles.glEnable(GL_CULL_FACE)	
        opengles.glShadeModel(GL_FLAT)
	opengles.glEnable(GL_NORMALIZE)
	opengles.glEnable(GL_DEPTH_TEST)
	
	#switches off alpha blending problem with desktop (is there a bug in the driver?)
	#Thanks to Roland Humphries who sorted this one!!
	opengles.glColorMask(1,1,1,0)  
	
	opengles.glEnableClientState(GL_VERTEX_ARRAY)
	opengles.glEnableClientState(GL_NORMAL_ARRAY)
	
	self.active = True

		    
class key():
    
    def __init__(self):
	self.key = curses.initscr()
	self.key.nodelay(1)

    def read(self):
	return (self.key.getch())

#=====================================================================================================================================================================================	
# Setup EGL display
    
class display(object):

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
		
    def create3D(self,x=0,y=0,w=0,h=0,depth=24,near=1.0,far=500.0):
	
	if w <= 0 or h <= 0:
	    w = self.max_width
	    h = self.max_height
	
	self.win_width = w
	self.win_height = h
        self.near=near
        self.far=far
	    
	create_display(self,x,y,w,h,depth)
	
	#Setup perspective view
	opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        hht = near * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = hht * w / h
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(near), eglfloat(far))
	opengles.glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
	opengles.glMatrixMode(GL_MODELVIEW)
	opengles.glLoadIdentity()


    def create2D(self,x=0,y=0,w=0,h=0,depth=24,near=-1.0,far=100.0):

	if w <= 0 or h <= 0:
	    w = self.max_width
	    h = self.max_height
	    
	self.win_width = w
	self.win_height = h

	create_display(self,x,y,w,h,depth)
	
	opengles.glMatrixMode(GL_PROJECTION)
	opengles.glLoadIdentity()
	opengles.glOrthof(eglfloat(0), eglfloat(w), eglfloat(0), eglfloat(h), eglfloat(-1), eglfloat(500))
	opengles.glMatrixMode(GL_MODELVIEW)
	opengles.glLoadIdentity()
	
	
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
	
        
    def swapBuffers(self):
        opengles.glFlush()
        opengles.glFinish()
	#clear_matrices
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
	    
    def screenshot(self,filestring):
	#CRASHES FOR NOW
	#screen = ctypes.pointer(opengles.glReadPixels(0,0,self.win_width,self.win_height, GL_RGBA, GL_UNSIGNED_BYTE))
	#im = Image.frombuffer("RGB",(self.win_width,self.win_height), screen, "raw", "RGB", 0,1)
	#im.save(filestring)
	


#=====================================================================================================================================================================================	
# Creation functions

class create_shape(object):

	def __init__(self,name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz):
		self.name = name
		self.x=x		#position
		self.y=y
		self.z=z
		self.rotx=rx		#rotation
		self.roty=ry
		self.rotz=rz
		self.sx=sx		#scale
		self.sy=sy
		self.sz=sz
		self.cx=cx		
		self.cy=cy
		self.cz=cz
		

	#this should all be done with matrices!! ... just for testing ...

	def scale(self,sx,sy,sz):
		self.sx = sx
		self.sy = sy
		self.sz = sz

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
    
class createCuboid(create_shape):
	
	def __init__(self,name, w,d,h, x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, cx=0.0,cy=0.0,cz=0.0):
		super(createCuboid,self).__init__(name, x,y,z, rx,ry,rz, 1.0,1.0,1.0, cx,cy,cz)
		
		print "Creating cuboid ..."
		
		self.width = w
		self.depth = d
		self.height = h
		self.ttype = GL_TRIANGLES
		ww=w*.5
		hh=h*.5
		dd=d*.5
		
		#cuboid data - faces are separated out for texturing..

		self.vertices = eglfloats(( -ww,hh,dd, ww,hh,dd, ww,-hh,dd, -ww,-hh,dd,
					  ww,hh,dd, ww,hh,-dd, ww,-hh,-dd, ww,-hh,dd,
					  -ww,hh,dd, -ww,hh,-dd, ww,hh,-dd, ww,hh,dd,
					  ww,-hh,dd, ww,-hh,-dd, -ww,-hh,-dd, -ww,-hh,dd,
					  -ww,-hh,dd, -ww,-hh,-dd, -ww,hh,-dd, -ww,hh,dd,
					  -ww,hh,-dd, ww,hh,-dd, ww,-hh,-dd, -ww,-hh,-dd));
		self.normals = eglfloats(( 0,0,1, 0,0,1, 0,0,1, 0,0,1,
					  1,0,0, 1,0,0, 1,0,0, 1,0,0, 
					  0,1,0, 0,1,0, 0,1,0, 0,1,0,
					  0,-1,0, 0,-1,0, 0,-1,0, 0,-1,0, 
					  -1,0,0, -1,0,0, -1,0,0, -1,0,0, 
					  0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1))
		self.indices = eglshorts(( 1,0,3, 1,3,2, 5,4,7, 5,7,6, 9,8,11, 9,11,10, 13,12,15, 13,15,14, 17,16,19, 17,19,18, 21,22,23, 21,23,20));
		self.tex_coords = eglfloats(( 0,0, 1,0, 1,1, 0,1,
					  0,0, 1,0, 1,1, 0,1,
					  0,0, 1,0, 1,1, 0,1,
					  0,0, 1,0, 1,1, 0,1,
					  0,0, 1,0, 1,1, 0,1,
					  0,0, 1,0, 1,1, 0,1))
					  
		#self.cube_colours = eglbytes(( 0,0,255,255, 0,0,0,255, 0,255,0,255, 0,255,0,255, 0,0,255,255, 255,0,0,255, 255,0,0,255, 0,0,0,255 ));
		#self.cube_fan1 = eglbytes(( 1,0,3, 1,3,2, 1,2,6, 1,6,5, 1,5,4, 1,4,0 ));
		#self.cube_fan2 = eglbytes(( 7,4,5, 7,5,6, 7,6,2, 7,2,3, 7,3,0, 7,0,4 ));
		
	def draw(self,tex):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.vertices);
		opengles.glNormalPointer( GL_FLOAT, 0, self.normals);
		
		if tex > 0: texture_on(tex,self.tex_coords,GL_FLOAT)
		#opengles.glEnableClientState(GL_COLOR_ARRAY)
		#opengles.glColorPointer( 4, GL_UNSIGNED_BYTE, 0, self.cube_colours);
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,self.sz,self.cx,self.cy,self.cz)
		opengles.glDrawElements( GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, self.indices)
		if tex > 0: texture_off()


class createMergeShape(create_shape):
	
	def __init__(self,name="",x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, sx=1.0,sy=1.0,sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createMergeShape,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Merge Shape ..."
		
		self.vertices=[]
		self.normals=[]
		self.tex_coords=[]
		self.indices=[]    #stores all indices for single render
		self.shape=[]
	    
	def merge(self,shape,x,y,z,rx=0.0,ry=0.0,rz=0.0,sx=1.0,sy=1.0,sz=1.0):

		# ONLY WORKS WITH GL_TRIANGLES
		if shape.ttype <> GL_TRIANGLES:
		    assert "Only GL_TRIANGLE shapes can be merged"
		    
		print "Merging Shape ..."
		
		vertices=[]
		normals=[]
		tex_coords=[]
		totindices=[]
		
		#ctypes.restype = ctypes.c_float
		ve = len(self.vertices)
		vi = len(self.indices)
		vc = len(shape.vertices)
		ic = len(shape.indices)
		vp = ve/3
		
		#print vc,ve,vi,ic
		    
		for v in range(0,vc,3):
		    vx = shape.vertices[v]
		    vy = shape.vertices[v+1]
		    vz = shape.vertices[v+2]
		    #print vx+x,vy+y,vz+z
		    #Rotate vertices here
		    self.vertices.append(vx*sx+x)
		    self.vertices.append(vy*sy+y)
		    self.vertices.append(vz*sz+z)
		    #Normals should also be rotated
		    self.normals.append(shape.normals[v])
		    self.normals.append(shape.normals[v+1])
		    self.normals.append(shape.normals[v+2])
		    
		for v in range(0,len(shape.tex_coords)):
		    self.tex_coords.append(shape.tex_coords[v])
		
		        
		ctypes.restype = ctypes.c_short
		indices=[]
		for v in range(0,ic):
		    ix = shape.indices[v]+vp
		    indices.append(ix)
		    self.indices.append(ix)
		    
		#print "verts:",vertices
		#print "inds",indices
		#print "tcs:",tex_coords
		
		self.totind = ic+vi
		self.verts = eglfloats(self.vertices)
		self.norms = eglfloats(self.normals)
		self.texcoords = eglfloats(self.tex_coords)
		self.inds = eglshorts(self.indices)
		self.shape.append((eglshorts(indices),ic,shape.ttype))

	def draw(self,shapeNo,tex):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
		opengles.glNormalPointer( GL_FLOAT, 0, self.norms);		
		if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
		transform(self.x,self.y,self.z, self.rotx,self.roty,self.rotz, self.sx,self.sy,self.sz, self.cx,self.cy,self.cz)		
		opengles.glDrawElements( self.shape[shapeNo][2], self.shape[shapeNo][1], GL_UNSIGNED_SHORT, self.shape[shapeNo][0])
		if tex > 0: texture_off()

	def drawAll(self,tex):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
		opengles.glNormalPointer( GL_FLOAT, 0, self.norms);		
		if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
		transform(self.x,self.y,self.z, self.rotx,self.roty,self.rotz, self.sx,self.sy,self.sz, self.cx,self.cy,self.cz)		
		opengles.glDrawElements( self.shape[0][2], self.totind, GL_UNSIGNED_SHORT, self.inds)
		if tex > 0: texture_off()
		
	
class createPlane(create_shape):
	
	def __init__(self,name,w,h, x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createPlane,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

		print "Creating plane ..."

		self.width = w
		self.height = h
		self.ttype = GL_TRIANGLES
		self.vertices=[]
		self.normals=[]
		self.tex_coords=[]
		self.indices=[]
		ww=w*.5
		hh=h*.5
		
		addVertex(self.vertices,-ww+x,hh+y,z,self.normals,0,0,1,self.tex_coords,0.0,0.0)
		addVertex(self.vertices,ww+x,hh+y,z,self.normals,0,0,1,self.tex_coords,1.0,0.0)
		addVertex(self.vertices,ww+x,-hh+y,z,self.normals,0,0,1,self.tex_coords,1.0,1.0)
		addVertex(self.vertices,-ww+x,-hh+y,z,self.normals,0,0,1,self.tex_coords,0.0,1.0)
		addTri(self.indices,1,0,3)
		addTri(self.indices,1,3,2)
		#plane data - this could be stored locally so that vertices / tex coords an be altered in real-time

		self.verts = eglfloats(self.vertices);
		self.inds = eglshorts(self.indices);
		self.norms = eglfloats(self.normals);
		self.texcoords = eglfloats(self.tex_coords);
		
	
	def draw(self,tex):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
		opengles.glNormalPointer( GL_FLOAT, 0, self.norms);

		if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,1,self.cx,self.cy,self.cz)    
		opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, self.inds)
		if tex > 0: texture_off()


class createLathe(create_shape):

	def __init__(self,name,x,y,z,path,sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(create_lathe,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

		print "Creating lathe ..."

		self.path = path
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]
	    

	def draw(self,texID):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.vertices);
		opengles.glNormalPointer( GL_FLOAT, 0, self.normals);

		if texID > 0: texture_on(texID,self.tex_coords,GL_FLOAT)
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,self.sz,self.cx,self.cy,self.cz)
		opengles.glDrawElements( GL_TRIANGLE_STRIP, self.ssize, GL_UNSIGNED_SHORT, self.indices)
		if texID > 0: texture_off()



class createSphere(create_shape):

	def __init__(self,name,x,y,z,radius,slices,sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createSphere,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating sphere ..."

		path = []
		st = pipi/slices
		for r in range(0,slices):
		    path.append((radius * math.sin(r*st),radius * math.cos(r*st)))
			
		self.radius = radius
		self.slices = slices
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,tex):
		shape_draw(self,tex)

class createTorus(create_shape):

	def __init__(self,name,x,y,z,radius,thickness, ringrots, sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createTorus,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Torus ..."

		path = []
		st = (pipi*2)/ringrots
		for r in range(0,ringrots+1):
		    path.append((radius + thickness * math.sin(r*st),thickness * math.cos(r*st)))
			
		self.radius = radius
		self.thickness = thickness
		self.ringrots = ringrots
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,tex):
		shape_draw(self,tex)

class createTube(create_shape):

	def __init__(self,name,x,y,z,radius,thickness, height, sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createTube,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Tube ..."
		
		t = thickness * 0.5
		path = []
		path.append((radius-t, height * .5))
		path.append((radius+t, height * .5))
		path.append((radius+t, -height * .5))
		path.append((radius-t, -height * .5))
		path.append((radius-t, height * .5))
			
		self.radius = radius
		self.thickness = thickness
		self.height = height
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,tex):
		shape_draw(self,tex)
		
class createSpiral(create_shape):

	def __init__(self,name,x,y,z,radius,thickness, ringrots, sides, rise=1.0, loops=2.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createSpiral,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Spiral ...", radius,thickness, ringrots, sides

		path = []
		st = (pipi*2)/ringrots
		for r in range(0,ringrots+1):
		    path.append((radius + thickness * math.sin(r*st),thickness * math.cos(r*st)))
		    print "path:",path[r][0], path[r][1]
			
		self.radius = radius
		self.thickness = thickness
		self.ringrots = ringrots
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides, rise, loops)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,texID):
		shape_draw(self, texID)
				
class createCylinder(create_shape):

	def __init__(self,name,x,y,z,radius,height,sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createCylinder,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Cylinder ..."

		path = []
		path.append((0,height * .5))
		path.append((radius, height * .5))
		path.append((radius, -height * .5))
		path.append((0,-height * .5))
		
		self.radius = radius
		self.height = height
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,tex):
		shape_draw(self,tex)
		
class createCone(create_shape):

	def __init__(self,name,x,y,z,radius,height,sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createCone,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Cone ..."

		path = []
		path.append((0,height * .5))
		path.append((radius, -height * .5))
		path.append((0,-height * .5))
		
		self.radius = radius
		self.height = height
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]

	def draw(self,tex):
		shape_draw(self,tex)		
	
class createTCone(create_shape):

	def __init__(self,name,x,y,z,radiusBot,radiusTop, height,sides, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createTCone,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Truncated Cone ..."

		path = []
		path.append((0,height * .5))
		path.append((radiusTop, height * .5))
		path.append((radiusBot, -height * .5))
		path.append((0,-height * .5))
		
		self.radiusBot = radiusBot
		self.radiusTop = radiusTop
		self.height = height
		self.sides = sides
		self.ttype = GL_TRIANGLE_STRIP
		
		results = lathe(path, sides)
		
		self.vertices = eglfloats(results[0])
		self.normals = eglfloats(results[1])
		self.indices = eglshorts(results[2])
		self.tex_coords = eglfloats(results[3])
		self.ssize = results[4]


	def draw(self,tex):
		shape_draw(self,tex)

class createExtrude(create_shape):

	def __init__(self,name,x,y,z, path, height, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createExtrude,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Creating Extrude ..."
		
		s = len(path)
		ht = height * 0.5

		self.verts=[]
		self.norms=[]
		self.botface=[]
		self.topface=[]
		self.sidefaces=[]
		self.tex_coords=[]
		self.edges = s
		self.ttype = GL_TRIANGLES
		
		minx = path[0][0]
		maxx = path[0][0]
		miny = path[0][1]
		maxy = path[0][1]
		
		#find min/max values for texture coords
		for p in range(0, s):
		    px = path[p][0]
		    py = path[p][1]
		    if py < miny: miny = py
		    if py > maxy: maxy = py
		    if px < minx: minx = px
		    if px > maxx: maxx = px
	    	
		tx = 1.0/(maxx-minx)
		ty = 1.0/(maxy-miny)
		
		for p in range (0, s):
		    px = path[p][0]
		    py = path[p][1]
		    self.verts.append(px)
		    self.verts.append(py)
		    self.verts.append(-ht)
		    self.norms.append(0.0)
		    self.norms.append(0.0)
		    self.norms.append(-1.0)
		    self.tex_coords.append((px-minx)*tx)
		    self.tex_coords.append((py-miny)*ty)		    
	    
		for p in range (0, s):
		    px = path[p][0]
		    py = path[p][1]
		    self.verts.append(px)
		    self.verts.append(py)
		    self.verts.append(ht)
		    self.norms.append(0.0)
		    self.norms.append(0.0)
		    self.norms.append(1.0)
		    self.tex_coords.append((px-minx)*tx)
		    self.tex_coords.append((py-miny)*ty)		    

		for p in range (0, s):		#top face indices - triangle fan
		    self.topface.append(p)
		    
		for p in range (0, s):		#bottom face indices - triangle fan
		    b=s+(s-p)
		    print "bi:",b
		    self.botface.append(b-1)
	
		for p in range (0, s):		#sides - triangle strip
		    self.sidefaces.append(p)
		    self.sidefaces.append(p+s)
		self.sidefaces.append(0)
		self.sidefaces.append(s)
		    
		self.verts = eglfloats(self.verts)
		self.norms = eglfloats(self.norms)
		self.tex_coords = eglfloats(self.tex_coords)
		self.topface = eglshorts(self.topface)
		self.botface = eglshorts(self.botface)
		self.sidefaces = eglshorts(self.sidefaces)

	def draw(self,tex1,tex2,tex3):
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts)
		opengles.glNormalPointer( GL_FLOAT, 0, self.norms)
		transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,self.sz,self.cx,self.cy,self.cz)
		if tex1 > 0: texture_on(tex1,self.tex_coords,GL_FLOAT)
		opengles.glDrawElements( GL_TRIANGLE_STRIP, self.edges * 2+2, GL_UNSIGNED_SHORT, self.sidefaces)
		if tex2 > 0: texture_on(tex2,self.tex_coords,GL_FLOAT)
		opengles.glDrawElements( GL_TRIANGLE_FAN, self.edges, GL_UNSIGNED_SHORT, self.topface)
		if tex3 > 0: texture_on(tex3,self.tex_coords,GL_FLOAT)
		opengles.glDrawElements( GL_TRIANGLE_FAN, self.edges, GL_UNSIGNED_SHORT, self.botface)
		if tex1 > 0: texture_off()

class createElevationMapFromTexture(create_shape):

	def __init__(self,name,x,y,z, mapfile, width, depth, height, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
		super(createElevationMapFromTexture,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
		
		print "Loading ...",mapfile
		
		im = Image.open(mapfile)
		self.pixels = im.load()
		ix,iy = im.size
		self.width = width
		self.depth = depth
		self.height = height
		self.ix=ix
		self.iy=iy
		self.ttype = GL_TRIANGLE_STRIP
		
		print "Creating Elevation Map ..."

		wh = width*0.5
		hh = depth*0.5
		ws = width / ix
		hs = depth / iy
		ht = height / 255.0
		tx = 1.0/ix
		ty = 1.0/iy
		
		verts=[]
		norms=[]
		tex_coords=[]
		idx=[]
		
		for y in range(0,iy):
		    for x in range(0,ix):
			hgt = self.pixels[x,y] * ht
			#print pixht
			#hgt = pixht[0]
			verts.append(-wh+x*ws)
			verts.append(hgt)
			verts.append(-hh+y*hs)
			norms.append(0.0)
			norms.append(1.0)
			norms.append(0.0)
			tex_coords.append(x * tx)
			tex_coords.append((iy-y) * ty)
		
		s=0
		#create one long triangle_strip by alternating X directions	
		for y in range(0,iy-2,2):
		    for x in range(0,ix-1):
			i = (y * ix)+x
			idx.append(i)
			idx.append(i+ix)
			s+=2
		    for x in range(ix-1,0,-1):
			i = ((y+1) * ix)+x
			idx.append(i+ix)
			idx.append(i)
			s+=2

		self.vertices = eglfloats(verts)
		self.normals = eglfloats(norms)
		self.indices = eglshorts(idx)
		self.tex_coords = eglfloats(tex_coords)
		self.ssize = s  #ix * iy * 2
		print s, ix * iy * 2
	
	# determines how high an object is when dropped on the map (providing it's inside the map area)
	def dropOn(self,x,z):
		wh = self.width*0.5 
		hh = self.depth*0.5 
		ws = self.width / self.ix
		hs = self.depth / self.iy
		ht = self.height / 255.0
		
		if x > -wh and x < wh and z > -hh and z < hh:
		    pixht = self.pixels[(wh-x)/ws,(hh-z)/hs] * ht
		
		return pixht

	# accurately determines how high an object is when dropped on the map (providing it's inside the map area)
	def calcHeight(self,px,pz):
		wh = self.width*0.5 
		hh = self.depth*0.5 
		ws = self.width / self.ix
		hs = self.depth / self.iy
		ht = self.height / 255.0
		#round off to nearest integer
		px = (wh - px)/ws
		pz = (hh - pz)/hs
		x = math.floor(px)
		z = math.floor(pz)
		#print px,pz,x,z
		#x = wh-math.floor(x+0.5)/ws
		#z = hh-math.floor(z+0.5)/hs
		
		ih=intersectTriangle((x,self.pixels[x,z]*ht,z), (x+1,self.pixels[x+1,z]*ht,z), (x,self.pixels[x,z+1]*ht,z+1), (px,0,pz))
		if ih == -100000:
		    ih=intersectTriangle((x+1,self.pixels[x+1,z+1]*ht,z+1), (x+1,self.pixels[x+1,z]*ht,z), (x,self.pixels[x,z+1]*ht,z+1), (px,0,pz))
		if ih == -100000: ih = 0
		
		return ih
		
	def draw(self,tex):
		shape_draw(self,tex)

			
			
			
		
#=====================================================================================================================================================================================	
# Cameras
				
class camera(create_shape):
    
    def __init__(self,name="",x=0.0,y=0.0,z=0.0,rx=0.0,ry=0.0,rz=0.0):
	super(camera,self).__init__(name, x,y,z, rx,ry,rz, 1,1,1)
	print "Creating camera ..."
	
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
	
#=====================================================================================================================================================================================	
# Texture functions

class loadTexture(object):
    
    def __init__(self,fileString):
	xyt=load_tex(fileString,GL_RGB,"RGB")
	self.ix=xyt[0]
	self.iy=xyt[1]
	self.tex=xyt[2]
	self.alpha=False	

class loadTextureAlpha(object):
    
    def __init__(self,fileString):	
	xyt=load_tex(fileString,GL_RGBA,"RGBA")
	self.ix=xyt[0]
	self.iy=xyt[1]
	self.tex=xyt[2]
	self.alpha=True
		  
#=====================================================================================================================================================================================	
# Lights

class light(object):
    
    def __init__(self,name,no,x,y,z,red=1,grn=1,blu=1):

	print "Creating light ..."

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

#=====================================================================================================================================================================================	
# Text and fonts

class piText3D(object):
    
    def __init__(self,name,font,scx,scy,colour):
	self.font=font
	xyt = load_tex(font+".png",GL_RGBA,"RGBA")
	
    def draw(self,tstring):
	s = tstring.split()
	
	
def showerror():
    e=opengles.glGetError()
    print hex(e)
    
