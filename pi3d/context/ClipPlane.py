# Added by Patrick Gaunt, 10-07-2012

import ctypes

from pi3d import *
from pi3d.constants import *

class ClipPlane():
  def __init__(self, no=0, x=0, y=0, z=1, w=60):
    self.no = ctypes.c_int(GL_CLIP_PLANE0 + no)
    self.equation = c_floats((x, y, z, w))
    opengles.glClipPlanef(self.no, self.equation)

  def enable(self):
    # TODO: perhaps a context manager?
    opengles.glEnable(self.no)

  def disable(self):
    opengles.glDisable(self.no)
