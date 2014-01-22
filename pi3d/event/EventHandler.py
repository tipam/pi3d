import threading

from pi3d.event.Constants import *
from pi3d.event.EventStream import EventStream

class EventHandler(object):
  """
  A class to handle events.

  Four types of events are handled: REL (mouse movement), KEY (keybaord keys and
  other device buttons), ABS (joysticks and gamepad analogue sticks) and SYN
  (delimits simultaneous events such as mouse movements)
  """
  def __init__(self, keyHandler=None, relHandler=None, absHandler=None, synHandler=None):
    self.buttons = dict()
    self.relHandler = relHandler
    self.keyHandler = keyHandler
    self.absHandler = absHandler
    self.synHandler = synHandler

    self.mutex = threading.Lock()

    self.absx = [0.0]*4
    self.absy = [0.0]*4
    self.absz = [0.0]*4
    self.absx2 = [0.0]*4
    self.absy2 = [0.0]*4
    self.absz2 = [0.0]*4
    self.abshatx = [0.0]*4
    self.abshaty = [0.0]*4

    self.relx = [0]*4
    self.rely = [0]*4
    self.relv = [0]*4
    self.relh = [0]*4
    self.reld = [0]*4

  def event(self, event):
    """
    Handles the given event.

    If the event is passed to a handler or otherwise handled then returns None,
    else returns the event. All handlers are optional.

    All key events are handled by putting them in the self.buttons dict, and
    optionally by calling the supplied handler.

    REL X, Y and wheel V and H events are all accumulated internally and
    also optionally passed to the supplied handler. All these events are handled.

    ABS X, Y, Z, RX, RY, RZ, Hat0X, Hat0Y are all accumulated internally and
    also optionally passed to the supplied handler. Other ABS events are not
    handled.

    All SYN events are passed to the supplied handler.

    There are several ABS events that we do not handle. In particular:
    THROTTLE, RUDDER, WHEEL, GAS, BRAKE, HAT1, HAT2, HAT3, PRESSURE,
    DISTANCE, TILT, TOOL_WIDTH. Implementing these is left as an exercise
    for the interested reader.

    Likewise, since one handler is handling all events for all devices, we
    may get the situation where two devices return the same button. The only
    way to handle that would seem to be to have a key dict for every device,
    which seems needlessly profligate for a situation that may never arise.
    """
    ret = event
    self.mutex.acquire()

    try:
      Handled = False
      if event.eventType == EV_SYN:
        if self.synHandler:
          self.synHandler(event.stream.deviceType, event.stream.deviceIndex, event.eventCode, event.eventValue)
          ret = None
      elif event.eventType == EV_KEY:
        if event.stream.grabbed == False and event.eventValue != 0:
          ret = None
        self.buttons[event.eventCode] = event.eventValue
        if self.keyHandler:
          self.keyHandler(event.stream.deviceType, event.stream.deviceIndex, event.eventCode, event.eventValue)
        ret = None
      elif event.eventType == EV_REL:
        if event.eventCode == REL_X:
          self.relx[event.stream.deviceIndex] += event.eventValue
          if self.relHandler:
            self.relHandler(event.stream.deviceType, event.stream.deviceIndex, event.eventValue, 0, 0, 0)
          ret = None
        elif event.eventCode == REL_Y:
          self.rely[event.stream.deviceIndex] += event.eventValue
          if self.relHandler:
            self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0, event.eventValue, 0, 0)
          ret = None
        elif event.eventCode == REL_WHEEL:
          self.relv[event.stream.deviceIndex] += event.eventValue
          if self.relHandler:
            self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0, 0, event.eventValue, 0)
          ret = None
        elif event.eventCode == REL_HWHEEL:
          self.relh[event.stream.deviceIndex] += event.eventValue
          if self.relHandler:
            self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0, 0, 0, event.eventValue)
        elif event.eventCode == REL_DIAL:
          self.relh[event.stream.deviceIndex] += event.eventValue
          if self.relHandler:
            self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0 ,0, 0, event.eventValue)
          ret = None
      elif event.eventType == EV_ABS:
        if event.eventCode == ABS_X:
          Handled = True
          self.absx[event.stream.deviceIndex] = event.stream.scale(EventStream.axisX, event.eventValue)
        elif event.eventCode == ABS_Y:
          Handled = True
          self.absy[event.stream.deviceIndex] = event.stream.scale(EventStream.axisY, event.eventValue)
        elif event.eventCode == ABS_Z:
          Handled = True
          self.absz[event.stream.deviceIndex] = event.stream.scale(EventStream.axisZ, event.eventValue)
        elif event.eventCode == ABS_RX:
          Handled = True
          self.absx2[event.stream.deviceIndex] = event.stream.scale(EventStream.axisRX, event.eventValue)
        elif event.eventCode == ABS_RY:
          Handled = True
          self.absy2[event.stream.deviceIndex] = event.stream.scale(EventStream.axisRY, event.eventValue)
        elif event.eventCode == ABS_RZ:
          Handled = True
          self.absz2[event.stream.deviceIndex] = event.stream.scale(EventStream.axisRZ, event.eventValue)
        elif event.eventCode == ABS_HAT0X:
          Handled = True
          self.abshatx[event.stream.deviceIndex] = event.stream.scale(EventStream.axisHat0X, event.eventValue)
        elif event.eventCode == ABS_HAT0Y:
          Handled = True
          self.abshaty[event.stream.deviceIndex] = event.stream.scale(EventStream.axisHat0Y, event.eventValue)
        if Handled:
          if self.absHandler:
            self.absHandler(event.stream.deviceType, event.stream.deviceIndex,
              self.absx[event.stream.deviceIndex], self.absy[event.stream.deviceIndex], self.absz[event.stream.deviceIndex],
              self.absx2[event.stream.deviceIndex], self.absy2[event.stream.deviceIndex], self.absz2[event.stream.deviceIndex],
              self.abshatx[event.stream.deviceIndex], self.abshaty[event.stream.deviceIndex])
          ret = None
    finally:
      self.mutex.release()
    return ret

  def get_rel_movement(self, index):
    """
    Returns the accumulated REL (mouse or other relative device) movements
    since the last call.

    The returned value is a tuple: (X, Y, WHEEL, H-WHEEL, DIAL)
    """
    self.mutex.acquire()
    try:
      ret = (self.relx[index], self.rely[index], self.relv[index],
             self.relh[index], self.reld[index])

      self.relx[index] = 0
      self.rely[index] = 0
      self.relv[index] = 0
      self.relh[index] = 0
      self.reld[index] = 0
    finally:
      self.mutex.release()
    return ret

  def key_state(self, buttonCode):
    """
    Returns the last event value for the given key code.

    Key names can be converted to key codes using codeOf[str].
    If the key is pressed the returned value will be 1 (pressed) or 2 (held).
    If the key is not pressed, the returned value will be 0.
    """
    try:
      return self.buttons[buttonCode]
    except KeyError:
      return 0

  def clear_key(self, buttonCode):
    """
    Clears the  event value for the given key code.

    Key names can be converted to key codes using codeOf[str].
    This emulates a key-up but does not generate any events.
    """
    try:
      self.buttons[buttonCode] = 0
    except KeyError:
      pass

  def get_keys(self):
    """
    Returns the first of whichever keys have been pressed.

    Key names can be converted to key codes using codeOf[str].
    This emulates a key-up but does not generate any events.
    """
    k_list = []
    try:
      for k in self.buttons:
        if self.buttons[k] != 0:
          k_list.append(k)
      return k_list
    except KeyError:
      pass
    return k_list

