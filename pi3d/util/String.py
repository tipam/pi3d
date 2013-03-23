from pi3d import *

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
from pi3d.util import Utility

DOTS_PER_INCH = 72.0
DEFAULT_FONT_SIZE = 0.24
DEFAULT_FONT_SCALE = DEFAULT_FONT_SIZE / DOTS_PER_INCH

class String(Shape):
  """Shape used for writing text on screen. It is a flat, one sided rectangualar plane"""
  def __init__(self, camera=None, light=None, font=None, string=None,
               x=0.0, y=0.0, z=1.0,
               sx=DEFAULT_FONT_SCALE, sy=DEFAULT_FONT_SCALE,
               is_3d=True, size=DEFAULT_FONT_SIZE,
               rx=0.0, ry=0.0, rz=0.0):
    """Standard Shape constructor without the facility to change z scale or 
    any of the offset values. Additional keyword arguments:
    
      *font*
        Font or Ttffont class object.
      *string*
        of ASCI characters in range(32, 128)
      *sx, sy*
        These change the actual vertex positions of the shape rather than being
        used as scaling factors. This is to avoid distortion when the string is
        drawn using an orthographic camera
      *is_3d*
        alters the values of sx and sy to give reasonable sizes with 2D or 3D
        drawing
      *size*
        approximate size of the characters in inches - obviously for 3D drawing
        of strings this will depend on camera fov, display size and how far away
        the string is placed
    """
    if not is_3d:
      sy = sx = size * 4.0
    super(String, self).__init__(camera, light, "", x, y, z,
                                 rx, ry, rz,  1.0, 1.0, 1.0,  0.0, 0.0, 0.0)

    if VERBOSE:
      print "Creating string ..."

    self.verts = []
    self.texcoords = []
    self.norms = []
    self.inds = []
    temp_verts = []

    xoff = 0.0
    maxh = 0.0
    #TODO cope with \n characters to give multi line strings
    for i, c in enumerate(string):
      v = ord(c) - 32
      w, h, texc, verts = font.ch[v]
      if v >= 0:
        for j in verts:
          temp_verts.append((j[0]+xoff, j[1], j[2]))
        xoff += w
        if h > maxh:
          maxh = h
        for j in texc:
          self.texcoords.append(j)
        for j in [(0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0)]:
          self.norms.append(j)
        stv = 4 * i
        for j in [(stv, stv + 2, stv + 1), (stv, stv + 3, stv + 2)]:
          self.inds.append(j)

    for j in temp_verts:
      self.verts.append(((j[0] - xoff/2.0) * sx, (j[1] + maxh/2.0) * sy, j[2]))

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))
    self.buf[0].textures = [font]
    self.buf[0].unib[1] = -1.0
