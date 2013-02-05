import ctypes

from echomesh.util.DefaultInstance import DefaultInstance

from numpy import array, dot, copy, tan, cos, sin, radians
from numpy.linalg import norm

from pi3d.constants import *
from pi3d.Shape import Shape
from pi3d.util.Utility import vec_normal, vec_cross, vec_sub, vec_dot

class Camera(DefaultInstance):
  """required object for creating and drawing Shape objects. Default instance
  created if none specified in script prior to creating a Shape
  """
  def __init__(self, at, eye, lens):
    """Set up view matrix to look from eye to at including perspective

    Arguments:
      *at*
        tuple (x,y,z) location to look at
      *eye*
        tuple (x,y,z) location to look from
      *lens*
        tuple (near plane distance, far plane value, field of view width,
        field of view height) fields of view in radians
    """
    super(Camera, self).__init__()

    self.at = at
    self.start_eye = eye # for reset with different lens settings
    self.eye = [eye[0], eye[1], eye[2]]
    self.lens = lens
    self.view = _LookAtMatrix(at, eye, [0,1,0])
    self.projection = _ProjectionMatrix(lens[0], lens[1], lens[2], lens[3])
    self.model_view = dot(self.view, self.projection)
    # Apply transform/rotation first, then shift into perspective space.
    self.mtrx = copy(self.model_view)
    # self.L_reflect = _LookAtMatrix(at,eye,[0,1,0],reflect=True)
    self.rtn = [0.0, 0.0, 0.0]

    self.was_moved = True

  @staticmethod
  def _default_instance():
    from pi3d.Display import Display
    return Camera((0, 0, 0), (0, 0, -1),
                  (1, 1000,
                   Display.INSTANCE.width / 1000.0,
                   Display.INSTANCE.height / 1000.0))

  def reset(self, lens=None):
    """Has to be called each loop if the camera position or rotation changes"""
    if lens != None:
      view = _LookAtMatrix(self.at, self.start_eye, [0,1,0])
      projection = _ProjectionMatrix(lens[0], lens[1], lens[2], lens[3])
      self.model_view = dot(view, projection)
    # TODO some way of resetting to original matrix
    self.mtrx = copy(self.model_view)
    self.rtn = [0.0, 0.0, 0.0]
    self.was_moved = True

  def position(self, pt):
    """position camera
    
    Arguments:
      *pt*
        tuple (x, y, z) floats
    """
    self.mtrx = dot([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [-pt[0], -pt[1], -pt[2], 1]],
                    self.mtrx)
    self.eye = [pt[0], pt[1], pt[2]]
    self.was_moved = True

  def rotateZ(self, angle):
    """Rotate camera z axis
    
    Arguments:
      *angle*
        in degrees
    """
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[c, s, 0, 0],
                       [-s, c, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]],
                      self.mtrx)
      self.rtn[2] = angle
      self.was_moved = True

  def rotateY(self, angle):
    """Rotate camera y axis
    
    Arguments:
      *angle*
        in degrees
    """
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[c, 0, -s, 0],
                       [0, 1, 0, 0],
                       [s, 0, c, 0],
                       [0, 0, 0, 1]],
                      self.mtrx)
      self.rtn[1] = angle
      self.was_moved = True

  def rotateX(self, angle):
    """Rotate camera x axis
    
    Arguments:
      *angle*
        in degrees
    """
    if angle:
      c = cos(radians(angle))
      s = sin(radians(angle))
      self.mtrx = dot([[1, 0, 0, 0],
                       [0, c, s, 0],
                       [0, -s, c, 0],
                       [0, 0, 0, 1]], self.mtrx)
      self.rtn[0] = angle
      self.was_moved = True

  def rotate(self, rx, ry, rz):
    """Rotate camera
    
    Arguments:
      *rx* 
        x rotation in degrees
      *ry*
        y rotation in degrees
      *rz*
        z rotation in degrees
    """
    self.rotateZ(rz)
    self.rotateX(rx)
    self.rotateY(ry)

def _LookAtMatrix(at, eye, up=[0,1,0], reflect=False):
  """Define a matrix looking at.

  Arguments:
    *at* 
      tuple (x,y,z) of point camera pointed at, floats
    *eye*
      matrix [x,y,z] position of camera, floats

  Keyword arguments:
    *up*
      array vector of up direction
    *eflect*
      boolean if matrix is reflected
  """
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
  return array([[xaxis[a], yaxis[a], zaxis[a], z[a]] for a in range(4)],
               dtype=ctypes.c_float)

def _ProjectionMatrix(near=10, far=1000.0, fov_w=1.6, fov_h=1.2):
  """Set up projection matrix
  
  Keyword arguments:
    *near*
      distance to near plane, float
    *far*
      distance to far plane, float
    *fov_w*
      horizontal field of view in radians
    *fov_h*
      vertical field of view in radians
  """
  # Matrices are considered to be M[row][col]
  # Use DirectX convention, so need to do rowvec*Matrix to transform
  w = 2.0 / fov_w
  h = 2.0 / fov_h
  q = far / (far - near)
  M = [[0] * 4 for i in range(4)]
  M[0][0] = w
  M[1][1] = h
  M[2][2] = q
  M[3][2] = -q * near
  M[2][3] = 1
  return array(M, dtype=ctypes.c_float)

