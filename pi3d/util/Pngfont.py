import ctypes

from PIL import ImageDraw

from pi3d.constants import *
from pi3d.Texture import Texture
import sys
if  sys.version_info[0] == 3:
  unichr = chr

# Text and fonts
# TODO TEXTURES NEED CLEANING UP

class Pngfont(Texture):
  def __init__(self, font, color=(255,255,255,255)):
    """

    A method of writing in pi3d using 'hand designed' fonts, where the top
    line of the texture contains metainformation about each character.

    Mainly superseded by the Font class.

    Arguments:
      *font*
        The name of a file containing a PNG texture.
      *color*
        A hex string representing a color.

    """
    if not font.endswith('.png'):
      font += '.png'
    super(Pngfont, self).__init__(font)
    #self.font = font
    pixels = self.im.load()

    self.glyph_table = {}
    # Extract font information from top scanline of font image;  create width,
    # height, tex_coord and vertices for each character.
    for v in range(95):
      x = (pixels[v * 2, 0][0] * 2.0) / self.ix
      y = ((pixels[v * 2, 0][1] + 8) * 2.0) / self.iy
      width = float(pixels[v * 2 + 1, 0][0])
      height = float(pixels[v * 2 + 1, 0][1])
      width_scale = width / self.ix
      height_scale = height / self.iy

      self.glyph_table[unichr(v + 32)] = [width, height,
        [(x + width_scale, y - height_scale),
         (x, y - height_scale),
         (x, y),
         (x + width_scale, y)],
        [(width, 0, 0), (0, 0, 0), (0, -height, 0), (width, -height, 0)]]

    self.height = height

    alph = self.im.split()[-1]  #keep alpha
    draw = ImageDraw.Draw(self.im)
    draw.rectangle((0, 1, self.ix, self.iy), fill=color)
    self.im.putalpha(alph)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()
