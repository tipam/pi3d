import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.Camera import Camera
from pi3d.shape.Sprite import Sprite
from pi3d.util.OffScreenTexture import OffScreenTexture

class PostProcess(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self, shader="post_base"):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(PostProcess, self).__init__("postprocess")
    # load shader
    self.shader = Shader(shader)
    self.camera = Camera(is_3d=False)
    self.sprite = Sprite(z=20.0, w=self.ix, h=self.iy)
    self.mipmap = False

  def start_capture(self):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. Large objects
    will obviously take a while to draw and re-draw
    """
    super(PostProcess, self)._start()

  def end_capture(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    super(PostProcess, self)._end()

  def draw(self, unif_vals=None):
    """ draw the shape using the saved texture
    Keyword Argument:
    
      *unif_vals*
        dictionay object i.e. {a:unif[a], b:unif[b], c:unif[c]} where a,b,c
        are subscripts of the unif array in Shape available for user
        custom space i.e. unif[48]...unif[59] corresponding with the vec3
        uniform variables unif[16][0] to unit[19][2]
    """
    if unif_vals:
      for i in unif_vals:
        self.sprite.unif[i] = unif_vals[i]
    self.sprite.draw(self.shader, [self], 0.0, 0.0, self.camera)

