from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
from pi3d.Shader import Shader
import sys
import os

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

    ww = w / 2.0
    hh = h / 2.0 if not flip else -h / 2.0

    verts = ((-ww, hh, 0.0), (ww, hh, 0.0), (ww, -hh, 0.0), (-ww, -hh, 0.0))
    norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1), (0, 0, -1))
    texcoords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0 , 1.0))

    inds = ((3, 0, 1), (1, 2, 3)) if not flip else ((0, 3, 2), (2, 1, 0))

    self.buf = [Buffer(self, verts, texcoords, inds, norms)]

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


class ButtonSprite(Shape):
  """ Stretches the middle part of an image to allow increased detail around
  edges and in corners"""
  def __init__(self, camera=None, light=None, w=1.0, h=1.0, corner=0.1, name="",
               texture=None, shader=None,
               x=0.0, y=0.0, z=20.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """Uses standard constructor for Shape. Extra Keyword arguments:

      *w*
        Width.
      *h*
        Height.
      *corner*
        The size that the edge thirds will be. Used for mapping textures to plane
    """
    super(ButtonSprite, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                 sx, sy, sz, cx, cy, cz)
    self.width = w
    self.height = h
    self.corner = corner
    verts = []
    norms = []
    texcoords = []
    inds = []

    ww = w / 2.0
    hh = h / 2.0

    for (j, y) in enumerate((hh, hh - corner, -hh + corner, -hh)):
        y_uv = j / 3.0
        for (i, x) in enumerate((-ww, -ww + corner, ww - corner, ww)):
            x_uv = i / 3.0
            verts.extend([[x, y, 0.0]])
            norms.extend([[0.0, 0.0, -1.0]])
            texcoords.extend([[x_uv, y_uv]])
            if i > 0 and j > 0:
                n = j * 4 + i
                inds.extend([[n-1, n-5, n-4],[n-4, n, n-1]])

    self.buf = [Buffer(self, verts, texcoords, inds, norms)]
    if texture is None:
        for p in sys.path:
            img_path = os.path.join(p, "pi3d/shape/button_image.png")
            if os.path.exists(img_path):
                texture = Texture(img_path)
                break
    else:
        if not isinstance(texture, Texture): # i.e. can load from file name
            texture = Texture(texture)
    if shader is None:
        shader = Shader("uv_flat")
    else:
        if not isinstance(shader, Shader):
            shader = Shader(shader)
    self.set_draw_details(shader, [texture])

  def repaint(self, t):
    self.draw()