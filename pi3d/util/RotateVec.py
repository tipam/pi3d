from pi3d.util.Utility import from_polar

"""Calculate position or direction 3D vector after rotation about axis"""
def rotate_vec(rx, ry, rz, xyz):
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
"""
# no longer used anywhere

def rotate_vec_x(r, xyz):
  ca, sa = from_polar(r)
  return xyz[0], xyz[1] * ca - xyz[2] * sa, xyz[1] * sa + xyz[2] * ca

def rotate_vec_y(r, xyz):
  ca, sa = from_polar(r)
  return xyz[2] * sa + xyz[0] * ca, xyz[1], xyz[2] * ca - xyz[0] * sa

def rotate_vec_z(r, xyz):
  ca, sa = from_polar(r)
  return xyz[0] * ca - xyz[1] * sa, xyz[0] * sa + xyz[1] * ca, xyz[2]
"""
