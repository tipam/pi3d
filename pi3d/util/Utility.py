import math
import numpy

from numpy import sqrt, sin, cos, tan, subtract, dot

from pi3d.constants import *
from pi3d.util.Ctypes import c_bytes

RECT_NORMALS = c_bytes((0, 0, -1,
                        0, 0, -1,
                        0, 0, -1,
                        0, 0, -1))

RECT_TRIANGLES = c_bytes((3, 0, 1,
                          3, 1, 2))

def rect_triangles():
  opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, RECT_TRIANGLES)

# TODO: not exact sure what this does but we do it a lot.
def texture_min_mag():
  for f in [GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER]:
    opengles.glTexParameterf(GL_TEXTURE_2D, f, ctypes.c_float(GL_LINEAR))

def sqsum(*args):
  """Return the sum of the squares of its arguments.

  DEPRECATED:  use numpy.dot(x, x).
  """
  return numpy.dot(args, args)

def magnitude(*args):
  """Return the magnitude (root mean square) of the vector."""
  return numpy.sqrt(numpy.dot(args, args))

def distance(v1, v2):
  """Return the distance between two points."""
  return magnitude(*subtract(v2, v1))

def from_polar(direction=0.0, magnitude=1.0):
  """
  Convert polar coordinates into Cartesian (x, y) coordinates.

  Arguments:

  *direction*
    Vector angle in degrees.
  *magnitude*
    Vector length.
  """
  return from_polar_rad(math.radians(direction), magnitude)

def from_polar_rad(direction=0.0, magnitude=1.0):
  """
  Convert polar coordinates into Cartesian (x, y) coordinates.

  Arguments:

  *direction*
    Vector angle in radians.
  *magnitude*
    Vector length.
  """
  return magnitude * numpy.cos(direction), magnitude * numpy.sin(direction)

def load_identity():
  opengles.glLoadIdentity()

# TODO: how many dot and cross products do we need?!
def dotproduct(x1 ,y1, z1, x2, y2, z2):
  return x1 * x2 + y1 * y2 + z1 * z2

def crossproduct(x1, y1, z1, x2, y2, z2):
  return y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2

#------------------------------
def TranslateMatrix(pt):
  M=[[0] * 4 for i in range(4)]
  for i in range(4):
    M[i][i] = 1.0
  for i in range(3):
    M[3][i] = pt[i]
  return M

# TODO: shouldn't this all be numpy?
def vec_sub(x, y):
  return [a - b for a, b in zip(x, y)]

def vec_dot(x, y):
  return sum(a * b for a, b in zip(x, y))

def vec_cross(a,b):
  return [a[1] * b[2] - a[2] * b[1],
          a[2] * b[0] - a[0] * b[2],
          a[0] * b[1] - a[1] * b[0]]

def vec_normal(A):
  n = sqrt(sum(a ** 2 for a in A)) + 0.0001
  return [a/n for a in A]

def BillboardMatrix():
  """Define a matrix that copies x,y and sets z to 0.9"""
  return [[1.0, 0.0, 0.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.9, 1.0]]

def mat_mult(A,B):
  return [[sum(A[i][j] * B[j][k] for j in range(4))
           for k in range(4)] for i in range(4)]

def mat_transpose(A):
  return [[A[k][i] for k in range(4)] for i in range(4)]

def vec_mat_mult(A,B):
  return [sum(A[j] * B[j][k] for j in range(4)) for k in range(4)]

def transform(origmtrx,x,y,z,rx,ry,rz,sx,sy,sz,cx,cy,cz):
  mtrx = [row[:] for row in origmtrx]
  mtrx = translate(mtrx,(x-cx,y-cy,z-cz))
  mtrx = rotate(mtrx,rx,ry,rz)
  if sx<>1.0 or sy<>1.0 or sz<>1.0: mtrx = scale(mtrx,sx,sy,sz)
  return translate(mtrx,(cx,cy,cz))

def scale(mtrx,sx,sy,sz):
  return mat_mult([[sx,0,0,0],[0,sy,0,0],[0,0,sz,0],[0,0,0,1]],mtrx)

def translate(mtrx,pt):
  #mtrx[3]=[sum(pt[j]*mtrx[j][i] for j in xrange(3))+mtrx[3][i] for i in xrange(4)]
  #return mtrx
  return mat_mult([[1,0,0,0],[0,1,0,0],[0,0,1,0],[pt[0],pt[1],pt[2],1]], mtrx)

def rotate(mtrx,rx,ry,rz):
  if rz<>0.0: mtrx=rotateZ(mtrx,rz)
  if rx<>0.0: mtrx=rotateX(mtrx,rx)
  if ry<>0.0: mtrx=rotateY(mtrx,ry)
  return mtrx

def rotateX(mtrx,angle):
  angle = math.radians(angle)
  c = cos(angle)
  s = sin(angle)
  return mat_mult([[1,0,0,0],[0,c,s,0],[0,-s,c,0],[0,0,0,1]],mtrx)

def rotateY(mtrx,angle):
  angle = math.radians(angle)
  c = cos(angle)
  s = sin(angle)
  return mat_mult([[c,0,-s,0],[0,1,0,0],[s,0,c,0],[0,0,0,1]],mtrx)

def rotateZ(mtrx,angle):
  angle = math.radians(angle)
  c = cos(angle)
  s = sin(angle)
  return mat_mult([[c,s,0,0],[-s,c,0,0],[0,0,1,0],[0,0,0,1]],mtrx)

def angleVecs(x1,y1,x2,y2,x3,y3):
    a = x2-x1
    b = y2-y1
    c = x2-x3
    d = y2-y3

    sqab = sqrt(a*a+b*b)
    sqcd = sqrt(c*c+d*d)
    l = sqab*sqcd
    if l == 0.0:
      l = 0.0001
    aa = ((a*c)+(b*d)) / l
    if aa == -1.0:
      return math.pi
    if aa == 0.0:
      return 0.0
    dist = (a*y3 - b*x3 + x1*b - y1*a) / sqab
    angle = acos(aa)

    if dist > 0.0:
      return math.pi / 2.0 - angle
    else:
      return angle

def lodDraw(here, there, mlist):
  """Level Of Detail checking and rendering. NB this will only work if the shader
  and texture information has been set for all the buf object in the model.
  No return value

  Arguments:
    *here*
      (x,y,z) tuple or array of view point
    *there*
      (x,y,z) tuple or array of model position
    *mlist*
      array of arrays with distance and model pairs. i.e. [[20, model1],[100, model2],[250, None]]
      Model is used up to that distance until the last entry then for all distances beyond,
      'None' can be used to draw nothing at a certain distance
  """
  dist = distance(here, there)
  for model in mlist:
    if dist < model[0]:
      if not (model[1] == None):
        model[1].position(there[0], there[1], there[2])
        model[1].draw()
      return

  # dist is more than any model dist so draw last
  model = mlist[len(mlist) - 1]
  if not (model[1] == None):
    model[1].position(there[0], there[1], there[2])
    model[1].draw()


"""
# TODO: None of these functions is actually called in the codebase.

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

def rotate(rotx, roty, rotz):
  # TODO: why the reverse order?
  rotatef(rotz, 0, 0, 1)
  rotatef(roty, 0, 1, 0)
  rotatef(rotx, 1, 0, 0)
"""
