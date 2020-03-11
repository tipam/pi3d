import ctypes

from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Camera import Camera

class ShadowCaster(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self, position, light, scale=10.0):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(ShadowCaster, self).__init__("shadow_caster")

    self.LIGHT_CAM = Camera(is_3d=False, scale=scale)
    l_p = light.lightpos
    l_len = (l_p[0]**2 + l_p[1]**2 + l_p[2]**2)**0.5
    self.OFFSET = [200.0 * i / l_len for i in l_p]
    self.LIGHT_CAM.position([position[i] - o for i, o in enumerate(self.OFFSET)])
    self.tilt, self.rot = self.LIGHT_CAM.point_at(position)
    self.cast_shader = Shader("shadowcast")


  def move_light(self, position):
    self.LIGHT_CAM.reset()
    self.LIGHT_CAM.rotate(self.tilt, self.rot, 0)
    self.LIGHT_CAM.position([position[i] - o for i, o in enumerate(self.OFFSET)])


  def start_cast(self, position=None):
    if position is not None:
      self.move_light(position)
    super(ShadowCaster, self)._start()


  def cast_shadow(self, shape):
    shape.draw(shader=self.cast_shader, light_camera=self.LIGHT_CAM)


  def end_cast(self):
    super(ShadowCaster, self)._end()


  def draw_shadow(self):
    self.emap.draw(shader=self.dshader)


  def draw_tree(self, tree, shader):
    tree.draw(shader, [self.color])

