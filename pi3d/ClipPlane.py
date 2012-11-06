# Added by Patrick Gaunt, 10-07-2012

from pi3d.pi3dCommon import *
from pi3d import Constants

class ClipPlane():
  def __init__(self, no=0, x=0, y=0, z=1, w=60):
    self.no = eglint(GL_CLIP_PLANE0 + no)
    self.equation = eglfloats((x, y, z, w))
    opengles.glClipPlanef(self.no, self.equation)

  def enable(self):
    opengles.glEnable(self.no)

  def disable(self):
    opengles.glDisable(self.no)