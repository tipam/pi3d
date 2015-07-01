from pi3d.util.Utility import from_polar
import numpy as np

"""Calculate position or direction 3D vector after rotation about axis"""
def rotate_vec(rx, ry, rz, xyz):
  if isinstance(xyz, np.ndarray) and len(xyz.shape) > 1:
    return _rotate_vec_numpy(rx, ry, rz, xyz)
  else:
    return _rotate_vec_normal(rx, ry, rz, xyz)

def _rotate_vec_normal(rx, ry, rz, xyz):
  x, y, z = xyz
  if ry:
    ca, sa = from_polar(ry)
    zz = z * ca - x * sa
    x = z * sa + x * ca
    z = zz
  if rx:
    ca, sa = from_polar(rx)
    yy = y * ca - z * sa
    z = y * sa + z * ca
    y = yy
  if rz:
    ca, sa = from_polar(rz)
    xx = x * ca - y * sa
    y = x * sa + y * ca
    x = xx
  return x, y, z

def _rotate_vec_numpy(rx, ry, rz, xyz):
  if ry:
    ca, sa = from_polar(ry)
    zz = xyz[:,2] * ca - xyz[:,0] * sa
    xyz[:,0] = xyz[:,2] * sa + xyz[:,0] * ca
    xyz[:,2] = zz
  if rx:
    ca, sa = from_polar(rx)
    yy = xyz[:,1] * ca - xyz[:,2] * sa
    xyz[:,2] = xyz[:,1] * sa + xyz[:,2] * ca
    xyz[:,1] = yy
  if rz:
    ca, sa = from_polar(rz)
    xx = xyz[:,0] * ca - xyz[:,1] * sa
    xyz[:,1] = xyz[:,0] * sa + xyz[:,1] * ca
    xyz[:,0] = xx
  return xyz
