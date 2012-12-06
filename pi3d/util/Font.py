import ctypes
import Image

from PIL import ImageDraw

from pi3d import *

# Text and fonts
# NEEDS FIXING - TEXTURES NEED CLEANING UP

class Font(object):
  def __init__(self, font, col="#ffffff"):
    self.font = font
    im = Image.open("fonts/%s.png" % font)
    self.ix, self.iy = im.size
    pixels = im.load()
    self.alpha = True
    self.blend = True

    self.chr = []
    #extract font information from top scanline of font image;
    #Create width,height,tex_coord and vertices for each char ...
    for v in range(95):
      x =(pixels[v * 2, 0][0] * 2.0) / self.ix  #x coord in image for this char
      y = ((pixels[v * 2, 0][1] + 8) * 2.0) / self.iy  #y coord in image for this char
      w = pixels[v * 2 + 1, 0][0] * 1.0   #width of this char
      h = pixels[v * 2 + 1, 0][1] * 1.0   #height of this char
      tw = w / self.ix
      th = h / self.iy

      self.chr.append((w, h, 
        [(x + tw, y - th), (x, y - th),  (x, y), (x + tw, y)], 
        [(w, 0, 0), (0, 0, 0), (0, -h, 0), (w, -h, 0)]))

    alph = im.split()[-1]  #keep alpha
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 1, self.ix, self.iy), fill=col)
    im.putalpha(alph)

    image = im.convert("RGBA").tostring("raw", "RGBA")
    self.tex = ctypes.c_int()
    
    #TODO this ought to be handled by Texture rather than duplicate code, maybe inherit from Texure?
    opengles.glGenTextures(1, ctypes.byref(self.tex), 0)
    opengles.glBindTexture(GL_TEXTURE_2D, self.tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          ctypes.string_at(image, len(image)))
    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, c_float(GL_LINEAR_MIPMAP_LINEAR))
    opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, c_float(GL_LINEAR))
    opengles.glGenerateMipmap(GL_TEXTURE_2D)
    opengles.glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

