from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes

import numpy as np
from math import tan, cos, sin, radians, degrees, atan2, sqrt

from pi3d.constants import *
from pi3d.util.Utility import vec_normal, vec_cross, vec_sub, vec_dot
from pi3d.util.DefaultInstance import DefaultInstance

class Camera(DefaultInstance):
  """required object for creating and drawing Shape objects. Default instance
  created if none specified in script prior to creating a Shape
  """
  def __init__(self, at=(0, 0, 0), eye=(0, 0, -0.1), lens=None,
              is_3d=True, scale=1.0):
    """Set up view matrix to look from eye to at including perspective

    Arguments:
      *at*
        tuple (x,y,z) location to look at
      *eye*
        tuple (x,y,z) location to look from
      *lens*
        tuple (near plane dist, far plane dist, **VERTICAL** field of view in degrees,
        display aspect ratio w/h)
      *is_3d*
        determines whether the camera uses a perspective or orthographic
        projection matrix
      *scale*
        number of pixels per unit of size for orthographic camera or divisor
        for fov if perspective
    """
    super(Camera, self).__init__()

    self.at = at
    self.start_eye = eye # for reset with different lens settings
    self.eye = np.array(eye)
    if lens is None:
      from pi3d.Display import Display
      lens = [Display.INSTANCE.near, Display.INSTANCE.far, Display.INSTANCE.fov,
                  Display.INSTANCE.width / float(Display.INSTANCE.height)]
    self.lens = lens
    self.view = _LookAtMatrix(at, eye, [0, 1, 0])
    if is_3d:
      self.projection = _ProjectionMatrix(lens[0], lens[1], lens[2] / scale, lens[3])
    else:
      self.projection = _OrthographicMatrix(scale=scale)
    self.model_view = np.dot(self.view, self.projection)
    # Apply transform/rotation first, then shift into perspective space.
    self.mtrx = np.array(self.model_view, copy=True)
    # self.L_reflect = _LookAtMatrix(at,eye,[0,1,0],reflect=True)
    self.rtn = [0.0, 0.0, 0.0]

    self.was_moved = True

  @staticmethod
  def _default_instance():
    from pi3d.Display import Display

    return Camera((0, 0, 0), (0, 0, -0.1),
                  [Display.INSTANCE.near, Display.INSTANCE.far, Display.INSTANCE.fov,
                  Display.INSTANCE.width / float(Display.INSTANCE.height)])

  def reset(self, lens=None, is_3d=True, scale=1.0):
    """Has to be called each loop if the camera position or rotation changes"""
    if lens is not None:
      view = _LookAtMatrix(self.at, self.start_eye, [0, 1, 0])
      projection = _ProjectionMatrix(lens[0], lens[1], lens[2] / scale, lens[3])
      self.model_view = np.dot(view, projection)
    elif not is_3d:
      view = _LookAtMatrix(self.at, self.start_eye, [0, 1, 0])
      projection = _OrthographicMatrix(scale=scale)
      self.model_view = np.dot(view, projection)
    # TODO some way of resetting to original matrix
    self.mtrx = np.copy(self.model_view)
    self.rtn = [0.0, 0.0, 0.0]
    self.was_moved = True

  def point_at(self, target=[0.0, 0.0, 10000.0]):
    """ point the camera at a point also return the tilt and rotation values

    Keyword argument:
      *target*
        Location as [x,y,z] array to point at, defaults to a high +ve z value as
        a kind of compass!
    """
    if target[0] == self.eye[0] and target[1] == self.eye[1] and target[2] == self.eye[2]:
      return
    dx, dy, dz = target[0] - self.eye[0], target[1] - self.eye[1], target[2] - self.eye[2]
    rot = -degrees(atan2(dx, dz))
    horiz = sqrt(np.dot([dx,dz], [dx, dz]))
    tilt = degrees(atan2(dy, horiz))
    self.rotate(tilt, rot, 0)
    return tilt, rot

  def position(self, pt):
    """position camera

    Arguments:
      *pt*
        tuple (x, y, z) floats
    """
    self.eye = np.array(pt)
    m = np.identity(4, dtype="float32")
    m[3,:3] = -self.eye
    self.mtrx = np.dot(m, self.mtrx)
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
      self.mtrx = np.dot([[c, s, 0, 0],
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
      self.mtrx = np.dot([[c, 0, -s, 0],
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
      self.mtrx = np.dot([[1, 0, 0, 0],
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

def _LookAtMatrix(at, eye, up=[0, 1, 0], reflect=False):
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
    eye[1] *= -1
    at[1] *= -1
  zaxis = vec_normal(vec_sub(at, eye))
  xaxis = vec_normal(vec_cross(up, zaxis))
  yaxis = vec_cross(zaxis, xaxis)
  xaxis.append(-vec_dot(xaxis, eye))
  yaxis.append(-vec_dot(yaxis, eye))
  zaxis.append(-vec_dot(zaxis, eye))
  z = [0, 0, 0, 1.0]
  return np.array([[xaxis[a], yaxis[a], zaxis[a], z[a]] for a in range(4)],
               dtype="float32")

def _ProjectionMatrix(near, far, fov, aspectRatio):
  """Set up perspective projection matrix

  Keyword arguments:
    *near*
      distance to near plane, float
    *far*
      distance to far plane, float
    *fov*
      **VERTICAL** field of view in degrees, float
    *aspectRatio*
      aspect ratio = width / height of the scene, float
  """
  # Matrices are considered to be M[row][col]
  # Use DirectX convention, so need to do rowvec*Matrix to transform
  size = 1 / tan(radians(fov)/2.0)
  M = np.zeros((4, 4), dtype="float32")
  M[0,0] = size/aspectRatio
  M[1,1] = size  #negative value reflects scene on the Y axis
  M[2,2] = (far + near) / (far - near)
  M[2,3] = 1
  M[3,2] = -(2 * far * near)/(far - near)
  return M

def _OrthographicMatrix(scale=1.0):
  """Set up orthographic projection matrix

  Keyword argument:
    *scale*
      number of pixels per unit of size

  """
  from pi3d.Display import Display
  M = np.zeros((4, 4), dtype="float32")
  M[0,0] = 2.0 * scale / Display.INSTANCE.width
  M[1,1] = 2.0 * scale / Display.INSTANCE.height
  #M[2,2] = 2.0 / Display.INSTANCE.width
  M[2,2] = 2.0 / 10000.0
  M[3,2] = -1
  M[3,3] = 1
  return M

