from __future__ import absolute_import, division, print_function, unicode_literals


import ctypes
import itertools
import os.path
import sys
if sys.version_info[0] == 3:
  unichr = chr

try:
  from PIL import Image, ImageDraw, ImageFont
except:
  print('Unable to import libraries from PIL')

from pi3d.constants import *
from pi3d.Texture import *
from pi3d.shape.Sprite import Sprite

MAX_SIZE = 1920

class FixedString(Texture):
  """
  A texture containing a simple string drawn using ImageDraw.
  
  The advantage over a standard String is that it only requires a simple
  Sprite shape for drawing so the gpu has to only draw two triangles
  rather than two triangles for each letter."""

  def __init__(self, font, string, color=(255,255,255,255),
               font_size=24, image_size=256, margin=5.0, justify='C',
               background_color=None, shader=None):
    """Arguments:
    *font*:
      File path/name to a TrueType font file.

    *string*:
      String to write.
      
    *color*:
      Color in format #RRGGBB, (255,0,0,255) etc (as accepted by PIL.ImageDraw)

    *font_size*:
      Point size for drawing the letters on the internal Texture

    *image_size*:
      Width and height of the Texture that backs the image.
      If it doesn't fit then a larger size will be tried up to MAX_SIZE.
      The isses are: maximum image size supported by the gpu (2048x2048?)
      gpu memory usage and time to load by working up the size required
      in 256 pixel steps.
      
    *margin*:
      Offsets from the top left corner for the text and space on right
      and bottom.

    *background_color*:
      filled background
      
    *shader*:
      can be passed to init otherwise needs to be set in set_shader or
      draw
    """
    super(FixedString, self).__init__(font)
    self.font = font
    try:
      imgfont = ImageFont.truetype(font, font_size)
    except IOError:
      abspath = os.path.abspath(font)
      msg = "Couldn't find font file '%s'" % font
      if font != abspath:
        msg = "%s - absolute path is '%s'" % (msg, abspath)
      raise Exception(msg)

    justify = justify.upper()
    ascent, descent = imgfont.getmetrics()
    height = ascent + descent
    lines = string.split('\n')
    nlines = len(lines)
    maxwid = 0
    for l in lines:
      line_wid = imgfont.getsize(l)[0]
      if line_wid > maxwid:
        maxwid = line_wid
    maxwid += 2.0 * margin
    texture_wid = WIDTHS[0]
    for l in WIDTHS:
      if l > maxwid:
        texture_wid = l
        break
      texture_wid = l
    texture_hgt = int(nlines * height + 2 * margin)
    
    self.im = Image.new("RGBA", (texture_wid, texture_hgt), background_color)
    self.alpha = True
    self.ix, self.iy = texture_wid, texture_hgt
    draw = ImageDraw.Draw(self.im)
    for i, line in enumerate(lines):
      line_len = imgfont.getsize(line)[0] 
      if justify == "C":
        xoff = (maxwid - line_len) / 2.0
      elif justify == "L":
        xoff = margin
      else:
        xoff = maxwid - line_len
      draw.text((xoff, margin + i * height), line, font=imgfont, fill=color)

    RGBs = 'RGBA'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()
    
    bmedge = nlines * height + 2.0 * margin
    self.sprite = Sprite(w=maxwid, h=bmedge)
    buf = self.sprite.buf[0] #convenience alias
    buf.textures = [self]
    if shader != None:
      self.sprite.shader = shader
      buf.shader = shader
    buf.unib[6] = float(maxwid / texture_wid) #scale to fit
    buf.unib[7] = float(bmedge / texture_hgt)
    
  def set_shader(self, shader):
    self.sprite.set_shader(shader)
    
  def draw(self, shader=None, txtrs=None, ntl=None, shny=None, camera=None, mlist=[]):
    self.sprite.draw(shader, txtrs, ntl, shny, camera, mlist)

  def _load_disk(self):
    """
    we need to stop the normal file loading by overriding this method
    """
