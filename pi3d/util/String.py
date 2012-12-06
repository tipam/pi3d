from pi3d import *

from pi3d.Buffer import Buffer
from pi3d.shape.Shape import Shape
from pi3d.util import Utility

DOTS_PER_INCH = 72.0
DEFAULT_FONT_DOT_SIZE = 24
DEFAULT_FONT_SCALE = DEFAULT_FONT_DOT_SIZE / DOTS_PER_INCH


class String(Shape):
  def __init__(self, camera, light, font, string, x=0.0, y=0.0, z=1.0, 
      sx=DEFAULT_FONT_SCALE, sy=DEFAULT_FONT_SCALE, is_3d = True, size=DEFAULT_FONT_DOT_SIZE, 
      rx=0.0, ry=0.0, rz=0.0):
    if not is_3d:
      sx = size / DOTS_PER_INCH
      sy = sx
    super(String, self).__init__(camera, light, "", x, y, z, rx, ry, rz,
                                sx, sy, 1.0, 0.0, 0.0, 0.0)

    if VERBOSE:
      print "Creating string ..."
    
    self.verts = []
    self.texcoords = []
    self.norms = []
    self.inds = []
    
    xoff = 0.0
    for i, c in enumerate(string):
      v = ord(c) - 32
      w, h, texc, verts = font.chr[v]
      off_verts = []
      for j in range(4): off_verts.append((verts[j][0] + xoff, verts[j][1], verts[j][2]))
      verts = off_verts
      xoff += w
      print xoff, w
      if v > 0:
        for j in verts: self.verts.append(j) 
        for j in texc: self.texcoords.append(j) 
        for j in [(0.0,0.0,1.0), (0.0,0.0,1.0), (0.0,0.0,1.0), (0.0,0.0,1.0)]: self.norms.append(j)
        for j in [(i, i + 2, i + 1), (i, i + 3, i + 2)]: self.inds.append(j) 

      
    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))
    self.buf[0].textures = [font]
