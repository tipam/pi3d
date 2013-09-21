from __future__ import absolute_import, division, print_function, unicode_literals

import six

from pi3d import *

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
from pi3d.util import Utility

DOTS_PER_INCH = 72.0
DEFAULT_FONT_SIZE = 0.24
DEFAULT_FONT_SCALE = DEFAULT_FONT_SIZE / DOTS_PER_INCH
GAP = 1.0

_NORMALS = [[0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]

class String(Shape):
  """Shape used for writing text on screen. It is a flat, one sided rectangualar plane"""
  def __init__(self, camera=None, light=None, font=None, string=None,
               x=0.0, y=0.0, z=1.0,
               sx=DEFAULT_FONT_SCALE, sy=DEFAULT_FONT_SCALE,
               is_3d=True, size=DEFAULT_FONT_SIZE,
               rx=0.0, ry=0.0, rz=0.0, justify="C"):
    """Standard Shape constructor without the facility to change z scale or
    any of the offset values. Additional keyword arguments:

      *font*
        Pngfont or Font class object.
      *string*
        of ASCI characters in range(32, 128) plus 10 = \n Line Feed
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
      *justify*
        default C for central, can be R for right or L for left
    """
    if not is_3d:
      sy = sx = size * 4.0
    super(String, self).__init__(camera, light, "", x, y, z,
                                 rx, ry, rz,  1.0, 1.0, 1.0,  0.0, 0.0, 0.0)

    if VERBOSE:
      print("Creating string ...")

    self.verts = []
    self.texcoords = []
    self.norms = []
    self.inds = []
    temp_verts = []

    xoff = 0.0
    yoff = 0.0
    lines = 0
    if not isinstance(string, six.text_type):
      string = string.decode('utf-8')
    nlines = string.count("\n") + 1

    def make_verts(): #local function to justify each line
      if justify.upper() == "C":
        cx = xoff / 2.0
      elif justify.upper() == "L":
        cx = 0.0
      else:
        cx = xoff
      for j in temp_verts:
        self.verts.append([(j[0] - cx) * sx,
                           (j[1] + nlines * font.height * GAP / 2.0 - yoff) * sy,
                           j[2]])

    default = font.glyph_table.get(six.unichr(0), None)
    for i, c in enumerate(string):
      if c == '\n':
        make_verts()
        yoff += font.height * GAP
        xoff = 0.0
        temp_verts = []
        lines += 1
        continue #don't attempt to draw this character!

      glyph = font.glyph_table.get(c, default)
      if not glyph:
        continue
      w, h, texc, verts = glyph
      for j in verts:
        temp_verts.append((j[0]+xoff, j[1], j[2]))
      xoff += w
      for j in texc:
        self.texcoords.append(j)
      self.norms.extend(_NORMALS)

      # Take Into account unprinted \n characters
      stv = 4 * (i - lines)
      self.inds.extend([[stv, stv + 2, stv + 1], [stv, stv + 3, stv + 2]])

    make_verts()

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))
    self.buf[0].textures = [font]
    self.buf[0].unib[1] = -1.0
