import fcntl
import os
import select
import logging

from pi3d.event.Constants import *

from pi3d.event import ioctl
from pi3d.event import AbsAxisScaling
from pi3d.event import EventStruct
from pi3d.event import Format

LOGGER = logging.getLogger(__name__)

EVIOCGRAB = ioctl._IOW(ord('E'), 0x90, "i")          # Grab/Release device

class EventStream(object):
  """
  encapsulates the event* file handling

  Each device is represented by a file in /dev/input called eventN, where N is
  a small number. (Actually, a keybaord is/can be represented by two such files.)
  Instances of this class open one of these files and provide means to read
  events from them.

  Class methods also exist to read from multiple files simultaneously, and
  also to grab and ungrab all instances of a given type.
  """
  AllStreams = [ ]
  axisX = 0
  axisY = 1
  axisZ = 2
  axisRX = 3
  axisRY = 4
  axisRZ = 5
  axisHat0X = 6
  axisHat0Y = 7
  axisHat1X = 8
  axisHat1Y = 9
  axisHat2X = 10
  axisHat2Y = 11
  axisHat3X = 12
  axisHat3Y = 13
  axisThrottle = 14
  axisRudder = 15
  axisWheel = 16
  axisGas = 17
  axisBrake = 18
  axisPressure = 19
  axisDistance = 20
  axisTiltX = 21
  axisTiltY = 22
  axisToolWidth = 23
  numAxes = 24

  axisToEvent = [ABS_X, ABS_Y, ABS_Z,  ABS_RX, ABS_RY,  ABS_RZ,
    ABS_HAT0X, ABS_HAT0Y, ABS_HAT1X, ABS_HAT1Y,
    ABS_HAT2X, ABS_HAT2Y, ABS_HAT3X, ABS_HAT3Y,
    ABS_THROTTLE, ABS_RUDDER, ABS_WHEEL, ABS_GAS, ABS_BRAKE,
    ABS_PRESSURE, ABS_DISTANCE, ABS_TILT_X, ABS_TILT_Y, ABS_TOOL_WIDTH]

  def __init__(self, index, deviceType):
    """
    Opens the given /dev/input/event file and grabs it.

    Also adds it to a class-global list of all existing streams.
    The index is a tuple: (deviceIndex, eventIndex). The deviceIndex
    can be used subsequently for differentiating multiple devices of the
    same type.
    """
    self.index = index[1]
    self.deviceIndex = index[0]
    self.deviceType = deviceType
    self.filename = "/dev/input/event"+str(self.index)
    self.filehandle = os.open(self.filename, os.O_RDWR)
    self.grab(True)
    self.grabbed = True
    EventStream.AllStreams.append(self)
    self.absInfo = [None] * EventStream.numAxes

  #def acquire_abs_info(self, axis):
  #  assert (axis < EventStream.numAxes), "Axis number out of range"
  #  self.absinfo[axis] = AbsAxisScaling(EventStream.axisToEvent[axis])

  def acquire_abs_info(self):
    """
    Acquires the axis limits for all the ABS axes.

    This will only be called for joystick-type devices.
    """
    for axis in range(EventStream.numAxes):
      self.absInfo[axis] = AbsAxisScaling.AbsAxisScaling(self, EventStream.axisToEvent[axis])

  def scale(self, axis, value):
    """
    Scale the given value according to the given axis.

    acquire_abs_info must have been previously called to acquire the data to
    do the scaling.
    """
    assert (axis < EventStream.numAxes), "Axis number out of range"
    if self.absInfo[axis]:
      return self.absInfo[axis].scale(value)
    else:
      return value

  def grab(self, grab=True):
    """
    Grab (or release) exclusive access to all devices of the given type.

    The devices are grabbed if grab is True and released if grab is False.

    All devices are grabbed to begin with. We might want to ungrab the
    keyboard for example to use it for text entry. While not grabbed, all key-down
    and key-hold events are filtered out.
    """
    #print "grab(", self, ",", grab,") =", 1 if grab else 0, "with 0x%x"%(EVIOCGRAB)
    fcntl.ioctl(self.filehandle, EVIOCGRAB, 1 if grab else 0)
    self.grabbed = grab
    #flush outstanding events
    #while self.next(): pass

  def __iter__(self):
    """
    Required to make this class an iterator
    """
    return self

  def next(self):
    """
    Returns the next waiting event.

    If no event is waiting, returns None.
    """
    ready = select.select([self.filehandle],[ ], [ ], 0)[0]
    if ready:
      s = os.read(self.filehandle, Format.EventSize)
      if s:
        event = EventStruct.EventStruct(self)
        event.decode(s)
        return event

    return None

  @classmethod
  def grab_by_type(self, deviceType, deviceIndex=None, grab=True, streams=None):
    """
    Grabs all streams of the given type.
    """
    if streams is None:
      streams = EventStream.AllStreams

    for x in streams:
      if x.deviceType == deviceType and (deviceIndex is None or
                                        x.deviceIndex == deviceIndex):
        x.grab(grab)

  @classmethod
  def allNext(cls, streams=None):
    """
    A generator fuction returning all waiting events in the given streams

    If the streams parameter is not given, then all streams are selected.
    """
    if streams is None:
      streams = EventStream.AllStreams

    selectlist = [x.filehandle for x in streams]
    ready = select.select(selectlist, [ ], [ ], 0)[0]
    if not ready: return
    while ready:
      for fd in ready:
        try:
          s = os.read(fd, Format.EventSize)
        except Exception as e:
          LOGGER.error("Couldn't read fd %d %s", fd, e)
          selectlist.remove(fd)
          s = None
        for x in streams:
          if x.filehandle == fd:
            stream = x
            break
        event = EventStruct.EventStruct(stream)
        if s:
          event.decode(s)
        yield event
      ready = select.select(selectlist, [ ], [ ], 0)[0]

  def __enter__(self):
    return self

  def release(self):
    """
    Ungrabs the file and closes it.
    """
    try:
      EventStream.AllStreams.remove(self)
      self.grab(False)
      os.close(self.filehandle)
    except:
      pass

  def __exit__(self, type, value, traceback):
    """
    Ungrabs the file and closes it.
    """
    self.release()
