from pi3d.Utility import from_polar

def rotate_vec(rx, ry, rz, xyz):
  x, y, z = xyz
  if rx:
    ca, sa = from_polar(rx)
    yy = y * ca - z * sa
    z = y * sa + z * ca
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

