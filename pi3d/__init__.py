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




