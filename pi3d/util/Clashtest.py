import ctypes

from six.moves import xrange

from PIL import Image

from pi3d.constants import *

from pi3d.Shader import Shader
from pi3d.Texture import Texture

class Clashtest(Texture):
  def __init__(self):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(Clashtest, self).__init__("clashtest")
    from pi3d.Display import Display
    self.ix, self.iy = Display.INSTANCE.width, Display.INSTANCE.height
    self.im = Image.new("RGB",(self.ix, self.iy))
    self.image = self.im.convert("RGB").tostring('raw', "RGB")
    self.alpha = False
    self.blend = False

    self._tex = ctypes.c_int()
    self.framebuffer = (ctypes.c_int * 1)()
    opengles.glGenFramebuffers(1, self.framebuffer)
    self.depthbuffer = (ctypes.c_int * 1)()
    opengles.glGenRenderbuffers(1, self.depthbuffer)

    # load clashtest shader
    self.shader = Shader("clashtest")

    size = self.ix * self.iy * 3
    self.img = (ctypes.c_char * size)()

  def _load_disk(self):
    """ have to override this
    """

  def draw(self, shape):
    """ draw the shape using the clashtest Shader

    Arguments:
      *shape*
        Shape object that will be drawn
    """
    shape.draw(shader=self.shader)

  def check(self, grain=50):
    """ checks the pixels of the texture to see if there is any change from the
    first pixel sampled; in which case returns True else returns False.

    Keyword argument:
      *grain*
        Number of locations to check over the whole image
    """
    opengles.glReadPixels(0, 0, self.ix, self.iy,
                               GL_RGB, GL_UNSIGNED_BYTE,
                               ctypes.byref(self.img))
    r0 = self.img[0:3]
    step = 3 * int(self.ix * self.iy / 50)
    for i in xrange(0, len(self.img)-3, step):
      if self.img[i:(i+3)] != r0:
        return True

    return False
