import ctypes
import Image

from pi3d import *
from pi3d.Shader import Shader
from pi3d.Texture import Texture

class Defocus(Texture):
  def __init__(self):
    super(Defocus, self).__init__("defocus")
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    from pi3d.Display import DISPLAY
    self.ix, self.iy = DISPLAY.width, DISPLAY.height
    self.im = Image.new("RGBA",(self.ix, self.iy)) 
    self.image = self.im.convert("RGBA").tostring('raw', "RGBA")
    self.alpha = True

    self._tex = ctypes.c_int()
    self.blend = False
    self.framebuffer = (ctypes.c_int * 24)()
    opengles.glGenFramebuffers(1, self.framebuffer)
    self.renderbuffer = (ctypes.c_int * 1024)() # is this really enough?
    opengles.glGenRenderbuffers(1, self.renderbuffer)

    # load blur shader
    self.shader = Shader("shaders/defocus")
    
  def _load_disk(self):
    """ have to override this
    """
    
  def start_blur(self):
    #opengles.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
    #opengles.glDepthRangef(c_float(1.0),c_float(-1.0))
    opengles.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._tex.value, 0)
    opengles.glEnable(GL_TEXTURE_2D)
    opengles.glActiveTexture(0)
    # none of these seem to do anything
    #opengles.glClearColor (c_float(0.3), c_float(0.3), c_float(0.7), c_float(1.0));
    #opengles.glColorMask(1, 1, 1, 0)
    #opengles.glEnable(GL_CULL_FACE)
    #opengles.glShadeModel(GL_FLAT)
    #opengles.glEnable(GL_NORMALIZE)
    #opengles.glEnable(GL_DEPTH_TEST)
    #opengles.glCullFace(GL_FRONT)
    #opengles.glHint(GL_GENERATE_MIPMAP_HINT, GL_NICEST)
    
    opengles.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE
    
  def blur(self, shape, dist_fr, dist_to, amount):
    shape.unif[42] = dist_fr # shader unif[14]
    shape.unif[43] = dist_to
    shape.unif[44] = amount
    shape.unif[45] = 1.0/self.ix # shader unif[15]
    shape.unif[46] = 1.0/self.iy
    shape.draw(self.shader, [self], 0.0, 0.0)
    
  def end_blur(self):
    opengles.glBindTexture(GL_TEXTURE_2D, 0)
    opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)
    #opengles.glBindRenderbuffer(GL_RENDERBUFFER, 0)
    #opengles.glEnable(GL_DEPTH_TEST)
    #opengles.glEnable(GL_CULL_FACE)
    #opengles.glDepthRangef(c_float(-1.0),c_float(1.0))
    #opengles.glReadPixels(0, 0, self.ix, self.iy, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(self.img))
    #self.im = Image.frombuffer('RGB', (self.ix, self.iy), self.img, 'raw', 'RGB', 0, 1)
    #self.image = self.im.convert("RGB").tostring('raw', "RGB")

    
