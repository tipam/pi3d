import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.Camera import Camera
from pi3d.shape.LodSprite import LodSprite
from pi3d.util.OffScreenTexture import OffScreenTexture

class PostProcess(OffScreenTexture):
  """For creating a an offscreen texture that can be redrawn using shaders
  as required by the developer"""
  def __init__(self, shader="post_base", mipmap=False, add_tex=None, divide=1):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer. Keyword Arguments:

      *shader*
        to use when drawing sprite, defaults to post_base, a simple
        3x3 convolution that does basic edge detection. Can be copied to
        project directory and modified as required.

      *mipmap*
        can be set to True with slight cost to speed, or use fxaa shader

      *add_tex*
        list of textures. If additional textures can be used by the shader
        then they can be added here.
     
    """
    super(PostProcess, self).__init__("postprocess")
    # load shader
    self.shader = Shader(shader)
    dummycam = Camera.instance() # in case this is prior to one being created 
    self.camera = Camera(is_3d=False)
    self.sprite = LodSprite(z=20.0, w=self.ix, h=self.iy, n=divide)
    self.sprite.set_2d_size(w=self.ix, h=self.iy)
    self.alpha = False
    self.blend = True
    self.mipmap = mipmap
    self.tex_list = [self] # TODO check if this self reference causes graphics memory leaks
    if add_tex:
      self.tex_list.extend(add_tex)

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
    self.sprite.draw(self.shader, self.tex_list, 0.0, 0.0, self.camera)

