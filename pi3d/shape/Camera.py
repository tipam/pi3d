from pi3d import *
from pi3d.shape.Shape import Shape
from pi3d.util import Utility

class Camera(Shape):
  def __init__(self, name="", x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0):
    super(Camera, self).__init__(name, x, y, z, rx, ry, rz, 1, 1, 1)
    if VERBOSE:
      print "Creating camera ..."

  def orthographic(self, left, right, bottom, top, zoom=1, near=-1, far=10):
    opengles.glMatrixMode(GL_PROJECTION)
    Utility.load_identity()
        #opengles.glOrthof(c_float(-10), c_float(10), c_float(10), c_float(-10.0), c_float(near), c_float(far))
    opengles.glOrthof(c_float(left / zoom),
                      c_float(right / zoom),
                      c_float(bottom / zoom),
                      c_float(top / zoom),
                      c_float(near), c_float(far))
    opengles.glMatrixMode(GL_MODELVIEW)
    Utility.load_identity()

  def perspective(self, w, h, zoom, near=1, far=500):
    opengles.glMatrixMode(GL_PROJECTION)
    Utility.load_identity()
    hht = near * math.tan(math.radians(45.0))
    hwd = hht * w / h
    opengles.glFrustumf(c_float(-hwd), c_float(hwd),
                        c_float(-hht), c_float(hht),
                        c_float(near), c_float(far))
    opengles.glMatrixMode(GL_MODELVIEW)
