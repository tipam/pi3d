import ctypes

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.Camera import Camera
from pi3d.shape.Sprite import Sprite
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Display import Display

class StereoCam(object):
  """For creating an apparatus with two sprites to hold left and right
  eye views.

  This Class is used to hold the 3D Camera which should be used to draw
  the 3D objects. It also holds a 2D Camera for drawing the Sprites"""
  def __init__(self, shader="uv_flat", mipmap=False, separation=0.4):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer. Keyword Arguments:

      *shader*
        to use when drawing sprite, defaults to post_base, a simple
        3x3 convolution that does basic edge detection. Can be copied to
        project directory and modified as required.

      *mipmap*
        can be set to True with slight cost to speed, or use fxaa shader

      *separation*
        distance between the two camera positions - how wide apart the
        eye views are.
    """
    # load shader
    self.shader = Shader(shader)
    self.camera_3d = Camera()
    self.camera_2d = Camera(is_3d=False)
    self.offs = separation / 2.0
    self.textures = []
    self.sprites = []
    self.tex_list = []
    for i in range(2):
      self.textures.append(OffScreenTexture(name="bin"))
      ix, iy = self.textures[i].ix, self.textures[i].iy
      #two sprites full width but moved so that they are centred on the
      #left and right edges. The offset values then move the uv mapping
      #so the image is on the right of the left sprite and left of the
      #right sprite
      self.sprites.append(Sprite(z=20.0, x=-ix/2.0 + i*ix, w=ix, h=iy, flip=True))
      self.sprites[i].set_offset((i * 0.5 - 0.25, 0.0))
      self.textures[i].alpha = False
      self.textures[i].blend = True
      self.textures[i].mipmap = mipmap
      self.tex_list.append([self.textures[i]])

  def move_camera(self, position, rot, tilt):
    self.camera_3d.reset()
    self.camera_3d.rotate(tilt, rot, 0)
    self.camera_3d.position(position)

  def start_capture(self, side):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display.

      *side*
        Either 0 or 1 to determine stereoscopic view
    """
    offs = -self.offs if side == 0 else self.offs
    self.camera_3d.position((self.camera_3d.mtrx[2,3] * offs, 0,
                            -self.camera_3d.mtrx[0,3] * offs))
    tex = self.textures[side]
    tex._start()
    xx = tex.ix / 4.0 # draw the middle only - half width
    yy = 0
    ww = tex.ix / 2.0
    hh = tex.iy
    opengles.glEnable(GL_SCISSOR_TEST)
    opengles.glScissor(ctypes.c_int(int(xx)), ctypes.c_int(int(yy)),
                  ctypes.c_int(int(ww)), ctypes.c_int(int(hh)))

  def end_capture(self, side):
    """ stop capturing to texture and resume normal rendering to default
    """
    self.textures[side]._end()
    opengles.glDisable(GL_SCISSOR_TEST)

  def draw(self):
    """ draw the shape using the saved texture
    """
    for i in range(2):
     self.sprites[i].draw(self.shader, self.tex_list[i], 0.0, 0.0, self.camera_2d)

