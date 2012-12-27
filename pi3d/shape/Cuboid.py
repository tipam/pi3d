from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.shape.Shape import Shape

class Cuboid(Shape):
  def __init__(self,  camera, light, w, h, d, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0):
    super(Cuboid,self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)

    if VERBOSE:
      print "Creating cuboid ..."

    self.width = w
    self.height = h
    self.depth = d
    self.ssize = 36
    self.ttype = GL_TRIANGLES

    ww = w / 2.0
    hh = h / 2.0
    dd = d / 2.0

    #cuboid data - faces are separated out for texturing..

    self.vertices = ((-ww, hh, dd), (ww, hh, dd), (ww,-hh, dd), (-ww, -hh, dd),
        (ww, hh, dd),  (ww, hh, -dd),  (ww, -hh, -dd), (ww, -hh, dd),
        (-ww, hh, dd), (-ww, hh, -dd), (ww, hh, -dd),  (ww, hh, dd),
        (ww, -hh, dd), (ww, -hh, -dd), (-ww, -hh, -dd),(-ww, -hh, dd),
        (-ww, -hh, dd),(-ww, -hh, -dd),(-ww, hh, -dd), (-ww, hh, dd),
        (-ww, hh, -dd),(ww, hh, -dd),  (ww, -hh, -dd), (-ww,-hh,-dd))
    self.normals = ((0.0, 0.0, 1),    (0.0, 0.0, 1),   (0.0, 0.0, 1),  (0.0, 0.0, 1),
        (1, 0.0, 0),  (1, 0.0, 0),    (1, 0.0, 0),     (1, 0.0, 0),
        (0.0, 1, 0),  (0.0, 1, 0),    (0.0, 1, 0),     (0.0, 1, 0),
        (0.0, -1, 0), (0,- 1, 0),     (0.0, -1, 0),    (0.0, -1, 0),
        (-1, 0.0, 0),  (-1, 0.0, 0),  (-1, 0.0, 0),    (-1, 0.0, 0),
        (0.0, 0.0, -1),(0.0, 0.0, -1),(0.0, 0.0, -1),  (0.0, 0.0, -1))
    
    self.indices = ((1, 0, 3), (1, 3, 2), (5, 4, 7),  (5, 7, 6),
        (9, 8, 11),  (9, 11, 10), (13, 12, 15), (13, 15, 14),
        (19, 18, 17),(19, 17, 16),(20, 21, 22), (20, 22, 23))

    tw = 1.0 #w       #texture scales (each set to 1 would stretch it over face)
    th = 1.0 #h
    td = 1.0 #d
    
    self.tex_coords = ((0.0, 0.0),        (tw, 0.0),        (tw, th),        (0.0, th),
        (0.0, 0.0),        (td, 0.0),        (td, th),        (0.0, th),
        (tw, 0.0),        (0.0, 0.0),        (0.0, td),        (tw, td),
        (0.0, 0.0),        (tw, 0.0),        (tw, td),        (0.0, td),
        (td, th),        (0.0, th),        (0.0, 0.0),        (td, 0.0),
        (tw, 0.0),        (0.0, 0.0),        (0.0, th),        (tw, th))
    
    self.buf = []
    self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))

