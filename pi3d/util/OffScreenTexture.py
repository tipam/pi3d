import ctypes, time
import numpy as np

import pi3d
from pi3d.constants import (GL_FRAMEBUFFER, GL_RENDERBUFFER, GL_COLOR_ATTACHMENT0,
                    GL_TEXTURE_2D, GL_DEPTH_COMPONENT16, GL_DEPTH_ATTACHMENT,
                    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT)
from pi3d.Texture import Texture

class OffScreenTexture(Texture):
  """For creating special effect after rendering to texture rather than
  onto the display. Used by Defocus, ShadowCaster, Clashtest etc
  """
  def __init__(self, name):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(OffScreenTexture, self).__init__(name)
    from pi3d.Display import Display
    self.disp = Display.INSTANCE
    self.ix, self.iy = self.disp.width, self.disp.height
    self.image = np.zeros((self.iy, self.ix, 4), dtype=np.uint8)
    self.blend = False
    self.mipmap = False

    self._tex = ctypes.c_uint()
    self.framebuffer = (ctypes.c_uint * 1)()
    pi3d.opengles.glGenFramebuffers(1, self.framebuffer)
    self.depthbuffer = (ctypes.c_uint * 1)()
    pi3d.opengles.glGenRenderbuffers(1, self.depthbuffer)

  def _load_disk(self):
    """ have to override this
    """

  def _start(self, clear=True):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. Large objects
    will obviously take a while to draw and re-draw
    """
    self.disp.offscreen_tex = True # flag used in Buffer.draw()
    pi3d.opengles.glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer[0])
    pi3d.opengles.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self._tex.value, 0)
    #thanks to PeterO c.o. RPi forum for pointing out missing depth attchmnt
    pi3d.opengles.glBindRenderbuffer(GL_RENDERBUFFER, self.depthbuffer[0])
    pi3d.opengles.glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16,
                self.ix, self.iy)
    pi3d.opengles.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER, self.depthbuffer[0])
    if clear: # TODO allow just depth or just color clearing?
      pi3d.opengles.glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    #assert opengles.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE

  def _end(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    self.disp.offscreen_tex = False # flag used in Buffer.draw()
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, 0)
    pi3d.opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

    
  def delete_buffers(self):
    pi3d.opengles.glDeleteFramebuffers(1, self.framebuffer)
    pi3d.opengles.glDeleteRenderbuffers(1, self.depthbuffer)

