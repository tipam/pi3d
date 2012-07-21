# pi3D module
# ===========
# Version 0.05
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

pi3d_version = 0.05

import sys, random
sys.path.append("include")
from pi3dCommon import *
import loaderEgg
import PIL.ImageOps, ImageDraw

def loadECfiles(path,fname,texs):
    #helper for loading environment cube faces
    filep=path+"/"+fname
    faces=[]
    faces.append(texs.loadTexture(filep+"_top.jpg"))
    faces.append(texs.loadTexture(filep+"_left.jpg"))
    faces.append(texs.loadTexture(filep+"_front.jpg"))
    faces.append(texs.loadTexture(filep+"_right.jpg"))
    faces.append(texs.loadTexture(filep+"_back.jpg"))
    faces.append(texs.loadTexture(filep+"_bottom.jpg"))
    return faces
    
def merge(self,shape, x,y,z, rx=0.0,ry=0.0,rz=0.0, sx=1.0,sy=1.0,sz=1.0, cx=0.0,cy=0.0,cz=0.0):

        # ONLY WORKS WITH GL_TRIANGLES
        if shape.ttype <> GL_TRIANGLES:
            assert "Only GL_TRIANGLE shapes can be merged"
            
        print "Merging", shape.name
        
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
            #Rotate vertices
            vx = shape.vertices[v]
            vy = shape.vertices[v+1]
            vz = shape.vertices[v+2]
            if rz<>0.0: vx,vy,vz = rotateVecZ(rz,vx,vy,vz)
            if rx<>0.0: vx,vy,vz = rotateVecX(rx,vx,vy,vz)
            if ry<>0.0: vx,vy,vz = rotateVecY(ry,vx,vy,vz)

            #Scale, offset and store vertices
            self.vertices.append(vx*sx+x)
            self.vertices.append(vy*sy+y)
            self.vertices.append(vz*sz+z)

            #Rotate normals
            vx = shape.normals[v]
            vy = shape.normals[v+1]
            vz = shape.normals[v+2]
            if rz<>0.0: vx,vy,vz = rotateVecZ(rz,vx,vy,vz)
            if rx<>0.0: vx,vy,vz = rotateVecX(rx,vx,vy,vz)
            if ry<>0.0: vx,vy,vz = rotateVecY(ry,vx,vy,vz)      
            self.normals.append(vx)
            self.normals.append(vy)
            self.normals.append(vz)
            
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
        self.ttype = GL_TRIANGLES
        self.shape.append((eglshorts(indices),ic,shape.ttype))
                
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
        
        #print startup notices
        print "Pi3D module - version",pi3d_version
        print "Copyright (c) Tim Skillman, 2012"
        print "Updates available from www.github.com/tipam/pi3d"
        print "Screen size",self.max_width, self.max_height
                
    def create3D(self,x=0,y=0,w=0,h=0, near=1.0, far=800.0, aspect=60.0, depth=24):
        
        if w <= 0 or h <= 0:
            w = self.max_width
            h = self.max_height
        
        self.win_width = w
        self.win_height = h
        self.near=near
        self.far=far
	
	self.left = x
	self.top = y
	self.right = x+w
	self.bottom = y+h
            
        create_display(self,x,y,w,h,depth)
        
        #Setup perspective view
        opengles.glMatrixMode(GL_PROJECTION)
        opengles.glLoadIdentity()
        hht = near * math.tan(aspect / 2.0 / 180.0 * 3.1415926)
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
	#opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
        opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
    def setBackColour(self,r,g,b,a):
        self.backColour=(r,g,b,a)
        opengles.glClearColor ( eglfloat(r), eglfloat(g), eglfloat(b), eglfloat(a) )
        if a<1.0:
            opengles.glColorMask(1,1,1,1)  #switches off alpha blending with desktop (is there a bug in the driver?)
        else:
            opengles.glColorMask(1,1,1,0)
            
    def screenshot(self,filestring):
        
        print "Taking screenshot to '",filestring,"'"
        
        size = self.win_height * self.win_width * 3
        img = (ctypes.c_char*size)()
        opengles.glReadPixels(0,0,self.win_width,self.win_height, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))
        im = Image.frombuffer("RGB",(self.win_width,self.win_height), img, "raw", "RGB", 0,1)
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im.save(filestring)
        


#=====================================================================================================================================================================================  
# Creation functions

class createCuboid(create_shape):
        
        def __init__(self, w,h,d, name="", x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, cx=0.0,cy=0.0,cz=0.0):
                super(createCuboid,self).__init__(name, x,y,z, rx,ry,rz, 1.0,1.0,1.0, cx,cy,cz)
                
                print "Creating cuboid ..."
                
                self.width = w
                self.height = h
                self.depth = d
                self.ssize = 36
                self.ttype = GL_TRIANGLES

                ww=w*.5
                hh=h*.5
                dd=d*.5
                
                tw=1.0 #w       #texture scales (each set to 1 would stretch it over face)
                th=1.0 #h
                td=1.0 #d
                
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
                self.indices = eglshorts(( 1,0,3, 1,3,2, 5,4,7, 5,7,6, 9,8,11, 9,11,10, 13,12,15, 13,15,14, 19,18,17, 19,17,16, 20,21,22, 20,22,23));
                self.tex_coords = eglfloats(( 0,0, tw,0, tw,th, 0,th,
                                          0,0, td,0, td,th, 0,th,
                                          tw,0, 0,0, 0,td, tw,td,
                                          0,0, tw,0, tw,td, 0,td,
                                          td,th, 0,th, 0,0, td,0,
                                          tw,0, 0,0, 0,th, tw,th))
                                          
                #self.cube_colours = eglbytes(( 0,0,255,255, 0,0,0,255, 0,255,0,255, 0,255,0,255, 0,0,255,255, 255,0,0,255, 255,0,0,255, 0,0,0,255 ));
                #self.cube_fan1 = eglbytes(( 1,0,3, 1,3,2, 1,2,6, 1,6,5, 1,5,4, 1,4,0 ));
                #self.cube_fan2 = eglbytes(( 7,4,5, 7,5,6, 7,6,2, 7,2,3, 7,3,0, 7,0,4 ));
                
        def draw(self,tex=None):
                shape_draw(self,tex)


class createEnvironmentCube(object):
        
        def __init__(self,size=500.0,maptype="HALFCROSS",name=""):
                
                print "Creating Environment Cube ..."
                
                self.scale = size
                self.ssize = 36
                self.ttype = GL_TRIANGLES
		self.maptype = maptype
                ww=self.scale*.5
                hh=self.scale*.5
                dd=self.scale*.5
                
                #cuboid data - faces are separated out for texturing..

                self.vertices = eglfloats(( -ww,hh,dd, ww,hh,dd, ww,-hh,dd, -ww,-hh,dd,
                                          ww,hh,dd, ww,hh,-dd, ww,-hh,-dd, ww,-hh,dd,
                                          -ww,hh,dd, -ww,hh,-dd, ww,hh,-dd, ww,hh,dd,
                                          ww,-hh,dd, ww,-hh,-dd, -ww,-hh,-dd, -ww,-hh,dd,
                                          -ww,-hh,dd, -ww,-hh,-dd, -ww,hh,-dd, -ww,hh,dd,
                                          -ww,hh,-dd, ww,hh,-dd, ww,-hh,-dd, -ww,-hh,-dd ))
                                          
                self.normals = eglfloats(( 0,0,1, 0,0,1, 0,0,1, 0,0,1,
                                          1,0,0, 1,0,0, 1,0,0, 1,0,0, 
                                          0,1,0, 0,1,0, 0,1,0, 0,1,0,
                                          0,-1,0, 0,-1,0, 0,-1,0, 0,-1,0, 
                                          -1,0,0, -1,0,0, -1,0,0, -1,0,0, 
                                          0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1))

                self.indices = eglshorts(( 3,0,1, 2,3,1, 7,4,5, 6,7,5, 11,8,9, 10,11,9, 15,12,13, 14,15,13, 19,16,17, 18,19,17, 23,22,21, 20,23,21));

                self.indfront = eglshorts((23,22,21, 20,23,21 )) #back
		self.indleft = eglshorts((19,16,17, 18,19,17)) #right
		self.indtop = eglshorts((11,8,9, 10,11,9))  #top
		self.indbot = eglshorts((15,12,13, 14,15,13))  #bottom
		self.indright = eglshorts((7,4,5, 6,7,5)) #left
		self.indback = eglshorts((3,0,1, 2,3,1)) #front
                
                if self.maptype == "HALFCROSS":
                    self.tex_coords = eglfloats(( 0.25,0.25, 0.25,0.75, -0.25,0.75, -0.25,0.25,
                                          0.25,0.75, 0.75,0.75, 0.75,1.25, 0.25,1.25,
                                          0.25,0.25, 0.75,0.25, 0.75,0.75, 0.25,0.75,  #top
                                          0,0, 1,0, 1,1, 0,1,    #bottom
                                          0.25,-0.25, 0.75,-0.25, 0.75,0.25, 0.25,0.25,
                                          0.75,0.25, 0.75,0.75, 1.25,0.75, 1.25,0.25))
		elif self.maptype == "CROSS":
                    self.tex_coords = eglfloats(( 1.0,0.34, 0.75,0.34, 0.75,0.661, 1.0,0.661, #back
                                          0.75,0.34, 0.5,0.34, 0.5,0.661, 0.75,0.661,  #right
                                          0.251,0.0, 0.251,0.34, 0.498,0.34, 0.498,0.0,  #top
                                          0.498,.998, 0.498,0.66, 0.251,0.66, 0.251,.998,    #bottom
                                          0.0,0.661, 0.25,0.661, 0.25,0.34, 0.0,0.34,    #left
                                          0.25,0.34, 0.5,0.34, 0.5,0.661, 0.25,0.661 )) #front
		else:
		    self.tex_faces = eglfloats(( .998,0.002, 0.002,0.002, 0.002,.998, .998,.998,  
						.998,0.002, 0.002,0.002, 0.002,.998, .998,.998,
						0.002,0.002, 0.002,.998, .998,.998, .998,0.002,
						.998,.998, .998,0.002, 0.002,0.002, 0.002,.998,  
						0.002,.998, .998,.998, .998,0.002, 0.002,0.002,
						0.002,0.002, .998,0.002, .998,.998, 0.002,.998))
		    

        def draw(self,tex,x,y,z):
		mtrx =(ctypes.c_float*16)()
		opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(mtrx))
		opengles.glTranslatef(eglfloat(-x), eglfloat(-y), eglfloat(-z))
		opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
		opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
		opengles.glVertexPointer( 3, GL_FLOAT, 0, self.vertices)
		opengles.glNormalPointer( GL_FLOAT, 0, self.normals)
		opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		opengles.glDisable(GL_LIGHTING)
		opengles.glEnable(GL_TEXTURE_2D)
		
		if self.maptype=="FACES":
		    opengles.glTexCoordPointer(2, GL_FLOAT, 0, self.tex_faces)
		    opengles.glBindTexture(GL_TEXTURE_2D,tex[0].tex)
		    opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indtop)
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
		    opengles.glBindTexture(GL_TEXTURE_2D,tex[1].tex)
		    opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indleft)
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
		    opengles.glBindTexture(GL_TEXTURE_2D,tex[2].tex)
		    opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indfront)
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
		    opengles.glBindTexture(GL_TEXTURE_2D,tex[3].tex)
		    opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indright)
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));
		    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
		    opengles.glBindTexture(GL_TEXTURE_2D,tex[4].tex)
		    opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indback)
		    if tex[5] >0:
			opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_LINEAR));  #BOTTOM (doesn't have to have one if None)
			opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_LINEAR));
			opengles.glBindTexture(GL_TEXTURE_2D,tex[5].tex)
			opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indbot)
		else:
		    #load view matrix
		    opengles.glTexCoordPointer(2, GL_FLOAT, 0, self.tex_coords)
		    opengles.glBindTexture(GL_TEXTURE_2D,tex.tex)
		    opengles.glDrawElements( GL_TRIANGLES, 36, GL_UNSIGNED_SHORT , self.indices)
		    
		#opengles.glEnable(GL_LIGHTING)
		opengles.glDisable(GL_TEXTURE_2D)
		#restore to previous matrix
		opengles.glLoadMatrixf(mtrx)
	

class createMergeShape(create_shape):
        
        def __init__(self,name="",x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, sx=1.0,sy=1.0,sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createMergeShape,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Creating Merge Shape ..."
                
                self.vertices=[]
                self.normals=[]
                self.tex_coords=[]
                self.indices=[]    #stores all indices for single render
                self.shape=[]
            
        def add(self,shape, x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, sx=1.0,sy=1.0,sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                merge(self,shape, x+shape.x,y+shape.y,z+shape.z, rx+shape.rotx,ry+shape.roty,rz+shape.rotz, sx*shape.sx,sy*shape.sy,sz*shape.sz, cx,cy,cz)

        def cluster(self,shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl):
                #create a cluster of shapes on an elevation map
                for v in range(0,count):
                        x=xpos+random.random()*w - w*0.5 #mapwidth*.9-mapwidth*.5
                        z=zpos+random.random()*d - d*0.5 #mapdepth*.9-mapdepth*.5
                        rh = random.random()*maxscl+minscl
                        rt = random.random()*360.0
                        y=elevmap.calcHeight(-x,-z)+rh*2
                        merge(self,shape, x,y,z, 0,rt,0, rh,rh,rh)
        
        def radialCopy(self, shape, x=0,y=0,z=0, startRadius=2.0, endRadius=2.0, startAngle=0.0, endAngle=360.0, step=12):
            
                st = (endAngle-startAngle) / step
                rst = (endRadius - startRadius) / int(st)
                rd = startRadius
                sta = startAngle
                
                for r in range(0,int(st)):
                    ca = math.cos(sta * rad)
                    sa = math.sin(sta * rad)
                    merge(self,shape, x+ca*rd,y,z+sa*rd, 0,sta,0)
                    sta += st
                    rd += rst
                    
        def draw(self,shapeNo,tex=None):
                opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
                opengles.glNormalPointer( GL_FLOAT, 0, self.norms);             
                if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
                transform(self.x,self.y,self.z, self.rotx,self.roty,self.rotz, self.sx,self.sy,self.sz, self.cx,self.cy,self.cz)                
                opengles.glDrawElements( self.shape[shapeNo][2], self.shape[shapeNo][1], GL_UNSIGNED_SHORT, self.shape[shapeNo][0])
                if tex > 0: texture_off()

        def drawAll(self,tex=None):
                opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
                opengles.glNormalPointer( GL_FLOAT, 0, self.norms);             
                if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
                opengles.glDisable(GL_CULL_FACE)
                transform(self.x,self.y,self.z, self.rotx,self.roty,self.rotz, self.sx,self.sy,self.sz, self.cx,self.cy,self.cz)                
                opengles.glDrawElements( self.shape[0][2], self.totind, GL_UNSIGNED_SHORT, self.inds)
                opengles.glEnable(GL_CULL_FACE)
                if tex > 0: texture_off()

                
class createPlane(create_shape):
        
        def __init__(self,w=1.0,h=1.0, name="", x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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
                
        
        def draw(self,tex=None):
                opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts);
                opengles.glNormalPointer( GL_FLOAT, 0, self.norms);
                if tex > 0: texture_on(tex,self.texcoords,GL_FLOAT)
                transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,1,self.cx,self.cy,self.cz)    
                opengles.glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, self.inds)
                if tex > 0: texture_off()


class createLathe(create_shape):

        def __init__(self,path, sides=12, name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createLathe,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                print "Creating lathe ..."

                self.path = path
                self.sides = sides
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]
            
        def draw(self,tex=None):
		opengles.glDisable(GL_CULL_FACE)
                shape_draw(self,tex)
                opengles.glEnable(GL_CULL_FACE)

class createDisk(create_shape):
    
        def __init__(self,radius=1,sides=12,name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createDisk,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Creating disk ..."

                self.verts=[]
                self.norms=[]
                self.inds=[]
                self.texcoords=[]
                self.ttype = GL_TRIANGLES
                self.sides = sides

                
                st = pipi/slices
                addVertex(self.verts,x,y,z,self.norms,0,1,0,self.texcoords,0.5,0.5)
                for r in range(0,sides+1):
                    ca=math.sin(r*st)
                    sa=math.cos(r*st)
                    addVertex(self.verts,x+radius * ca,y,z+radius * sa,self.norms,0,1,0,self.texcoords,ca*0.5+0.5,sa*0.5+0.5)
                    
                for r in range(0,sides):   
                    addTri(self.inds,0,r+1,r+2)

                self.vertices = eglfloats(self.verts);
                self.indices = eglshorts(self.inds);
                self.normals = eglfloats(self.norms);
                self.tex_coords = eglfloats(self.texcoords);
                self.ssize = sides*3            
        
        def draw(self,tex=None):
                shape_draw(self,tex)        


class createSphere(create_shape):

        def __init__(self,radius=1,slices=12,sides=12,hemi=0.0,name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createSphere,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Creating sphere ..."

                path = []
                st = (pipi*(1.0-hemi))/slices
                for r in range(0,slices+1):
                    path.append((radius * math.sin(r*st),radius * math.cos(r*st)))
                        
                self.radius = radius
                self.slices = slices
                self.sides = sides
                self.hemi = hemi
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self,tex)


class createTorus(create_shape):

        def __init__(self,radius=2.0,thickness=0.5, ringrots=6, sides=12,name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self,tex)

class createTube(create_shape):

        def __init__(self,radius=1.0,thickness=0.5, height=2.0, sides=12,name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self,tex)
                
class createSpiral(create_shape):

        def __init__(self,radius=1.0,thickness=0.2, ringrots=6, sides=12, rise=1.0, loops=2.0, name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createSpiral,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Creating Spiral ...", radius,thickness, ringrots, sides

                path = []
                st = (pipi*2)/ringrots
                hr = rise * 0.5
                for r in range(0,ringrots+1):
                    path.append((radius + thickness * math.sin(r*st),thickness * math.cos(r*st)-hr))
                    print "path:",path[r][0], path[r][1]
                        
                self.radius = radius
                self.thickness = thickness
                self.ringrots = ringrots
                self.sides = sides
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True, rise, loops)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self, tex)
                                
class createCylinder(create_shape):

        def __init__(self,radius=1.0,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self,tex)
                
class createCone(create_shape):

        def __init__(self,radius=1.0,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createCone,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Creating Cone ..."

                path = []
                path.append((0,height * .5))
                path.append((radius, -height * .5))
                path.append((0,-height * .5))
                
                self.radius = radius
                self.height = height
                self.sides = sides
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]

        def draw(self,tex=None):
                shape_draw(self,tex)            
        
class createTCone(create_shape):

        def __init__(self,radiusBot=1.2,radiusTop=0.8,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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
                self.ttype = GL_TRIANGLES
                
                results = lathe(path, sides, True)
                
                self.vertices = eglfloats(results[0])
                self.normals = eglfloats(results[1])
                self.indices = eglshorts(results[2])
                self.tex_coords = eglfloats(results[3])
                self.ssize = results[4]


        def draw(self,tex=None):
                shape_draw(self,tex)

class createExtrude(create_shape):

        def __init__(self, path, height=1.0, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
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

                for p in range (0, s):          #top face indices - triangle fan
                    self.topface.append(p)
                    
                for p in range (0, s):          #bottom face indices - triangle fan
                    b=s+(s-p)
                    print "bi:",b
                    self.botface.append(b-1)
        
                for p in range (0, s):          #sides - triangle strip
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

        def draw(self,tex1=None,tex2=None,tex3=None):
                opengles.glVertexPointer( 3, GL_FLOAT, 0, self.verts)
                opengles.glNormalPointer( GL_FLOAT, 0, self.norms)
		mtrx =(ctypes.c_float*16)()
		opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(mtrx))
                transform(self.x,self.y,self.z,self.rotx,self.roty,self.rotz,self.sx,self.sy,self.sz,self.cx,self.cy,self.cz)
                if tex1 > 0: texture_on(tex1,self.tex_coords,GL_FLOAT)
                opengles.glDrawElements( GL_TRIANGLE_STRIP, self.edges * 2+2, GL_UNSIGNED_SHORT, self.sidefaces)
                if tex2 > 0: texture_on(tex2,self.tex_coords,GL_FLOAT)
                opengles.glDrawElements( GL_TRIANGLE_FAN, self.edges, GL_UNSIGNED_SHORT, self.topface)
                if tex3 > 0: texture_on(tex3,self.tex_coords,GL_FLOAT)
                opengles.glDrawElements( GL_TRIANGLE_FAN, self.edges, GL_UNSIGNED_SHORT, self.botface)
                if tex1 > 0: texture_off()
		opengles.glLoadMatrixf(mtrx)

class createElevationMapFromTexture(create_shape):

        def __init__(self, mapfile, width=100.0, depth=100.0, height=10.0, divx=0, divy=0, ntiles=1.0, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createElevationMapFromTexture,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)
                
                print "Loading height map ...",mapfile
                
                if divx>200 or divy>200:
                        print "... Map size can't be bigger than 200x200 divisions"
                        divx=200
                        divy=200
                        
                im = Image.open(mapfile)
                im = PIL.ImageOps.invert(im)
                ix,iy = im.size
                if (ix>200 and divx==0) or (divx > 0):
                        if divx==0:
                                divx=200
                                divy=200
                        im = im.resize((divx,divy),Image.ANTIALIAS)
                        ix,iy = im.size
                if not im.mode == "P":
                        im = im.convert('P', palette=Image.ADAPTIVE)
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
                self.pixels = im.load()
                self.width = width
                self.depth = depth
                self.height = height
                self.ix=ix
                self.iy=iy
                self.ttype = GL_TRIANGLE_STRIP
                
                print "Creating Elevation Map ...", ix,iy

                wh = width*0.5
                hh = depth*0.5
                ws = width / ix
                hs = depth / iy
                ht = height / 255.0
                tx = ntiles/ix
                ty = ntiles/iy
                
                verts=[]
                norms=[]
                tex_coords=[]
                idx=[]
                
                for y in range(0,iy):
                        for x in range(0,ix):
                                hgt = (self.pixels[x,y])*ht
                                verts.append(-wh+x*ws)
                                verts.append(hgt)
                                verts.append(-hh+y*hs)
                                norms.append(0.0)
                                norms.append(1.0)
                                norms.append(0.0)
                                tex_coords.append((ix-x) * tx)
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
                
        def draw(self,tex=None):
                shape_draw(self,tex)


class clipPlane():
# Added by Patrick Gaunt, 10-07-2012
    
    def __init__(self, no=0, x=0, y=0, z=1, w=60):
	self.no = eglint(GL_CLIP_PLANE0 + no)
	self.equation = eglfloats((x,y,z,w))
	opengles.glClipPlanef(self.no, self.equation)
	
    def enable(self):
	opengles.glEnable(self.no)
	
    def disable(self):
	opengles.glDisable(self.no)
	
#=====================================================================================================================================================================================  
# Cameras
                                
class camera(create_shape):
    
    def __init__(self,name="",x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0):
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

class loadModel(create_shape):
        
    def __init__(self,fileString, texs, name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
        super(loadModel,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

        self.exf = fileString[-3:].lower()
        self.texs = texs
        print "Loading ",fileString
        
        if self.exf == 'egg':
            self.model = loaderEgg.loadFileEGG(self,fileString,texs)
            return self.model
        else:
            print self.exf, "file not supported"
            return None
            
    def draw(self,tex=None,n=None):
        if self.exf == 'egg': loaderEgg.draw(self,tex,n)
        
    def clone(self): 
        newLM = loadModel("__clone__."+self.exf,self.texs)
        newLM.vGroup = self.vGroup
        return newLM
        
    def reparentTo(self, parent):
        if not(self in parent.childModel):  parent.childModel.append(self)
	
    def texSwap(self, texID, filename):
	return loaderEgg.texSwap(self, texID, filename)
            
                                        
#=====================================================================================================================================================================================  
# Lights

class createLight(object):
    
    def __init__(self,no=0,red=1.0,grn=1.0,blu=1.0, name="",x=0,y=0,z=0, ambR=0.5,ambG=0.5,ambB=0.5):

        print "Creating light ..."

	self.ambient = eglfloats((ambR,ambG,ambB,1.0))
	self.diffuse = eglfloats((red,grn,blu,1.0))
	self.specular = eglfloats((red,grn,blu,1.0))
	self.xyz = eglfloats((x,y,z,1))
	self.no = eglint(GL_LIGHT0 + no)
	self.name = name
	#self.mShininess = eglfloat(120.0)
	self.lighton = False
	
	#opengles.glLightModelfv(GL_LIGHT_MODEL_COLOUR_CONTROL, GL_SEPERATE_SPECULAR_COLOR)   #Turns on specular highlights for textures
	#opengles.glMaterialfv(GL_FRONT, GL_SHININESS, self.mShininess)#TIM: don't think this works but would like it to
	opengles.glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient)
	opengles.glLightfv(self.no,GL_AMBIENT, self.ambient) 
	opengles.glLightfv(self.no,GL_DIFFUSE,self.diffuse) 
	opengles.glLightfv(self.no,GL_SPECULAR,self.specular) 
	opengles.glLightfv(self.no,GL_POSITION,self.xyz) 
	# 0 for a distant light and -1 for a spot. LIGHT0 comes predefined as a distant light but that's changed here
	# I would have thought either w needs to be passed as a parameter to __init__ and not overwritten in position
	# and/or define global values SPOT, DIST, POINT = -1, 0, 1


    def position(self,x,y,z):

	mtrx =(ctypes.c_float*16)()
	opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(mtrx))
	opengles.glLoadIdentity()
	self.xyz = eglfloats((x,y,z,1))
	opengles.glLightfv(self.no, GL_POSITION,self.xyz)
	opengles.glLoadMatrixf(mtrx)
    
    def on(self):
	#load view matrix
	opengles.glEnable(GL_LIGHTING)
	opengles.glEnable(self.no)
	opengles.glLightfv(self.no,GL_POSITION,self.xyz) #TIM: fv
	self.lighton = True

    def off(self):
	opengles.glDisable(self.no)
	opengles.glDisable(GL_LIGHTING)
	self.lighton = False

class fog():
# By paddywwoof
# 12-12-2012
    def __init__(self, density=0.005, colour=(0.3, 0.6, 0.8, 0.5)):
        opengles.glFogf(GL_FOG_MODE, GL_EXP) # defaults to this anyway
        opengles.glFogf(GL_FOG_DENSITY, eglfloat(density)) # exponent factor
        opengles.glFogfv(GL_FOG_COLOR, eglfloats(colour)) # don't think the alpha value alters the target object alpha
	
    def on(self):
        opengles.glEnable(GL_FOG)
	
    def off(self):
        opengles.glDisable(GL_FOG)
	
#=====================================================================================================================================================================================  
# Text and fonts
# NEEDS FIXING - TEXTURES NEED CLEANING UP

class font(object):
    
    def __init__(self,font,col="#ffffff"):
        self.font=font
        im = Image.open("fonts/"+font+".png")
        ix,iy = im.size
        pixels = im.load()
                
        self.chr = []
        #extract font information from top scanline of font image;
        #Create width,height,tex_coord and vertices for each char ...
        for v in range(0,95):
            x=(pixels[v*2,0][0] * 2.0)/ix  #x coord in image for this char
            y=((pixels[v*2,0][1]+8) * 2.0)/iy  #y coord in image for this char
            w=pixels[v*2+1,0][0] * 1.0   #width of this char
            h=pixels[v*2+1,0][1] * 1.0   #height of this char
            tw=w/ix
            th=h/iy
            #print chr(v+32),x,y,w,h,tw,th
            self.chr.append((w,h,eglfloats((x+tw,y-th, x,y-th, x,y, x+tw,y)),eglfloats((w,0,0, 0,0,0, 0,-h,0, w,-h,0))))

        alpha = im.split()[-1]  #keep alpha
        draw = ImageDraw.Draw(im)
        draw.rectangle((0,1,ix,iy),fill=col)
        im.putalpha(alpha)
        
        #im = im.transpose(Image.FLIP_TOP_BOTTOM)
        image = im.convert("RGBA").tostring("raw","RGBA")
        self.tex=eglint()
        opengles.glGenTextures(1,ctypes.byref(self.tex))
        opengles.glBindTexture(GL_TEXTURE_2D,self.tex)
        opengles.glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,ix,iy,0,GL_RGBA,GL_UNSIGNED_BYTE, ctypes.string_at(image,len(image)))
        

#=====================================================================================================================================================================================  
# Odd classes

class missile(object):
    def __init__(self):
        self.isActive = False
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0
        self.countDown=0
    
    def fire(self, x,y,z, dx,dy,dz, rx,ry,rz, cnt=0):
        self.isActive = True
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.countDown = cnt
        
    def move(self,missile,tex,dy=0.0,dx=0.0,dz=0.0):
        if dx==0.0: self.x += self.dx
        else: self.x=dx
        if dy==0.0: self.y += self.dy
        else: self.y=dy
        if dz==0.0: self.z += self.dz
        else: self.z=dz
        if self.countDown > 0:
            self.countDown -= 1
            if self.countDown == 0:
                print "fizzle"
                self.IsActive = False
        missile.x = self.x
        missile.y = self.y
        missile.z = self.z
        missile.rotx = self.rx
        missile.roty = self.ry
        missile.rotz = self.rz
        missile.draw(tex)

class ball(object):
    
    def __init__(self,radius,x,y,vx=0.0,vy=0.0,decay=0.001):
	self.radius=radius
	self.x=x
	self.y=y
	self.x=x
	self.vx = vx
	self.vy = vy
	self.mass =radius*2
	self.decay = decay
	
    def hit(self,otherball):
	#used for pre-checking ball positions
	dx = (self.x+self.vx)-(otherball.x+otherball.vx)
	dy = (self.y+self.vy)-(otherball.y+otherball.vy)
	rd = self.radius+otherball.radius
	if (dx**2+dy**2) <= (rd**2): return True
	else: return False
	
    def collisionBounce(self,otherball):
	dx = self.x-otherball.x
	dy = self.y-otherball.y
	rd = self.radius+otherball.radius
	#print dx,dy #,self.x,otherball.x
	if (dx**2+dy**2) <= (rd**2):
	    #sq = 1.0 / math.sqrt(dx**2+dy**2)
	    #print "dxdy", dx**2+dy**2
	    #otherball.vx = math.copysign((dx*sq),self.vx)*5.0
	    #otherball.vy = math.copysign((dy*sq),self.vy)*5.0
	    #self.vx = 0.0 #math.copysign(abs(dy*sq),self.vx)
	    #self.vy = 0.0 #-math.copysign(abs(dx*sq),self.vy)
	    
	    cangle = math.atan2(dy,dx)
	    mag1 = math.sqrt(self.vx**2+self.vy**2)
	    mag2 = math.sqrt(otherball.vx**2+otherball.vy**2)
	    dir1 = math.atan2(self.vy,self.vx)
	    dir2 = math.atan2(otherball.vy,otherball.vx)
	    nspx1 = mag1 * math.cos(dir1-cangle)
	    nspy1 = mag1 * math.sin(dir1-cangle)
	    nspx2 = mag2 * math.cos(dir2-cangle)
	    nspy2 = mag2 * math.sin(dir2-cangle)
	    fspx1 = ((self.mass-otherball.mass)*nspx1+(otherball.mass*2)*nspx2)/(self.mass+otherball.mass)
	    fspx2 = ((self.mass*2)*nspx1+(otherball.mass-self.mass)*nspx2)/(self.mass+otherball.mass)
	    fspy1 = nspy1
	    fspy2 = nspy2
	    self.vx = math.cos(cangle)*fspx1+math.cos(cangle+pipi*.5)*fspy1
	    self.vy = math.sin(cangle)*fspx1+math.sin(cangle+pipi*.5)*fspy1
	    otherball.vx = math.cos(cangle)*fspx2+math.cos(cangle+pipi*.5)*fspy2
	    otherball.vy = math.sin(cangle)*fspx2+math.sin(cangle+pipi*.5)*fspy2

    
class shader(object):

# This class based on Peter de Rivaz's mandlebrot example

	def showlog(self,shader):
	    """Prints the compile log for a shader"""
	    N=1024
	    log=(ctypes.c_char*N)()
	    loglen=ctypes.c_int()
	    opengles.glGetShaderInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
	    print "Shader log:",log.value

	def showprogramlog(self,shader):
	    """Prints the compile log for a shader"""
	    N=1024
	    log=(ctypes.c_char*N)()
	    loglen=ctypes.c_int()
	    opengles.glGetProgramInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
	    print log.value
            
    
	def __init__(self, vshader_source, fshader_source, tex1=None, tex2=None, param1=None, param2=None, param3=None):
		
	    #Pi3D can only accept shaders with limited parameters as specific parameters
	    #would require a lot more coding unless there's a way of passing these back.
	    #Shaders should have their parameters defined in the shader source.
	    #The only parameters Pi3D can pass (for now) is textures.

	    self.vshader_source = ctypes.c_char_p(
              "attribute vec4 vertex;"
              "varying vec2 tcoord;"
              "void main(void) {"
              "  vec4 pos = vertex;"
              "  pos.xy*=0.9;"
              "  gl_Position = pos;"
              "  tcoord = vertex.xy*0.5+0.5;"
              "}")
	      	    
	    self.tex1 = tex1
	    self.tex2 = tex2
	    
	    vshads = ctypes.c_char_p(vshader_source)
	    fshads = ctypes.c_char_p(fshader_source)
	    
	    vshader = opengles.glCreateShader(GL_VERTEX_SHADER)
	    opengles.glShaderSource(vshader, 1, ctypes.byref(self.vshader_source), 0)
	    opengles.glCompileShader(vshader)
	    self.showlog(vshader)
	    
	    fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER)
	    opengles.glShaderSource(fshader, 1, ctypes.byref(fshads), 0)
	    opengles.glCompileShader(fshader)
	    self.showlog(fshader)

	    self.program = opengles.glCreateProgram()
	    opengles.glAttachShader(self.program, vshader)
	    opengles.glAttachShader(self.program, fshader)
	    opengles.glLinkProgram(self.program)
	    self.showprogramlog(self.program)

	def use(self):
	    if self.tex1<>None: unif_tex1 = opengles.glGetUniformLocation(self.program, "tex1")  #frag shader must have a uniform 'tex1'
	    if self.tex2<>None: unif_tex2 = opengles.glGetUniformLocation(self.program, "tex2")  #frag shader must have a uniform 'tex2'
	    opengles.glUseProgram ( self.program );

        #self.program = program
        #self.unif_color = opengles.glGetUniformLocation(program, "color");
        #self.attr_vertex = opengles.glGetAttribLocation(program, "vertex");
        #self.unif_scale = opengles.glGetUniformLocation(program, "scale");
        #self.unif_offset = opengles.glGetUniformLocation(program, "offset");
        #self.unif_tex = opengles.glGetUniformLocation(program, "tex");




