import ctypes
import Image

from PIL import ImageDraw, ImageFont

from pi3d.constants import *
from pi3d.Texture import Texture

class Ttffont(Texture):
  """Loads a Ttf font from disk and creates a Texture and lookup table for
  the String class to write with"""
  def __init__(self, font, col="#ffffff", fontsize=48, imagesize=512):
    """Arguments:
    
      *font*
        file path/name to a ttf file
        
    Keyword arguments:
    
      *col*
        colour in standard hex format #RRGGBB
      *fontsize*
        point size for drawing the letters on the internal Texture
      *imagesize*
        pixels square, needs to be bigger for large point size
    """
    super(Ttffont, self).__init__(font)
    self.font = font
    imgfont = ImageFont.truetype(font, fontsize)

    self.im = Image.new("RGBA", (imagesize, imagesize))
    self.alpha = True
    self.ix, self.iy = imagesize, imagesize

    self.ch = []

    draw = ImageDraw.Draw(self.im)

    curX = 0.0
    curY = 0.0
    characters = []
    maxRowHeight = 0.0
    for i in range(32, 128):
      ch = chr(i)

      chwidth, chheight = imgfont.getsize(ch)

      if curX + chwidth*1.1 >= imagesize:
        curX = 0.0
        curY = curY + maxRowHeight
        maxRowHeight = 0.0

      if chheight > maxRowHeight:
        maxRowHeight = chheight

      draw.text((curX, curY), ch, font = imgfont, fill = col)
      x = (curX + 0.0) / self.ix
      y = (curY + chheight + 0.0) / self.iy
      tw = (chwidth + 0.0) / self.ix
      th = (chheight + 0.0) / self.iy
      w = imagesize
      h = imagesize

      self.ch.append((chwidth, chheight,
              [(x + tw, y - th), (x, y - th), (x, y), (x + tw, y)],
              [(chwidth, 0, 0),  (0, 0, 0),  (0, -chheight, 0),  (chwidth, -chheight, 0)]))

      curX = curX + chwidth*1.1 # to avoid overlapping corners of italics

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()

  def _load_disk(self):
    """
    we need to stop the normal file loading by overriding this method
    """
