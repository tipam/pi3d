from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Lathe(Shape):
  """ 3d model inherits from Shape.
  Makes a shape by rotating a path of x,y locations around the y axis
  NB the path should start at the top of the object to generate the correct normals
  also in order for edges to show correctly include a tiny bevel
  i.e. [..(0,2),(2,1),(1.5,0)..] has a sharp corner at 2,1 and should be entered as
  [..(0,2),(2,1),(2,0.999),(1.5,0)..] to get good shading
  """
  def __init__(self, camera=None, light=None, path=None, sides=12, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *path*
        Array of coordinates rotated to form shape [(x0,y0),(x1,y1)..]
      *sides*
        Number of sides for Shape._lathe() to use.
    """
    super(Lathe, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating lathe ...")

    self.path = path if path != None else []

    self.buf = [self._lathe(path, sides)]

  # TODO intervene in call to Buffer.draw() so that face culling can be disabled
  #this draw method disables face culling which allows the backs of faces to show,
  #however the normals will be wrong and it will look as if it is illuminated from the opposite direction to the light source
  #def draw(self, tex=None, shl=GL_UNSIGNED_SHORT):
  #  opengles.glDisable(GL_CULL_FACE)
  #  super(Lathe, self).draw(tex, shl)
  #  opengles.glEnable(GL_CULL_FACE)
