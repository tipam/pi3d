import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.Texture import Texture

class Defocus(Texture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(Defocus, self).__init__("defocus")
    from pi3d.Display import Display
    self.ix, self.iy = Display.INSTANCE.width, Display.INSTANCE.height
    self.im = Image.new("RGBA",(self.ix, self.iy))
    self.image = self.im.convert("RGBA").tostring('raw', "RGBA")
    self.alpha = True
    self.blend = False

    self._tex = ctypes.c_int()
    self.framebuffer = (ctypes.c_int * 1)()
    opengles.glGenFramebuffers(1, self.framebuffer)
    self.depthbuffer = (ctypes.c_int * 1)()
    opengles.glGenRenderbuffers(1, self.depthbuffer)

    # load blur shader
    self.shader = Shader("defocus")

  def _load_disk(self):
    """ have to override this
    """

  def start_blur(self):
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
    opengles.glClear(GL_DEPTH_BUFFER_BIT)

    opengles.glEnable(GL_TEXTURE_2D)
    opengles.glActiveTexture(0)

    #assert opengles.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE

  def end_blur(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    opengles.glBindTexture(GL_TEXTURE_2D, 0)
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

  def blur(self, shape, dist_fr, dist_to, amount):
    """ draw the shape using the saved texture
    Arguments:
    
      *shape*
        Shape object that will be drawn
      *dist_fr*
        distance from zero plane that will be in focus, float
      *dist_to*
        distance beyond which everything will be at max blur, float
      *amount*
        degree of max blur, float. Values over 5 will cause banding
    """
    shape.unif[42] = dist_fr # shader unif[14]
    shape.unif[43] = dist_to
    shape.unif[44] = amount
    shape.unif[45] = 1.0/self.ix # shader unif[15]
    shape.unif[46] = 1.0/self.iy
    shape.draw(self.shader, [self], 0.0, 0.0)
    
  def delete_buffers(self):
    opengles.glDeleteFramebuffers(1, self.framebuffer)
    opengles.glDeleteRenderbuffers(1, self.depthbuffer)

