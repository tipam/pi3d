from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info[0] == 3:
  unichr = chr
  text_type = str
else:
  text_type = unicode
import logging

from pi3d import *

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
from pi3d.util import Utility

LOGGER = logging.getLogger(__name__)
DOTS_PER_INCH = 72.0
DEFAULT_FONT_SIZE = 0.24
DEFAULT_FONT_SCALE = DEFAULT_FONT_SIZE / DOTS_PER_INCH
GAP = 1.0

_NORMALS = [[0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0]]

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

    LOGGER.info("Creating string ...")

    self.verts = []
    self.texcoords = []
    self.norms = []
    self.inds = []
    temp_verts = []

    xoff = 0.0
    yoff = 0.0
    lines = 0
    if not isinstance(string, text_type):
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

    default = font.glyph_table.get(unichr(0), None)
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
      w, h, texc, verts = glyph[0:4]
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
    
    self.string = string #for later use in quick_change() method
    self.maxlen = len(string)
    self.font = font
  
  def quick_change(self, new_string):
    """Method for quickly changing some characters within a previously
    generated String. i.e. for changing digits in a readout etc.
    
    NB: 1. if you use a variable width font there will be some distortion
    as characters are stretched or squashed to the original character's
    dimensions. 2. there is no account made of new line characters (TODO)
    3. you must make the original string long enough to fit any additional
    characters you add to new_string 4. you must make sure the Font as
    used for the String.__init__ contains all the glyphs you may need for
    subsequent changes.
    """
    import ctypes
    if new_string != self.string:
      new_string = new_string + ' ' * (len(self.string) - len(new_string))
      trunc_string = new_string[:self.maxlen] #chop to length
      for i, c in enumerate(trunc_string):
        if c != self.string[i]:
          stride = 8
          offset = 6
          texc = self.font.glyph_table[c][2]
          for j, tc in enumerate(texc): #patch values directly into array_buffer
            for k in [0, 1]:
              self.buf[0].array_buffer[(i * 4 + j),(offset + k)] = tc[k]
          uvmod = True
      self.buf[0]._select() #then just call glBufferData
      opengles.glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.buf[0].array_buffer.nbytes,
                        self.buf[0].array_buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
      self.string = new_string
