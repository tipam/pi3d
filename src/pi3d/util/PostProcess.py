import ctypes

from pi3d.constants import (opengles, GL_SCISSOR_TEST, GLint, GLsizei, GL_RGBA,
                GLubyte, GL_UNSIGNED_BYTE)
from pi3d.Shader import Shader
from pi3d.Camera import Camera
from pi3d.shape.LodSprite import LodSprite
from pi3d.util.OffScreenTexture import OffScreenTexture

class PostProcess(OffScreenTexture):
  """For creating a an offscreen texture that can be redrawn using shaders
  as required by the developer"""
  def __init__(self, shader="post_base", mipmap=False, add_tex=None,
              scale=1.0, camera=None, divide=1):
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
        
      *scale*
        will only render this proportion of the full screen which will
        then be mapped to the full uv of the Sprite. The camera object
        passed (below) will need to have the same scale set to avoid
        perspective distortion
        
      *camera*
        the camera to use for rendering to the offscreen texture
        
      *divide*
        allow the sprite to be created with intermediate vertices to allow
        interesting vertex shader effects
     
    """
    super(PostProcess, self).__init__("postprocess")
    self.scale = scale
    # load shader
    if type(shader) == Shader:
      self.shader = shader
    else:
      self.shader = Shader.create(shader)
    if camera is None:
      self.viewcam = Camera.instance() # in case this is prior to one being created
    else:
      self.viewcam = camera
    self.camera = Camera(is_3d=False)
    self.sprite = LodSprite(camera=self.camera, z=20.0, w=self.ix, h=self.iy, n=divide)
    self.sprite.set_2d_size(w=self.ix, h=self.iy)
    self.tex_list = [self.color, self.depth] # TODO check if this self reference causes graphics memory leaks
    if add_tex:
      self.tex_list.extend(add_tex)
    self.sprite.set_draw_details(self.shader, self.tex_list, 0.0, 0.0)
    for b in self.sprite.buf:
      b.unib[6] = self.scale # ufact
      b.unib[7] = self.scale # vfact
      b.unib[9] = (1.0 - self.scale) * 0.5 # uoffset
      b.unib[10] = (1.0 - self.scale) * 0.5 # voffset
    self.blend = True
    self.mipmap = mipmap

  def start_capture(self, clear=True):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. Large objects
    will obviously take a while to draw and re-draw
    """
    super(PostProcess, self)._start(clear=clear)
    from pi3d.Display import Display
    xx = int(Display.INSTANCE.width / 2.0 * (1.0 - self.scale)) - 1
    yy = int(Display.INSTANCE.height / 2.0 * (1.0 - self.scale)) - 1
    ww = int(Display.INSTANCE.width * self.scale) + 2
    hh = int(Display.INSTANCE.height * self.scale) + 2
    opengles.glEnable(GL_SCISSOR_TEST)
    opengles.glScissor(GLint(xx), GLint(yy), GLsizei(ww), GLsizei(hh))

  def end_capture(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    super(PostProcess, self)._end()
    opengles.glDisable(GL_SCISSOR_TEST)

  def draw(self, unif_vals=None):
    """ draw the shape using the saved texture
    Keyword Argument:
    
      *unif_vals*
        dictionay object i.e. {a:unif[a], b:unif[b], c:unif[c]} where a,b,c
        are subscripts of the unif array in Shape available for user
        custom space i.e. unif[48]...unif[59] corresponding with the vec3
        uniform variables unif[16][0] to unif[19][2]
        NB the values must be three value tuples or 1D arrays
    """
    if unif_vals:
      for i in unif_vals:
        self.sprite.unif[i] = unif_vals[i]
    self.sprite.draw()
