import ctypes

from six.moves import xrange

from PIL import Image

from pi3d.constants import *

from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture

class Clashtest(OffScreenTexture):
  def __init__(self):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(Clashtest, self).__init__("clashtest")
    # load clashtest shader
    self.shader = Shader("clashtest")

    self.img = (ctypes.c_char * (self.ix * 3))()
    self.step = 3 * int(self.ix / 50)
    self.img_sz = len(self.img)-3
    self.s_flg = False
    self.y0 = int(self.iy / 2)

  def draw(self, shape):
    """ draw the shape using the clashtest Shader

    Arguments:
      *shape*
        Shape object that will be drawn
    """
    if not self.s_flg:
      opengles.glEnable(GL_SCISSOR_TEST)
      opengles.glScissor(ctypes.c_int(int(0)), ctypes.c_int(self.y0),
                    ctypes.c_int(self.ix), ctypes.c_int(1))
      self.s_flg = True
    shape.draw(shader=self.shader)

  def check(self, grain=50):
    """ checks the pixels of the texture to see if there is any change from the
    first pixel sampled; in which case returns True else returns False.

    Keyword argument:
      *grain*
        Number of locations to check over the whole image
    """
    opengles.glDisable(GL_SCISSOR_TEST)
    self.s_flg = False
    opengles.glReadPixels(0, self.y0, self.ix, 1,
                               GL_RGB, GL_UNSIGNED_BYTE,
                               ctypes.byref(self.img))
    r0 = self.img[0:3]
    for i in xrange(0, self.img_sz, self.step):
      if self.img[i:(i+3)] != r0:
        return True

    return False
