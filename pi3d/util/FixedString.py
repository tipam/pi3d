from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes
import numpy as np
import itertools
import os.path
import sys
if sys.version_info[0] == 3:
  unichr = chr

# NB PIL must be available to use FixedString. Otherwise use Pngfont
from PIL import Image, ImageDraw, ImageFont

from pi3d.constants import *
from pi3d.Texture import *
from pi3d.shape.Sprite import Sprite

class FixedString(Texture):
  """
  A texture containing a simple string drawn using ImageDraw.
  
  The advantage over a standard String is that it only requires a simple
  Sprite shape for drawing so the gpu has to only draw two triangles
  rather than two triangles for each letter."""

  def __init__(self, font, string, camera=None, color=(255,255,255,255),
               font_size=24, margin=5.0, justify='C',
               background_color=None, shader=None, f_type='', mipmap=True):
    """Arguments:
    
    *font*:
      File path/name to a TrueType font file.

    *string*:
      String to write.
      
    *camera*:
      Camera object passed on to constructor of sprite
      
    *color*:
      Color in format '#RRGGBB', (255,0,0,255), 'orange' etc (as accepted 
      by PIL.ImageDraw) default (255, 255, 255, 255) i.e. white 100% alpha

    *font_size*:
      Point size for drawing the letters on the internal Texture. default 24

    *margin*:
      Offsets from the top left corner for the text and space on right
      and bottom. default 5.0
      
    *justify*:
      L(eft), C(entre), R(ight) default C

    *background_color*:
      filled background in ImageDraw format as above. default None i.e.
      transparent. 
      
    *shader*:
      can be passed to init otherwise needs to be set in set_shader or
      draw. default None
      
    *f_type*:
      filter type. BUMP will generate a normal map (indented by default,
      +BUMP or BUMP+ will make it stick out), EMBOSS, CONTOUR, BLUR and 
      SMOOTH do what they sound like they will do.
    """
    super(FixedString, self).__init__(font, mipmap=mipmap)
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
    f_type = f_type.upper()
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

    if f_type == '':
      pass
    elif 'BUMP' in f_type:
      amount = -1.0 if '+' in f_type else 1.0
      self.image = self._normal_map(np.array(self.im, dtype=np.uint8), amount)
    else:
      from PIL import ImageFilter
      if f_type == 'EMBOSS':
        self.im = self.im.filter(ImageFilter.EMBOSS)
      elif f_type == 'CONTOUR':
        self.im = self.im.filter(ImageFilter.CONTOUR)
      elif f_type == 'BLUR':
        self.im = self.im.filter(ImageFilter.BLUR)
      elif f_type == 'SMOOTH':
        self.im = self.im.filter(ImageFilter.SMOOTH_MORE)
      self.image = np.array(self.im)
      if background_color is None:
        if isinstance(color, str):
          from PIL import ImageColor
          color = ImageColor.getrgb(color)
        self.image[:,:,:3] = color[:3]
    self._tex = ctypes.c_int()
    
    bmedge = nlines * height + 2.0 * margin
    self.sprite = Sprite(camera=camera, w=maxwid, h=bmedge)
    buf = self.sprite.buf[0] #convenience alias
    buf.textures = [self]
    if shader != None:
      self.sprite.shader = shader
      buf.shader = shader
    buf.unib[6] = float(maxwid / texture_wid) #scale to fit
    buf.unib[7] = float(bmedge / texture_hgt)
    
  def set_shader(self, shader):
    ''' wrapper for Shape.set_shader'''
    self.sprite.set_shader(shader)
    
  def draw(self, shader=None, txtrs=None, ntl=None, shny=None, camera=None, mlist=[]):
    '''wrapper for Shape.draw()'''
    self.sprite.draw(shader, txtrs, ntl, shny, camera, mlist)
    
  def _load_disk(self):
    """
    we need to stop the normal file loading by overriding this method
    """
