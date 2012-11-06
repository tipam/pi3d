# pi3D module
# ===========
# Version 0.06
#
# Copyright (c) 2012, Tim Skillman, Tom Swirly
# (Some code initially based on Peter de Rivaz pyopengles example.)
#
#    www.github.com/rec/pi3d
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

import math
import os.path
import random
import sys

import PIL.ImageOps, ImageDraw

from pi3d.pi3dCommon import *

from pi3d import loaderEgg
from pi3d import Constants

from pi3d.Display import Display

CUBE_PARTS = ('top', 'left', 'front', 'right', 'back', 'bottom')

def loadECfiles(path, fname, textures):
  # Helper for loading environment cube faces.
  files = (os.path.join(path, '%s_%s.jpg' % (fname, p)) for p in CUBE_PARTS)
  return [textures.loadTexture(f) for f in files]

class createCylinder(Shape):

        def __init__(self,radius=1.0,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createCylinder,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                if Constants.VERBOSE:
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

class createCone(Shape):

        def __init__(self,radius=1.0,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createCone,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                if Constants.VERBOSE:
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

class createTCone(Shape):

        def __init__(self,radiusBot=1.2,radiusTop=0.8,height=2.0,sides=12, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createTCone,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                if Constants.VERBOSE:
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

class createExtrude(Shape):

        def __init__(self, path, height=1.0, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createExtrude,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                if Constants.VERBOSE:
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
                    if Constants.VERBOSE:
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

class createElevationMapFromTexture(Shape):

        def __init__(self, mapfile, width=100.0, depth=100.0, height=10.0, divx=0, divy=0, ntiles=1.0, name="",x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
                super(createElevationMapFromTexture,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

                if Constants.VERBOSE:
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

                if Constants.VERBOSE:
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
                if Constants.VERBOSE:
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

class camera(Shape):

    def __init__(self,name="",x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0):
        super(camera,self).__init__(name, x,y,z, rx,ry,rz, 1,1,1)
        if Constants.VERBOSE:
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

class loadModel(Shape):

    def __init__(self,fileString, texs, name="", x=0.0,y=0.0,z=0.0, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, cx=0.0,cy=0.0,cz=0.0):
        super(loadModel,self).__init__(name, x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz)

        self.exf = fileString[-3:].lower()
        self.texs = texs
        if Constants.VERBOSE:
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

        if Constants.VERBOSE:
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
                if Constants.VERBOSE:
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

	if (dx**2+dy**2) <= (rd**2):
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
	    self.vx = math.cos(cangle)*fspx1+math.cos(cangle+math.pi*.5)*fspy1
	    self.vy = math.sin(cangle)*fspx1+math.sin(cangle+math.pi*.5)*fspy1
	    otherball.vx = math.cos(cangle)*fspx2+math.cos(cangle+math.pi*.5)*fspy2
	    otherball.vy = math.sin(cangle)*fspx2+math.sin(cangle+math.pi*.5)*fspy2


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
            if Constants.VERBOSE:
              self.showlog(vshader)

	    fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER)
	    opengles.glShaderSource(fshader, 1, ctypes.byref(fshads), 0)
	    opengles.glCompileShader(fshader)
            if Constants.VERBOSE:
              self.showlog(fshader)

	    self.program = opengles.glCreateProgram()
	    opengles.glAttachShader(self.program, vshader)
	    opengles.glAttachShader(self.program, fshader)
	    opengles.glLinkProgram(self.program)
            if Constants.VERBOSE:
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




