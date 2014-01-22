import struct

from pi3d.event import Format

class EventStruct(object):
  """
  A single event from the linux input event system.

  Events are tuples: (Time, Type, Code, Value)
  In addition we remember the stream it came from.

  Externally, only the unhandled event handler gets passed the whole event,
  but the SYN handler gets the code and value. (Also the keyboard handler, but
  those are renamed to key and value.)

  This class is responsible for converting the Linux input event structure into
  one of these objects and back again.
  """
  def __init__(self, stream, time=None, eventType=None, eventCode=None,
               eventValue=None):
    """
    Create a new event.

    Generally all but the stream parameter are left out; we will want to
    populate the object from a Linux input event using decode.
    """
    self.stream = stream
    self.time = time
    self.eventType = eventType
    self.eventCode = eventCode
    self.eventValue = eventValue

  def __str__(self):
    """
    Uses the stream to give the device type and whether it is currently grabbed.
    """
    return "Input event %s[%d], %d -- %f: 0x%x(0x%x) = 0x%x" % (
      self.stream.deviceType, self.stream.deviceIndex, self.stream.grabbed,
      self.time, self.eventType, self.eventCode, self.eventValue)

  def __repr__(self):
    return "EventStruct(%s, %f, 0x%x, 0x%x, 0x%x)" % (
      repr(self.stream), self.time, self.eventType, self.eventCode,
      self.eventValue)

  def encode(self):
    """
    Encode this event into a Linux input event structure.

    The output is packed into a string. It is unlikely that this function
    will be required, but it might as well be here.
    """
    tint = long(self.time)
    tfrac = long((self.time - tint)*1000000)
    return struct.pack(Format.Event, tsec, tfrac, self.eventType,
                       self.eventCode, self.eventValue)

  def decode(self, s):
    """
    Decode a Linux input event into the fields of this object.

    Arguments:
      *s*
        A binary structure packed into a string.
    """
    (tsec, tfrac,  self.eventType, self.eventCode,
     self.eventValue) = struct.unpack(Format.Event, s)

    self.time = tsec + tfrac / 1000000.0
