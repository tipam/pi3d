from pi3d import *

class DisplayOpenGL(object):
  def __init__(self):
    b = bcm.bcm_host_init()
    assert b >= 0

    # Get the width and height of the screen
    w = c_int()
    h = c_int()
    s = bcm.graphics_get_display_size(0, ctypes.byref(w), ctypes.byref(h))
    assert s >= 0
    self.width, self.height = w.value, h.value

