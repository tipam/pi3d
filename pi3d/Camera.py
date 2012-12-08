from numpy import array, dot, copy, tan, cos, sin, radians
from pi3d import *
from pi3d.shape.Shape import Shape
from pi3d.util.Utility import mat_mult, vec_normal, vec_cross, vec_sub, vec_dot, rotate, rotateX, rotateZ, rotateX, rotateY

class Camera(object):
  def __init__(self, at, eye, lens):
    """Set up view matrix to look from eye to at including perspective"""
    self.eye = eye
    self.view = LookAtMatrix(at,eye,[0,1,0])
    self.projection = ProjectionMatrix(lens[0], lens[1], lens[2], lens[3])
    #self.modelView = mat_mult(self.view, self.projection) # Apply transform/rotation first, then shift into perspective space
    #self.mtrx = [row[:] for row in self.modelView]
    self.modelView = dot(self.view, self.projection) # Apply transform/rotation first, then shift into perspective space
    self.mtrx = copy(self.modelView)
    #self.L_reflect = LookAtMatrix(at,eye,[0,1,0],reflect=True)
    #self.M_reflect = mat_mult(self.L_reflect,self.P)
 
  def reset(self):
    self.mtrx = [row[:] for row in self.modelView]    
        
  def copy(self,copyMatrix):
    self.mtrx = [row[:] for row in copyMatrix]  #usually copies the modelView matrix to begin with

  def copynew(self):
    return [row[:] for row in self.mtrx]

  def identity(self):
    self.mtrx = array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    
  def translate(self,pt):
    #self.mtrx = translate(self.mtrx,pt)
    self.mtrx = dot([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-pt[0], -pt[1], -pt[2], 1]], self.mtrx)
    eye = (pt[0], pt[1], pt[2])
  
  def rotateZ(self,angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    self.mtrx = dot([[c,s,0,0],[-s,c,0,0],[0,0,1,0],[0,0,0,1]], self.mtrx)


  def rotateY(self,angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    self.mtrx = dot([[c,0,-s,0],[0,1,0,0],[s,0,c,0],[0,0,0,1]], self.mtrx)

  def rotateX(self,angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    self.mtrx = dot([[1,0,0,0],[0,c,s,0],[0,-s,c,0],[0,0,0,1]], self.mtrx)

  def rotate(self,rx,ry,rz):
    # rot z->x->y
    if not(rz == 0.0): self.rotateZ(rz)
    if not(rx == 0.0): self.rotateX(rx)
    if not(ry == 0.0): self.rotateY(ry)
  """  
  # not applicable to Camera
  def scale(self,sx,sy,sz):
    self.mtrx=scale(self.mtrx,sx,sy,sz)
    
  def transform(self,x,y,z,rx,ry,rz,sx,sy,sz,cx,cy,cz):
    self.mtrx = translate(self.mtrx,(x-cx,y-cy,z-cz))
    rotate(self,rx,ry,rz)
    if sx<>1.0 or sy<>1.0 or sz<>1.0: self.mtrx = scale(self.mtrx,sx,sy,sz)
    self.mtrx = translate(self.mtrx,(cx,cy,cz))
  """
def LookAtMatrix(at, eye, up=[0,1,0], reflect=False):
  """Define a matrix of an eye looking at"""
  # If reflect, then reflect in plane -20.0 (water depth)
  if reflect:
    depth = -20.0 # Shallower to avoid edge effects
    eye[2] = 2*depth-eye[2]
    at[2] = 2*depth-at[2] 
  zaxis = vec_normal(vec_sub(at,eye))
  xaxis = vec_normal(vec_cross(up,zaxis))
  yaxis = vec_cross(zaxis,xaxis)
  xaxis.append(-vec_dot(xaxis,eye))
  yaxis.append(-vec_dot(yaxis,eye))
  zaxis.append(-vec_dot(zaxis,eye))
  z = [0,0,0,1.0]
  #TODO all using numpy functions
  return array([[xaxis[a],yaxis[a],zaxis[a],z[a]] for a in range(4)])

def ProjectionMatrix(near=10, far=1000.0, fov_h=1.6, fov_v=1.2):
  """Setup projection matrix with given distance to near and far planes
  and fields of view in radians"""
  # Matrices are considered to be M[row][col]
  # Use DirectX convention, so need to do rowvec*Matrix to transform
  w = 1.0/tan(fov_h*0.5)
  h = 1.0/tan(fov_v*0.5)
  Q = far/(far-near)
  M = [[0]*4 for i in range(4)]
  M[0][0] = w
  M[1][1] = h
  M[2][2] = Q
  M[3][2] = -Q*near
  M[2][3] = 1
  #TODO all using numpy functions
  return array(M)

