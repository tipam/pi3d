from pi3d.constants import *
from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape

class Sprite(Shape):
  """ 3d model inherits from Shape, differs from Plane in being single sided"""
  def __init__(self, camera=None, light=None, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=20.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0, flip=False):
    """Uses standard constructor for Shape. Extra Keyword arguments:

      *w*
        Width.
      *h*
        Height.
      *flip*
        If set to True then the Sprite is flipped vertically (top to bottom)
    """
    super(Sprite, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                 sx, sy, sz, cx, cy, cz)
    self.width = w
    self.height = h
    self.ttype = GL_TRIANGLES
    self.verts = []
    self.norms = []
    self.texcoords = []
    self.inds = []

    ww = w / 2.0
    hh = h / 2.0 if not flip else -h / 2.0

    self.verts = ((-ww, hh, 0.0), (ww, hh, 0.0), (ww, -hh, 0.0), (-ww, -hh, 0.0))
    self.norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1), (0, 0, -1))
    self.texcoords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0 , 1.0))

    self.inds = ((3, 0, 1), (1, 2, 3)) if not flip else ((0, 3, 2), (2, 1, 0))

    self.buf = []
    self.buf.append(Buffer(self, self.verts, self.texcoords, self.inds, self.norms))

  def repaint(self, t):
    self.draw()


class ImageSprite(Sprite):
  """A 2D sprite containing a texture and shader. The constructor also
  calls set_2d_size so that ImageSprite objects can be used directly to draw
  on a Canvas shape (if shader=2d_flat). Additional arguments:

    *texture*
      either a Texture object or, if not a Texture, will attempt to load
      a file using texture as a path and name to an image.
    *shader*
      a Shader object
  """
  def __init__(self, texture, shader, **kwds):
    super(ImageSprite, self).__init__(**kwds)
    if not isinstance(texture, Texture): # i.e. can load from file name
      texture = Texture(texture)
    self.set_shader(shader)
    self.buf[0].set_draw_details(shader, [texture])
    self.set_2d_size() # method in Shape, default full window size

  def _load_opengl(self):
    self.buf[0].textures[0].load_opengl()

  def _unload_opengl(self):
    self.buf[0].textures[0].unload_opengl()
