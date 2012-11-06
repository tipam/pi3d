from pi3d.pi3dCommon import *
from pi3d import Constants

class Camera(Shape):
  def __init__(self, name="", x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0):
    super(Camera, self).__init__(name, x, y, z, rx, ry, rz, 1, 1, 1)
    if Constants.VERBOSE:
      print "Creating camera ..."

  def orthographic(self, left, right, bottom, top, zoom=1, near=-1, far=10):
    opengles.glMatrixMode(GL_PROJECTION)
    opengles.glLoadIdentity()
        #opengles.glOrthof(eglfloat(-10), eglfloat(10), eglfloat(10), eglfloat(-10.0), eglfloat(near), eglfloat(far))
    opengles.glOrthof(eglfloat(left / zoom),
                      eglfloat(right / zoom),
                      eglfloat(bottom / zoom),
                      eglfloat(top / zoom),
                      eglfloat(near), eglfloat(far))
    opengles.glMatrixMode(GL_MODELVIEW)
    opengles.glLoadIdentity()

  def perspective(self, w, h, zoom, near=1, far=500):
    opengles.glMatrixMode(GL_PROJECTION)
    opengles.glLoadIdentity()
    hht = near * math.tan(math.radians(45.0))
    hwd = hht * w / h
    opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd),
                        eglfloat(-hht), eglfloat(hht),
                        eglfloat(near), eglfloat(far))
    opengles.glMatrixMode(GL_MODELVIEW)
