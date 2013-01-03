from numpy import array, dot, copy, tan, cos, sin, radians
from numpy.linalg import norm
from pi3d import *
from pi3d.shape.Shape import Shape
from pi3d.util.DefaultInstance import DefaultInstance
from pi3d.util.Utility import vec_normal, vec_cross, vec_sub, vec_dot

class Camera(DefaultInstance):
  def __init__(self, at, eye, lens):
    """Set up view matrix to look from eye to at including perspective
    at   -- (x,y,z) location to look at
    eye  -- (x,y,z) location to look from
    lens -- (near plane distance, far plane value, field of view width,
            field of view height) fields of view in radians
    """
    super(Camera, self).__init__()

    self.eye = [eye[0], eye[1], eye[2]]
    self.view = LookAtMatrix(at,eye,[0,1,0])
    self.projection = ProjectionMatrix(lens[0], lens[1], lens[2], lens[3])
    #self.mtrx = [row[:] for row in self.model_view]
    self.model_view = dot(self.view, self.projection)
    # Apply transform/rotation first, then shift into perspective space.
    self.mtrx = copy(self.model_view)
    # self.L_reflect = LookAtMatrix(at,eye,[0,1,0],reflect=True)
    self.rtn = [0.0, 0.0, 0.0]

    # self.c_floats will eventually hold the cfloats array for quicker passing
    # to shader in Shape.draw().
    self.c_floats = None
    self.was_moved = True

  @staticmethod
  def _default_instance():
    from pi3d.Display import DISPLAY
    return Camera((0, 0, 0), (0, 0, -1),
                  (1, 1000, DISPLAY.width / 1000.0, DISPLAY.height / 1000.0))

  def reset(self):
    self.mtrx = copy(self.model_view)
    self.rtn = [0.0, 0.0, 0.0]
    self.c_floats = None
    self.was_moved = True

  def copy(self,copyMatrix):
    self.mtrx = copy(copyMatrix)
    # Usually copies the model_view matrix to begin with.

  def copynew(self):
    return copy(self.mtrx)

  def identity(self):
    self.mtrx = array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], dtype=c_float)

  def translate(self, pt):
    # TODO this should really be called position
    self.mtrx = dot([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [-pt[0], -pt[1], -pt[2], 1]],
                    self.mtrx)
    self.eye = [pt[0], pt[1], pt[2]]
    self.c_floats = None
    self.was_moved = True

  def rotateZ(self, angle):
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[c, s, 0, 0],
                       [-s, c, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]],
                      self.mtrx)
      self.rtn[2] = angle
      self.c_floats = None
      self.was_moved = True

  def rotateY(self, angle):
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[c, 0, -s, 0],
                       [0, 1, 0, 0],
                       [s, 0, c, 0],
                       [0, 0, 0, 1]],
                      self.mtrx)
      self.rtn[1] = angle
      self.c_floats = None
      self.was_moved = True

  def rotateX(self, angle):
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[1, 0, 0, 0],
                       [0, c, s, 0],
                       [0, -s, c, 0],
                       [0, 0, 0, 1]], self.mtrx)
      self.rtn[0] = angle
      self.c_floats = None
      self.was_moved = True

  def rotate(self, rx, ry, rz):
    self.rotateZ(rz)
    self.rotateX(rx)
    self.rotateY(ry)

def LookAtMatrix(at, eye, up=[0,1,0], reflect=False):
  """Define a matrix of an eye looking at"""
  # If reflect, then reflect in plane -20.0 (water depth)
  if reflect:
    depth = -20.0 # Shallower to avoid edge effects
    eye[2] = 2 * depth - eye[2]
    at[2] = 2 * depth - at[2]
  zaxis = vec_normal(vec_sub(at, eye))
  xaxis = vec_normal(vec_cross(up, zaxis))
  yaxis = vec_cross(zaxis, xaxis)
  xaxis.append(-vec_dot(xaxis, eye))
  yaxis.append(-vec_dot(yaxis, eye))
  zaxis.append(-vec_dot(zaxis, eye))
  z = [0, 0, 0, 1.0]
  #TODO all using numpy functions
  return array([[xaxis[a], yaxis[a], zaxis[a], z[a]] for a in range(4)],
               dtype=c_float)
  #return array([xaxis,yaxis,zaxis,z])

def ProjectionMatrix(near=10, far=1000.0, fov_w=1.6, fov_h=1.2):
  """Setup projection matrix with given distance to near and far planes
  and fields of view in radians"""
  # Matrices are considered to be M[row][col]
  # Use DirectX convention, so need to do rowvec*Matrix to transform
  #w = 1.0 / tan(fov_w * 0.5)
  #h = 1.0 / tan(fov_h * 0.5)
  w = 2.0 / fov_w
  h = 2.0 / fov_h
  q = far / (far - near)
  M = [[0] * 4 for i in range(4)]
  M[0][0] = w
  M[1][1] = h
  M[2][2] = q
  M[3][2] = -q * near
  M[2][3] = 1
  #M[2][3] = -q * near
  #M[3][2] = 1
  #TODO all using numpy functions
  return array(M, dtype=c_float)

