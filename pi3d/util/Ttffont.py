import ctypes
import Image

try:
  from PIL import ImageDraw, ImageFont
except:
  print 'Unable to import libraries from PIL'

from pi3d.constants import *
from pi3d.Texture import Texture

class Ttffont(Texture):
  """A Ttffont contains a TrueType font ready to be rendered in OpenGL.

  A font is just a mapping from codepoints (single Unicode characters) to glyphs
  (graphical representations of those characters).

  Ttffont packs one whole font into a single Texture using PIL.ImageFont,
  then creates a table mapping codepoints to subrectangles of that Texture.

"""

  def __init__(self, font, color="#ffffff", font_size=48, image_size=512,
               italic_adjustment=1.1):
    """
    Arguments:
      *font*
        File path/name to a TrueType font file.

    Keyword arguments:
      *color*
        Color in standard hex format #RRGGBB

      *font_size*
        Point size for drawing the letters on the internal Texture

      *image_size*
        Width and height of the Texture that backs the image.
        You'll need to adjust this up for larger fonts.

      *italic_adjustment*
        Adjusts the bounding width to take italics into account.  The default
        value is 1.1; you can get a tighter bounding if you set this down
        closer to 1, but italics might get cut off at the right.
    """
    super(Ttffont, self).__init__(font)
    self.font = font
    imgfont = ImageFont.truetype(font, font_size)

    self.im = Image.new("RGBA", (image_size, image_size))
    self.alpha = True
    self.ix, self.iy = image_size, image_size

    self.glyph_table = []

    draw = ImageDraw.Draw(self.im)

    curX = 0.0
    curY = 0.0
    characters = []
    maxRowHeight = 0.0
    for i in range(32, 128):
      ch = chr(i)
      chwidth, chheight = imgfont.getsize(ch)

      if curX + chwidth * italic_adjustment >= image_size:
        curX = 0.0
        curY = curY + maxRowHeight
        maxRowHeight = 0.0

      if chheight > maxRowHeight:
        maxRowHeight = chheight

      draw.text((curX, curY), ch, font=imgfont, fill=color)
      x = (curX + 0.0) / self.ix
      y = (curY + chheight + 0.0) / self.iy
      tw = (chwidth + 0.0) / self.ix
      th = (chheight + 0.0) / self.iy
      w = image_size
      h = image_size

      table_entry = [
        chwidth,
        chheight,
        [[x + tw, y - th], [x, y - th], [x, y], [x + tw, y]],
        [[chwidth, 0, 0], [0, 0, 0], [0, -chheight, 0], [chwidth, -chheight, 0]]
        ]

      self.glyph_table.append(table_entry)

      # Correct the character width for italics.
      curX = curX + chwidth * italic_adjustment

    RGBs = 'RGBA' if self.alpha else 'RGB'
    self.image = self.im.convert(RGBs).tostring('raw', RGBs)
    self._tex = ctypes.c_int()

  def _load_disk(self):
    """
    we need to stop the normal file loading by overriding this method
    """
