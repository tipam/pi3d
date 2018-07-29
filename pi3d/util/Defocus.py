import ctypes

from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture

class Defocus(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(Defocus, self).__init__("defocus")
    # load blur shader
    self.shader = Shader("defocus")

  def start_blur(self):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. If you want blurred
    edges you will have to capture the rendering of an object and its
    background then re-draw them using the blur() method. Large objects
    will obviously take a while to draw and re-draw
    """
    super(Defocus, self)._start()

  def end_blur(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    super(Defocus, self)._end()

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

