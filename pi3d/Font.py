import Image

from PIL import ImageDraw

from pi3d.pi3dCommon import *
from pi3d import Constants

# Text and fonts
# NEEDS FIXING - TEXTURES NEED CLEANING UP

class Font(object):
  def __init__(self, font, col="#ffffff"):
    self.font = font
    im = Image.open("fonts/%s.png" % font)
    ix,iy = im.size
    pixels = im.load()

    self.chr = []
    #extract font information from top scanline of font image;
    #Create width,height,tex_coord and vertices for each char ...
    for v in range(0,95):
      x=(pixels[v * 2, 0][0] * 2.0) / ix  #x coord in image for this char
      y=((pixels[v * 2, 0][1] + 8) * 2.0) / iy  #y coord in image for this char
      w=pixels[v * 2 + 1, 0][0] * 1.0   #width of this char
      h=pixels[v * 2 + 1, 0][1] * 1.0   #height of this char
      tw=w / ix
      th=h / iy

      self.chr.append((w, h, eglfloats((x + tw, y - th, x, y - th,
                                        x, y, x + tw, y)),
                       eglfloats((w, 0,0, 0 , 0, 0, 0, -h, 0, w, -h, 0))))

    alpha = im.split()[-1]  #keep alpha
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 1, ix, iy), fill=col)
    im.putalpha(alpha)

    #im = im.transpose(Image.FLIP_TOP_BOTTOM)
    image = im.convert("RGBA").tostring("raw", "RGBA")
    self.tex = eglint()
    opengles.glGenTextures(1,ctypes.byref(self.tex))
    opengles.glBindTexture(GL_TEXTURE_2D, self.tex)
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
                          GL_RGBA,GL_UNSIGNED_BYTE,
                          ctypes.string_at(image, len(image)))

