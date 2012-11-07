# pi3D common module
# ==================
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

import ctypes, math, threading

from ctypes import c_byte
from ctypes import c_float
from ctypes import c_int
from ctypes import c_short

from pi3d import Constants

# Pick up our constants extracted from the header files with prepare_constants.py
from constants.egl import *
from constants.gl2 import *
from constants.gl2ext import *
from constants.gl import *

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

def ctypes_array(ct, x):
  return (ct * len(x))(*x)

def c_bytes(x):
  return ctypes_array(c_byte, x)

def c_ints(x):
  return ctypes_array(c_int, x)

def c_floats(x):
  return ctypes_array(c_float, x)

def c_shorts(x):
  return ctypes_array(c_short, x)

# TODO: not exact sure what this does but we do it a lot.
def texture_min_mag():
  for f in [GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER]:
    opengles.glTexParameterf(GL_TEXTURE_2D, f, c_float(GL_LINEAR))

def sqsum(*args):
  return sum(x * x for x in args)

def magnitude(*args):
  return math.sqrt(sqsum(*args))

def from_polar(direction=0.0, magnitude=1.0):
  return from_polar_rad(math.radians(direction), magnitude)

def from_polar_rad(direction=0.0, magnitude=1.0):
  return magnitude * math.cos(direction), magnitude * math.sin(direction)

def rotatef(angle, x, y, z):
  if angle:
    opengles.glRotatef(c_float(angle), c_float(x), c_float(y), c_float(z))

def translatef(x, y, z):
  opengles.glTranslatef(c_float(x), c_float(y), c_float(z))

def scalef(sx, sy, sz):
  opengles.glScalef(c_float(sx), c_float(sy), c_float(sz))

def load_identity():
  opengles.glLoadIdentity()

# position, rotate and scale an object
def transform(x, y, z, rotx, roty, rotz, sx, sy, sz, cx, cy, cz):
  translatef(x - cx, y - cy, z - cz)

  # TODO: why the reverse order?
  rotatef(rotz, 0, 0, 1)
  rotatef(roty, 0, 1, 0)
  rotatef(rotx, 1, 0, 0)
  scalef(sx, sy, sz)
  translatef(cx, cy, cz)

def rotate(rotx, roty, rotz):
  # TODO: why the reverse order?
  rotatef(rotz, 0, 0, 1)
  rotatef(roty, 0, 1, 0)
  rotatef(rotx, 1, 0, 0)

def normalize_vector(begin, end):
  diff = [e - b for b, e in zip(begin, end)]
  mag = magnitude(*diff)
  return [(x / mag if mag > 0.0 else 0.0) for x in diff]

def intersect_triangle(v1, v2, v3, pos):
  #Function calculates the y intersection of a point on a triangle

  #Z order triangle
  if v1[2] > v2[2]:
    v1, v2 = v2, v1

  if v1[2] > v3[2]:
    v1, v3 = v3, v1

  if v2[2] > v3[2]:
    v2, v3 = v3, v2

  if pos[2] > v2[2]:
    #test bottom half of triangle
    if pos[2] > v3[2]:
      #print "z below triangle"
      return -100000  # point completely out

    za = (pos[2] - v1[2]) / (v3[2] - v1[2])
    dxa = v1[0] + (v3[0] - v1[0]) * za
    dya = v1[1] + (v3[1] - v1[1]) * za

    zb = (v3[2] - pos[2]) / (v3[2] - v2[2])
    dxb = v3[0] - (v3[0] - v2[0]) * zb
    dyb = v3[1] - (v3[1] - v2[1]) * zb
    if (pos[0] < dxa and pos[0] < dxb) or (pos[0] > dxa and pos[0] > dxb):
      #print "outside of bottom triangle range"
      return -100000
  else:
    #test top half of triangle
    if pos[2] < v1[2]:
        #print "z above triangle",pos[2],v1[2]
        return -100000  # point completely out
    za = (pos[2] - v1[2]) / (v3[2] - v1[2])
    dxa = v1[0] + (v3[0] - v1[0]) * za
    dya = v1[1] + (v3[1] - v1[1]) * za

    zb = (v2[2] - pos[2]) / ((v2[2] + 0.00001) - v1[2])  #get rid of FP error!
    dxb = v2[0] - (v2[0] - v1[0]) * zb
    dyb = v2[1] - (v2[1] - v1[1]) * zb
    if (pos[0] < dxa and pos[0] < dxb) or (pos[0] > dxa and pos[0] > dxb):
      #print "outside of top triangle range"
      return -100000

  #return resultant intersecting height
  return dya + (dyb - dya) * ((pos[0] - dxa)/(dxb - dxa))

def rotate_vec(rx, ry, rz, xyz):
  x, y, z = xyz
  if rx:
    ca, sa = from_polar(rx)
    yy = y * ca-z * sa
    z = y * sa+z * ca
    y = yy

  if ry:
    ca, sa = from_polar(ry)
    zz = z * ca - x * sa
    x = z * sa + x * ca
    z = zz

  if rz:
    ca, sa = from_polar(rz)
    xx = x * ca - y * sa
    y = x * sa + y * ca
    x = xx

  return x, y, z

def rotate_vec_x(r, x, y, z):
  ca, sa = from_polar(r)
  return x, y * ca - z * sa, y * sa + z * ca

def rotate_vec_y(r, x, y, z):
  ca, sa = from_polar(r)
  return z * sa + x * ca, y, z * ca - x * sa

def rotate_vec_z(r,x,y,z):
  ca, sa = from_polar(r)
  return x * ca - y * sa, x * sa + y * ca, z

# TODO: should be a method on Shape.
def addVertex(v, x, y, z, n, nx, ny, nz, t, tx, ty):
# add vertex,normal and tex_coords ...
  v.extend([x, y, z])
  n.extend([nx, ny, nz])
  t.extend([tx, ty])

# TODO: should be a method on Shape.
def addTri(v, x, y, z):
# add triangle refs.
  v.extend([x, y, z])

# TODO: Should be a method on shape.
def shape_draw(self, tex, shl=GL_UNSIGNED_SHORT):
  from pi3d import Texture
  opengles.glShadeModel(GL_SMOOTH)
  opengles.glVertexPointer(3, GL_FLOAT, 0, self.vertices)
  opengles.glNormalPointer(GL_FLOAT, 0, self.normals)
  with Texture.Loader(tex, self.tex_coords):
    mtrx = (c_float * 16)()
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
    transform(self.x, self.y, self.z, self.rotx, self.roty, self.rotz,
              self.sx, self.sy, self.sz, self.cx, self.cy, self.cz)
    opengles.glDrawElements( self.ttype, self.ssize, shl , self.indices)
    opengles.glLoadMatrixf(mtrx)

# Should be a function in shape.
def lathe(path, sides = 12, tris = False, rise = 0.0, coils = 1.0):
  s = len(path)
  rl = int(sides * coils)
  if tris:
    ssize = rl * 6 * (s - 1)
  else:
    ssize = rl * 2 * (s - 1) + (s * 2) - 2

  pn = 0
  pp = 0
  tcx = 1.0 / sides
  pr = (math.pi / sides) * 2
  rdiv = rise / rl
  ss = 0

  #find largest and smallest y of the path used for stretching the texture over
  p = [i[1] for i in path]
  miny = min(*p)
  maxy = max(*p)

  verts = []
  norms = []
  idx = []
  tex_coords = []

  opx = path[0][0]
  opy = path[0][1]

  for p in range(s):
    px = path[p][0]
    py = path[p][1]

    tcy = 1.0 - ((py - miny) / (maxy - miny))

    #normal between path points
    dx, dy = normalize_vector((opx, opy), (px, py))

    for r in range (0, rl):
      cosr, sinr = from_polar_rad(pr * r)
      # TODO: why the reversal?

      verts.extend([px * sinr, py, px * cosr])
      norms.extend([-sinr * dy, dx, -cosr * dy])
      tex_coords.extend([tcx * r, tcy])
      py += rdiv

    #last path profile (tidies texture coords)
    verts.extend([0, py, px])
    norms.extend([0, dx, -dy])
    tex_coords.extend([1.0, tcy])

    if p < s-1:
      if tris:
        # Create indices for GL_TRIANGLES
        pn += (rl + 1)
        for r in range(rl):
          idx.extend([pp + r + 1, pp + r,
                      pn + r, pn + r,
                      pn + r + 1, pp + r + 1])
          ss += 6
        pp += (rl + 1)
      else:
        #Create indices for GL_TRIANGLE_STRIP
        pn += (rl + 1)
        for r in range(rl):
          idx.extend([pp + r, pn + r])
          ss += 2
        idx.extend([pp + sides, pn + sides])
        ss += 2
        pp += (rl + 1)

    opx = px
    opy = py

  if Constants.VERBOSE:
    print ssize, ss
  return (verts, norms, idx, tex_coords, ssize)

# TODO: Nothing below this line is ever actually called.

def ctype_resize(array, new_size):
  resize(array, sizeof(array._type_) * new_size)
  return (array._type_ * new_size).from_address(addressof(array))

def showerror():
  return opengles.glGetError()

def limit(x, below, above):
  return max(min(x, above), below)

def angle_vecs(x1, y1, x2, y2, x3, y3):
  a = x2 - x1
  b = y2 - y1
  c = x2 - x3
  d = y2 - y3

  sqab = magnitude(a, b)
  sqcd = magnitude(c, d)
  l = sqab * sqcd
  if l == 0.0:  # TODO: comparison between floats.
    l = 0.0001
  aa = ((a * c) + (b * d)) / l
  if aa == -1.0:  # TODO: comparison between floats.
    return math.pi
  if aa == 0.0:   # TODO: comparison between floats.
    return 0.0
  dist = (a * y3 - b * x3 + x1 * b - y1 * a) / sqab
  angle = math.acos(aa)

  if dist > 0.0:
    return math.pi * 2 - angle
  else:
    return angle

def calc_normal(x1, y1, z1, x2, y2, z2):
  dx = x2 - x1
  dy = y2 - y1
  dz = z2 - z1
  mag = magnitude(dx, dy, dz)
  return (dx / mag, dy / mag, dz / mag)

