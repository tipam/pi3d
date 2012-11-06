class Shape(object):
  def __init__(self, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz):
    self.name = name
    self.x = x                #position
    self.y = y
    self.z = z
    self.rotx = rx                #rotation
    self.roty = ry
    self.rotz = rz
    self.sx = sx                #scale
    self.sy = sy
    self.sz = sz
    self.cx = cx                #center
    self.cy = cy
    self.cz = cz

        #this should all be done with matrices!! ... just for testing ...

  def scale(self, sx, sy, sz):
    self.sx = sx
    self.sy = sy
    self.sz = sz

  def position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def translate(self, dx, dy, dz):
    self.x = self.x + dx
    self.y = self.y + dy
    self.z = self.z + dz

  def rotateToX(self, v):
    self.rotx = v

  def rotateToY(self, v):
    self.roty = v

  def rotateToZ(self, v):
    self.rotz = v

  def rotateIncX(self,v):
    self.rotx += v

  def rotateIncY(self,v):
    self.roty += v

  def rotateIncZ(self,v):
    self.rotz += v

