from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes

import numpy as np
import math

from pi3d.util.Utility import vec_normal, vec_cross, vec_sub, vec_dot
from pi3d.util.DefaultInstance import DefaultInstance

class Camera(DefaultInstance):
  """required object for creating and drawing Shape objects. Default instance
  created if none specified in script prior to creating a Shape
  """
  def __init__(self, at=(0, 0, 0), eye=(0, 0, -0.1), lens=None,
              is_3d=True, scale=1.0, absolute=True):
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
      *absolute*
        when True (default) then all rotations are relative to the absolute
        frame of reference. When False then rotations are relative to the
        rotated position
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
    self.scale = scale
    self.was_moved = True
    self.rotated = False
    self.mtrx_made = True
    self.absolute = absolute
    self.r_mtrx = np.identity(4, dtype='float32') # rotation matrix for rotations relative to rotated frame of reference
    self.rx = np.identity(4, dtype='float32') # hold rotation matrices for each axis
    self.ry = np.identity(4, dtype='float32')
    self.rz = np.identity(4, dtype='float32')
    self.t1 = np.identity(4, dtype='float32') # translation applied prior to rotation i.e. for stereo effect
    self.t2 = np.identity(4, dtype='float32') # translation applied after rotation i.e. actual position


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
    self.scale = scale
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
    rot = -math.degrees(math.atan2(dx, dz))
    horiz = (dx * dx + dz * dz) ** 0.5
    tilt = math.degrees(math.atan2(dy, horiz))
    self.rotate(tilt, rot, 0)
    return tilt, rot

  def get_direction(self):
    """ returns the direction that the Camera is pointing as a numpy unit
    vector [x,y,z] this can be used directly for positioning the view
    position without resorting to trig functions. Also see relocate()
    """
    if not self.rotated:
      self._make_r_mtrx()
    return self.r_mtrx[0:3,2]

  def relocate(self, rot=None, tilt=None, point=np.array([0.0, 0.0, 0.0]),
                distance=np.array([0.0, 0.0, 0.0]), normal=None,
                slope_factor=0.5, crab=False):
    """ A convenience function for frequently used Camera animation steps.
    The camera is reset and the rotation and tilt are applied. If a normal
    is not supplied the camera is positioned using the distance and point
    vectors. If there is a normal then the camera is moved to the point
    and the new position relative to this is returned. This behaviour
    allows the y coordinate to be subsequently adjusted (in the calling
    program) using ElevationMap.calcHeight()

    The normal vector is also used in conjunction with the slope_factor
    to determine an adjustment to the distance moved each frame.

      *rot*
        absolute y rotation of the Camera

      *tilt*
        x rotation

      *point*
        3D vector to move relative to (or to if normal is None)

      *distance*
        3D vector from point to Camera

      *normal*
        3D vector normal to surface at point

      *slope_factor*
        effect of normal vector on movement

      *crab*
        if True then distance is horizontally at right angles to direction
        that the Camera is pointing
    """
    self.reset()
    if tilt is not None:
      self.rotateX(tilt)
    if rot is not None:
      self.rotateY(rot)

    if not self.rotated:
      self._make_r_mtrx()
    direction = self.r_mtrx[0:3,2] # NB this is different from the direction vector in self.mtrx
    if crab:
      direction = np.cross(direction, [0.0, 1.0, 0.0]) # horizontal sideways
    if normal is None: # move the camera to new location now
      new_point = direction * distance + point
      self.position(new_point)
      return new_point
    else: # move the camera to old position but return new position (for height adjustment)
      self.position(point)
      # resultant in x,z plane
      netf = np.dot(direction[[0,2]], (normal[[0,2]] * slope_factor))
      if netf > -1.0:
        return direction * distance * (1.0 + netf) + point
    return point # otherwise don't move!

  def position(self, pt):
    """position camera

    Arguments:
      *pt*
        tuple (x, y, z) floats
    """
    self.eye = np.array(pt)
    self.t2[3,:3] = self.eye * -1.0
    #self.mtrx = np.dot(m, self.mtrx)
    self.was_moved = True
    self.mtrx_made = False

  def _rotate_axis(self, angle, k0, k1, k2, k3):
    ''' similar job needed for each axis but with different signs
    '''
    c = math.cos(math.radians(angle))
    s = math.sin(math.radians(angle))
    self.was_moved = True
    self.mtrx_made = False
    self.rotated = False
    return [[k0 * c, k1 * s], 
            [k2 * s, k3 * c]]

  def rotateZ(self, angle):
    """Rotate camera z axis

    Arguments:
      *angle*
        in degrees
    """
    self.rz[0:2,0:2] = self._rotate_axis(angle, 1, 1, -1, 1)
    self.rtn[2] = angle

  def rotateY(self, angle):
    """Rotate camera y axis

    Arguments:
      *angle*
        in degrees
    """
    self.ry[0:3:2,0:3:2] = self._rotate_axis(angle, 1, -1, 1, 1)
    self.rtn[1] = angle

  def rotateX(self, angle):
    """Rotate camera x axis

    Arguments:
      *angle*
        in degrees
    """
    self.rx[1:3,1:3] = self._rotate_axis(angle, 1, 1, -1, 1)
    self.rtn[0] = angle

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

  def offset(self, pt):
    """position camera

    Arguments:
      *pt*
        tuple (x, y, z) floats
    """
    self.t1[3,:3] = np.array(pt) * -1.0
    self.was_moved = True
    self.mtrx_made = False

  def make_mtrx(self):
    if not self.rotated:
      self._make_r_mtrx()
    self.mtrx = np.dot(self.t2,
                    np.dot(self.r_mtrx,
                        np.dot(self.t1, self.mtrx)))
    self.mtrx_made = True

  def _make_r_mtrx(self):
    if self.absolute:
      self.r_mtrx = np.identity(4, dtype='float32')
    self.r_mtrx = np.dot(self.r_mtrx, 
                      np.dot(self.ry,
                          np.dot(self.rx, self.rz)))
    self.rotated = True
    
  def euler_angles(self, matrix=None):
    ''' Or more correctly Tait-Bryan angles. Argument
    
      *matrix*
        can supply a rotation matrix to use (as generated by the following
        method.) Defaults to using the Camera.r_mtrx
        
    in pi3d arrangement (C type and Z into screen)::
    
        cz.cx-sz.sx.sy  cy.sz+cz.sx.sy  -cx.sy
        -cx.sz          cz.cx            sx
        cz.sy+cy.sz.sx  sz.sy-cz.cy.sx   cx.cy``
    '''
    m = matrix if matrix is not None else self.r_mtrx # alias for clarity
    rx = math.asin(m[1,2])
    cx = math.cos(rx)
    if cx != 0.0:
      ry = math.atan2(-m[0,2], m[2,2])
    else:
      ry = math.pi / 2.0
    rz = math.atan2(-m[1,0], m[1,1])
    return math.degrees(rx), math.degrees(ry), math.degrees(rz)
  
  def matrix_from_two_vectors(self, start_vector, vector):
    ''' uses two 3D vectors (arrays) to generate a rotation vector representing
    the movement from one direction to another. NB because there are many
    ways of doing this the z rotation may not match so this this method might
    be best combined with the euler_angles system above. See the 
    pi3d_demos/ForestStereo.py example - key press 'k'
    '''
    start_vector /= np.linalg.norm(start_vector) # convert to unit length
    vector /= np.linalg.norm(vector)
    axis = np.cross(vector, start_vector)
    l_axis = np.linalg.norm(axis)
    if l_axis == 0: # might be zero if coincident vectors
      axis = np.array([0.0, 1.0, 0.0])
    else:
      axis /= l_axis
    # sine of angle, for some reason has to be assigned to cos value i.e.
    # the angle is complementary to the expected one. Not really sure why this is!
    c = np.dot(start_vector, vector)
    angle = math.asin(c) # angle in radians
    x, y, z = axis[0:3] # aliases for clarity in matrix below
    s = math.cos(angle) # see comment above about using a = 90-a
    t = 1.0 - c
    return np.array([
                     [t*x*x + c,   t*y*x + z*s, t*x*z - y*s, 0.0], # 1
                     [t*x*y - z*s, t*y*y + c,   t*y*z + x*s, 0.0], # 2
                     [t*x*z + y*s, t*y*z - x*s, t*z*z + c,   0.0], # 3
                     [0.0,         0.0,         0.0,         1.0]], dtype='float')
  
  matrix_from_two_vecors = matrix_from_two_vectors # original had typo!

#################################
####### utility functions #######

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
    #depth = -20.0 # Shallower to avoid edge effects
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
  size = 1 / math.tan(math.radians(fov)/2.0)
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

