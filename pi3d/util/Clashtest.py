import ctypes
import numpy as np

from pi3d.constants import (opengles, GL_SCISSOR_TEST, GLint, GLsizei, GL_RGBA,
                GLubyte, GL_UNSIGNED_BYTE)

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

    self.img = np.zeros((self.ix, 4), dtype=np.uint8)
    self.step = int(self.ix / 100)
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
      opengles.glScissor(GLint(0), GLint(self.y0),
                    GLsizei(self.ix), GLsizei(1))
      self.s_flg = True
    shape.draw(shader=self.shader)

  def check(self, grain=50):
    """ checks the pixels of the texture to see if there is any change from the
    first pixel sampled; in which case returns True else returns False.

    Keyword argument:
      *grain*
        Number of locations to check over the whole image
        NB this is no longer used - there are fixed 100 checks across the
        full width at the mid y position. This self.setp value is set in
        __init__()
    """
    opengles.glDisable(GL_SCISSOR_TEST)
    self.s_flg = False
    img = self.img # alias to make code a bit less bulky!
    opengles.glReadPixels(GLint(0), GLint(self.y0), GLsizei(self.ix), GLsizei(1),
                          GL_RGBA, GL_UNSIGNED_BYTE,
                          img.ctypes.data_as(ctypes.POINTER(GLubyte)))

    if  (np.any(img[::self.step,0] != img[0,0]) or 
         np.any(img[::self.step,1] != img[0,1]) or 
         np.any(img[::self.step,2] != img[0,2])):
      return True
    return False
