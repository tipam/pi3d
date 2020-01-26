import ctypes, time
import numpy as np

import pi3d
from pi3d.constants import (GL_FRAMEBUFFER, GL_RENDERBUFFER, GL_COLOR_ATTACHMENT0,
                    GL_TEXTURE_2D, GL_DEPTH_COMPONENT16, GL_DEPTH_ATTACHMENT,
                    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_TEXTURE_MIN_FILTER,
                    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_NEAREST,
                    GL_LINEAR, GL_CLAMP_TO_EDGE, GL_UNSIGNED_BYTE, GL_RGBA, GL_DEPTH_COMPONENT,
                    GL_UNSIGNED_SHORT, GLuint, GLsizei, PLATFORM, PLATFORM_PI)

OFFSCREEN_QUEUE = []

class TextureShell():
  """ Allows OffscreenTexture to hold a color texture and a depth texture that can be
  added to Buffer.texture allowing it to have tex() function called as with a normal Texture
  """
  def __init__(self, _tex, ix, iy, blend, mipmap):
    self._tex = _tex
    self.ix = ix
    self.iy = iy
    self.blend = False
    self.mipmap = False

  def tex(self):
    return self._tex

class OffScreenTexture(object):
  """For creating special effect after rendering to texture rather than
  onto the display. Used by Defocus, ShadowCaster, Clashtest etc
  """
  def __init__(self, name=""):
    """ new system doesn't use Texture
    """
    from pi3d.Display import Display
    self.disp = Display.INSTANCE
    self.ix, self.iy = self.disp.width, self.disp.height

    color = GLuint()
    depth = GLuint()
    self.framebuffer = (GLuint * 1)()
    pi3d.opengles.glGenFramebuffers(GLsizei(1), self.framebuffer)
    self.depthbuffer = (GLuint * 1)()
    pi3d.opengles.glGenRenderbuffers(GLsizei(1), self.depthbuffer)

    pi3d.opengles.glGenTextures(1, ctypes.byref(color))
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, color)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    pi3d.opengles.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.ix,
                    self.iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    pi3d.opengles.glGenerateMipmap(GL_TEXTURE_2D)
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, 0)

    pi3d.opengles.glGenTextures(1, ctypes.byref(depth))
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, depth)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    pi3d.opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    pi3d.opengles.glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT16, self.ix,
                    self.iy, 0, GL_DEPTH_COMPONENT, GL_UNSIGNED_SHORT, None)
    pi3d.opengles.glGenerateMipmap(GL_TEXTURE_2D)
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, 0)
    pi3d.opengles.glEnable(GL_TEXTURE_2D)

    self.color = TextureShell(color, self.ix, self.iy, False, True)
    self.depth = TextureShell(depth, self.ix, self.iy, False, True)

  def _start(self, clear=True):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. Large objects
    will obviously take a while to draw and re-draw
    """
    self.disp.offscreen_tex = True # flag used in Buffer.draw()
    pi3d.opengles.glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer[0])
    #thanks to PeterO c.o. RPi forum for pointing out missing depth attchmnt
    pi3d.opengles.glBindRenderbuffer(GL_RENDERBUFFER, self.depthbuffer[0])
    pi3d.opengles.glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16,
                self.ix, self.iy)
    pi3d.opengles.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER, self.depthbuffer[0])
    pi3d.opengles.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self.color._tex.value, 0)
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, 0) # this seems to be needed here
    if PLATFORM != PLATFORM_PI: # depth capture this way doesn't work with bcm
      pi3d.opengles.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                  GL_TEXTURE_2D, self.depth._tex.value, 0)
    if clear: # TODO allow just depth or just color clearing?
      pi3d.opengles.glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    #assert opengles.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE

    global OFFSCREEN_QUEUE
    if self not in OFFSCREEN_QUEUE:
        OFFSCREEN_QUEUE.append(self)

  def _end(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    self.disp.offscreen_tex = False # flag used in Buffer.draw()
    pi3d.opengles.glBindTexture(GL_TEXTURE_2D, 0)
    pi3d.opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

    global OFFSCREEN_QUEUE
    del OFFSCREEN_QUEUE[-1]
    if OFFSCREEN_QUEUE:
        # resume previously active offscreen texture if any
        OFFSCREEN_QUEUE[-1]._start(clear=False)

  def tex(self):
    return self.color.tex()

  @property
  def blend(self):
    return self.color.blend
  @blend.setter
  def blend(self, val):
    self.color.blend = val

  @property
  def mipmap(self):
    return self.color.mipmap
  @mipmap.setter
  def mipmap(self, val):
    self.color.mipmap = val

  def delete_buffers(self):
    pi3d.opengles.glDeleteFramebuffers(GLsizei(1), self.framebuffer)
    pi3d.opengles.glDeleteRenderbuffers(GLsizei(1), self.depthbuffer)
