import ctypes
import Image

from PIL import ImageDraw

from pi3d import *
from pi3d.Texture import Texture

# Text and fonts
# TODO TEXTURES NEED CLEANING UP

class Font(Texture):
  def __init__(self, font, col="#ffffff"):
    super(Font, self).__init__("fonts/%s.png" % font)
    self.font = font
    pixels = self.im.load()

    self.ch = []
    #extract font information from top scanline of font image;
    #Create width,height,tex_coord and vertices for each char ...
    for v in range(95):
      x =(pixels[v * 2, 0][0] * 2.0) / self.ix  #x coord in image for this char
      y = ((pixels[v * 2, 0][1] + 8) * 2.0) / self.iy  #y coord in image for this char
      w = pixels[v * 2 + 1, 0][0] * 1.0   #width of this char
      h = pixels[v * 2 + 1, 0][1] * 1.0   #height of this char
      tw = w / self.ix
      th = h / self.iy

      self.ch.append((w, h, 
        [(x + tw, y - th), (x, y - th),  (x, y), (x + tw, y)], 
        [(w, 0, 0), (0, 0, 0), (0, -h, 0), (w, -h, 0)]))

    alph = self.im.split()[-1]  #keep alpha
    draw = ImageDraw.Draw(self.im)
    draw.rectangle((0, 1, self.ix, self.iy), fill=col)
    self.im.putalpha(alph)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw',RGBs)
    self._tex = ctypes.c_int()
