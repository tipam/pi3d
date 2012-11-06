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




