import array
import fcntl
import struct
from pi3d.event import ioctl

def EVIOCGABS(axis):
  return ioctl._IOR(ord('E'), 0x40 + axis, "ffffff")	# get abs value/limits

class AbsAxisScaling(object):
  """
  Fetches and implements the EV_ABS axis scaling.

  The constructor fetches the scaling values from the given stream for the
  given axis using an ioctl.

  There is a scale method, which scales a given value to the range -1..+1.
  """
  def __init__(self, stream, axis):
    """
    Fetch the scale values for this stream and fill in the instance
    variables accordingly.
    """
    s = array.array("i", [1, 2, 3, 4, 5, 6])
    try:
      x = fcntl.ioctl(stream.filehandle, EVIOCGABS(axis), s)
    except IOError:
      self.value = self.minimum = self.maximum = self.fuzz = self.flat = self.resolution = 1
    else:
      self.value, self.minimum, self.maximum, self.fuzz, self.flat, self.resolution = struct.unpack("iiiiii", s)

  def __str__(self):
    return "Value {0} Min {1}, Max {2}, Fuzz {3}, Flat {4}, Res {5}".format(self.value, self.minimum, self.maximum, self.fuzz, self.flat, self.resolution)

  def scale(self, value):
    """
    scales the given value into the range -1..+1
    """
    return (float(value) - float(self.minimum)) / float(self.maximum - self.minimum) * 2.0 - 1.0

