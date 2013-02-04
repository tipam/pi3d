import ctypes
import Image

from pi3d import *
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
    self.shader = Shader("shaders/clashtest")

    size = self.ix * self.iy * 3
    self.img = (ctypes.c_char * size)()

  def _load_disk(self):
    """ have to override this
    """

  def start_check(self):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. If you want blurred
    edges you will have to capture the rendering of an object and its
    background then re-draw them using the blur() method. Large objects
    will obviously take a while to draw and re-draw
    """
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
    opengles.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self._tex.value, 0)
    #thanks to PeterO c.o. RPi forum for pointing out missing depth attchmnt
    opengles.glBindRenderbuffer(GL_RENDERBUFFER, self.depthbuffer)
    opengles.glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16,
                self.ix, self.iy)
    opengles.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER, self.depthbuffer)
    #opengles.glClearColor(ctypes.c_float(0.0), ctypes.c_float(0.0), ctypes.c_float(0.0), ctypes.c_float(0.0))
    opengles.glClear(GL_DEPTH_BUFFER_BIT)
    opengles.glClear(GL_COLOR_BUFFER_BIT)

    opengles.glEnable(GL_TEXTURE_2D)
    opengles.glActiveTexture(0)

    #assert opengles.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE

  def end_check(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    opengles.glBindTexture(GL_TEXTURE_2D, 0)
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

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
    opengles.glReadPixels(0, 0, self.ix, self.iy, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(self.img))
    r0 = self.img[0:3]
    step = 3 * int(self.ix * self.iy / 50)
    for i in xrange(0, len(self.img)-3, step):
      if self.img[i:(i+3)] != r0:
        return True
        
    return False
