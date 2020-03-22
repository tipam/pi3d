from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.loader import loaderEgg
from pi3d.loader import loaderObj
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Model(Shape):
  """ 3d model inherits from Shape
  loads vertex, normal, uv, index, texture and material data from obj or egg files
  at the moment it doesn't fully implement the features such as animation,
  reflectivity etc
  """
  def __init__(self, camera=None, light=None, file_string=None,
               name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *file_string*
        path and name of obj or egg file
    """
    super(Model, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)
    if '__clone__' in file_string:
      # Creating a copy but with pointer to buf.
      return
    self.exf = file_string[-3:].lower()
    LOGGER.debug("Loading {}".format(file_string))

    if self.exf == 'egg':
      loaderEgg.loadFileEGG(self, file_string)
    elif self.exf == 'obj':
      loaderObj.loadFileOBJ(self, file_string)
    else:
      LOGGER.error("%s file not supported", self.exf)

  def clone(self, camera = None, light = None):
    """create a new Model but buf points to same array of Buffers
    so much quicker to create than reloading all the vertices etc
    """
    newModel = Model(file_string = "__clone__", x=self.unif[0], y=self.unif[1], z=self.unif[2],
               rx=self.unif[3], ry=self.unif[4], rz=self.unif[5], sx=self.unif[6], sy=self.unif[7], sz=self.unif[8],
               cx=self.unif[9], cy=self.unif[10], cz=self.unif[11])
    newModel.buf = self.buf
    newModel.vGroup = self.vGroup
    newModel.shader = self.shader
    newModel.textures = self.textures
    return newModel

  def reparentTo(self, parent):
    #TODO functionality not implemented would need to cope with Shape methods
    #if self not in parent.childModel:
    #  parent.childModel.append(self)
    pass
