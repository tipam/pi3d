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

from pi3d.Texture import Texture, WIDTHS
from pi3d.shape.Sprite import Sprite

class FixedString(Texture):
  """
  A texture containing a simple string drawn using ImageDraw.
  
  The advantage over a standard String is that it only requires a simple
  Sprite shape for drawing so the gpu has to only draw two triangles
  rather than two triangles for each letter."""

  def __init__(self, font, string, camera=None, color=(255,255,255,255),
               shadow=(0,0,0,255), shadow_radius=0,
               font_size=24, margin=5.0, justify='C',
               background_color=None, shader=None, f_type='', mipmap=True, width=None):
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

    *shadow*:
      Color of shadow, default black.

    *shadow_radius*:
      Gaussian blur radius applied to shadow layer, default 0 (no shadow)

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
    new_lines = []
    maxwid = 0
    for l in lines:
      line_wid = imgfont.getsize(l)[0]
      if width is not None and line_wid > width:
        new_line = ""
        space = ""
        words = l.split(" ")
        for word in words:
          check_line = "{}{}{}".format(new_line, space, word)
          if imgfont.getsize(check_line)[0] <= width:
            new_line = check_line
          else: # wrap before this word TODO cope with lines with no spaces
            if "-" in word: # TODO make this a function to split first on " " then "-" then on
              split_word = word.split("-")
              pre = split_word[0]
              post = "-".join(split_word[1:])
              check_line = "{} {}-".format(new_line, pre)
              if imgfont.getsize(check_line)[0] <= width:
                new_line = check_line
                word = post
            new_lines.append(new_line)
            new_line = word
          space = " "
        new_lines.append(new_line)
      else:
        new_lines.append(l)
    lines = new_lines
    for l in lines:
      line_wid = imgfont.getsize(l)[0]
      if line_wid > maxwid:
        maxwid = line_wid
    maxwid += 2.0 * margin
    texture_wid = min(int(maxwid / 4) * 4, 2048)
    nlines = len(lines)
    texture_hgt = int(nlines * height + 2 * margin)

    self.im = Image.new("RGBA", (texture_wid, texture_hgt), background_color)
    self.ix, self.iy = texture_wid, texture_hgt
    draw = ImageDraw.Draw(self.im)
    if shadow_radius > 0:
      from PIL import ImageFilter
      self._render_text(lines, justify, margin, imgfont, maxwid, height, shadow, draw)
      self.im = self.im.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
      if background_color == None:
        im_arr = self._force_color(np.array(self.im), shadow)
        try: # numpy not quite working fully in pypy so have to convert tobytes
          self.im = Image.fromarray(im_arr)
        except:
          h, w, c = im_arr.shape
          rgb = 'RGB' if c == 3 else 'RGBA'
          self.im = Image.frombytes(rgb, (w, h), im_arr.tobytes())
        
      draw = ImageDraw.Draw(self.im)

    self._render_text(lines, justify, margin, imgfont, maxwid, height, color, draw)

    force_color = background_color is None and shadow_radius == 0
    if f_type == '':
      self.image = np.array(self.im)
    elif 'BUMP' in f_type:
      amount = -1.0 if '+' in f_type else 1.0
      self.image = self._normal_map(np.array(self.im, dtype=np.uint8), amount)
      force_color = False

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

    if force_color:
      self.image = self._force_color(self.image, color)

    self._tex = ctypes.c_uint()

    bmedge = nlines * height + 2.0 * margin
    self.sprite = Sprite(camera=camera, w=maxwid, h=bmedge)
    buf = self.sprite.buf[0] #convenience alias
    buf.textures = [self]
    if shader != None:
      self.sprite.shader = shader
      buf.shader = shader
    buf.unib[6] = float(maxwid / texture_wid) #scale to fit
    buf.unib[7] = float(bmedge / texture_hgt)

  def _render_text(self, lines, justify, margin, imgfont, maxwid, height, color, draw):
    for i, line in enumerate(lines):
      line_len = imgfont.getsize(line)[0]
      if justify == "C":
        xoff = (maxwid - line_len) / 2.0
      elif justify == "L":
        xoff = margin
      else:
        xoff = maxwid - line_len

      draw.text((xoff, margin + i * height), line, font=imgfont, fill=color)


  def set_shader(self, shader):
    ''' wrapper for Shape.set_shader'''
    self.sprite.set_shader(shader)

  def draw(self, shader=None, txtrs=None, ntl=None, shny=None, camera=None):
    '''wrapper for Shape.draw()'''
    self.sprite.draw(shader, txtrs, ntl, shny, camera)

  def _force_color(self, im_array, color):
    """
    Overwrite color of all pixels as PIL renders text incorrectly when drawing on transparent backgrounds
    http://nedbatchelder.com/blog/200801/truly_transparent_text_with_pil.html
    """
    if isinstance(color, str):
      from PIL import ImageColor
      color = ImageColor.getrgb(color)
    im_array[:,:,:3] = color[:3]
    return im_array

  def _load_disk(self):
    """
    we need to stop the normal file loading by overriding this method
    """
