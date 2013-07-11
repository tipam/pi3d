from pi3d.Display import Display
from Xlib import X
            
class Mouse(object):
  def __init__(self):
    pass
    
  def __init__(self, mouse='mice', restrict=True, width=1920, height=1200):
    """
    Arguments:
      *mouse*
        /dev/input/ device name
      *restrict*
        stops or allows the mouse x and y values to carry on going beyond:
      *width*
        mouse x limit
      *height*
        mouse y limit
    """
    self.width = width
    self.height = height
    self.restrict = restrict
    self.reset()

  def reset(self):
    self._x = self._y = self._dx = self._dy = 0

  def start(self):
    pass
    
  def run(self):
    pass

  def _update_pointer(self):
    n = len(Display.INSTANCE.event_list)
    for i, e in enumerate(Display.INSTANCE.event_list):
      if e.type == X.MotionNotify:
        Display.INSTANCE.event_list.pop(i)
        self._dx = e.root_x - self._x
        self._dy = e.root_y - self._y
        self._x = e.root_x
        self._y = e.root_y
        return True
    return False

  def position(self):
    self._update_pointer()
    return self._x, self._y

  def velocity(self):
    self._update_pointer()
    return self._dx, self._dy

  def stop(self):
    pass

  #TODO add more methods so this can be used by the modified InputEvents class
