import ctypes

from PIL import ImageDraw

from pi3d.constants import *
from pi3d.Texture import Texture

# Text and fonts
# TODO TEXTURES NEED CLEANING UP

class Font(Texture):
  def __init__(self, font, color="#ffffff"):
    """

    A method of writing in pi3d using 'hand designed' fonts, where the top
    line of the texture contains metainformation about each character.

    Mainly superseded by the Ttffont class.

    Arguments:
      *font*
        The name of a file containing a PNG texture.
      *color*
        A hex string representing a color.

    """
    f = font
    if not f.endswith('.png'):
      f += '.png'
    super(Font, self).__init__("fonts/%s" % f)
    self.font = font
    pixels = self.im.load()

    self.ch = []
    # Extract font information from top scanline of font image;  create width,
    # height, tex_coord and vertices for each character.
    for v in range(95):
      x = (pixels[v * 2, 0][0] * 2.0) / self.ix
      y = ((pixels[v * 2, 0][1] + 8) * 2.0) / self.iy
      width = float(pixels[v * 2 + 1, 0][0])
      height = float(pixels[v * 2 + 1, 0][1])
      width_scale = width / self.ix
      height_scale = height / self.iy

      self.ch.append((width, height,
        [(x + width_scale, y - height_scale),
         (x, y - height_scale),
         (x, y),
         (x + width_scale, y)],
        [(width, 0, 0), (0, 0, 0), (0, -height, 0), (width, -height, 0)]))

    alph = self.im.split()[-1]  #keep alpha
    draw = ImageDraw.Draw(self.im)
    draw.rectangle((0, 1, self.ix, self.iy), fill=color)
    self.im.putalpha(alph)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()
