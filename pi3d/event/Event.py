import six_mod
import logging

from pi3d.event import EventHandler
from pi3d.event import Keys
from pi3d.event.FindDevices import find_devices
from pi3d.event.Constants import *
from pi3d.event.EventStream import EventStream

LOGGER = logging.getLogger(__name__)
_KEYS = (k for k in vars(Keys) if not k.startswith('_'))
KEY_CODE = dict((k, getattr(Keys, k)) for k in _KEYS)
CODE_KEY = {}
for v in KEY_CODE:
  CODE_KEY[KEY_CODE[v]] = v

def key_to_code(key):
  return KEY_CODE.get(str(key), -1) if isinstance(key, six_mod.string_types) else key

def code_to_key(code):
  return CODE_KEY.get(code, '')

class InputEvents(object):
  """Encapsulates the entire InputEvents subsystem.

  This is generally all you need to import. For efficiency reasons you may
  want to make use of CodeOf[ ], but everything else is hidden behind this class.

  On instantiation, we open all devices that are keyboards, mice or joysticks.
  That means we might have two of one sort of another, and that might be a problem,
  but it would be rather rare.

  There are several ABS (joystick, touch) events that we do not handle, specifically
  THROTTLE, RUDDER, WHEEL, GAS, BRAKE, HAT1, HAT2, HAT3, PRESSURE,
  DISTANCE, TILT, TOOL_WIDTH. Implementing these is left as an exercise
  for the interested reader. Similarly, we make no attempt to handle multi-touch.

  Handlers can be supplied, in which case they are called for each event, but
  it isn't necessary; API exists for all the events.

  The handler signatures are:

    def mouse_handler_func(sourceType, SourceIndex, x, y, v, h)
    def joystick_handler_func(sourceType, SourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty)
    def key_handler_func(sourceType, SourceIndex, key, value)
    def syn_handler_func(sourceType, SourceIndex, code, value)
    def unhandled_handler_func(event)

  where:
    sourceType:
      the device type string (keyboard, mouse, joystick),

    sourceIndex:
      an incrementing number for each device of that type, starting at zero,
      and event is an EventStruct object.

    key:
      the key code, not its ASCII value or anything simple.

  Use key_to_code() to convert from the name of a key to its code,
  and code_to_key() to convert a code to a name.

  The keys are listed in pi3d.event.Constants.py or /usr/include/linux/input.h
  Note that the key names refer to a US keyboard.
  """
  def __init__(self, keyboardHandler=None, mouseHandler=None, joystickHandler=None, synHandler=None, unhandledHandler=None, wantKeyboard=True, wantMouse=True, wantJoystick=True):
    self.unhandledHandler = unhandledHandler
    self.streams = [ ]
    if wantKeyboard:
      keyboards =  find_devices("kbd")
      for x in keyboards:
        self.streams.append(EventStream(x, "keyboard"))
    else:
      keyboards = [ ]
    LOGGER.debug("keyboards = %s", keyboards)
    if wantMouse:
      mice = find_devices("mouse", butNot=keyboards)
      for x in mice:
        self.streams.append(EventStream(x, "mouse"))
      LOGGER.debug("mice = %s", mice)
    else:
      mice = [ ]
    if wantJoystick:
      joysticks = find_devices("js", butNot=keyboards+mice)
      for x in joysticks:
        self.streams.append(EventStream(x, "joystick"))
      LOGGER.debug("joysticks = %s", joysticks)
    for x in self.streams:
      x.acquire_abs_info()

    self.handler = EventHandler.EventHandler(
                  keyboardHandler, mouseHandler, joystickHandler, synHandler)

  def do_input_events(self):
    """
    Handle all events that have been triggered since the last call.
    """
    for event in EventStream.allNext(self.streams):
      if event.eventType == None:
        self.streams.remove(event.stream)
        event.stream.release()
        continue
      if self.handler.event(event) and self.unhandledHandler:
        self.unhandledHandler(event)

  def key_state(self, key):
    """
    Returns the state of the given key.

    The returned value will be 0 for key-up, or 1 for key-down. This method
    returns a key-held(2) as 1 to aid in using the returned value as a
    movement distance.

    This function accepts either the key code or the string name of the key.
    It would be more efficient to look-up and store the code of
    the key with KEY_CODE[ ], rather than using the string every time. (Which
    involves a dict look-up keyed with a string for every key_state call, every
    time around the loop.)

    Gamepad keys are:
    Select = BTN_BASE3, Start = BTN_BASE4
    L1 = BTN_TOP       R1 = BTN_BASE
    L2 = BTN_PINKIE    R2 = BTN_BASE2
    The action buttons are:
            BTN_THUMB
    BTN_TRIGGER     BTN_TOP
            BTN_THUMB2
    Analogue Left Button = BTN_BASE5
    Analogue Right Button = BTN_BASE6

    Some of those may clash with extended mouse buttons, so if you are using
    both at once, you'll see some overlap.

    The direction pad is hat0 (see get_hat)
    """
    return self.handler.key_state(key_to_code(key))

  def clear_key(self, key):
    """
    Clears the state of the given key.

    Emulates a key-up, but does not call any handlers.
    """
    return self.handler.clear_key(key_to_code(key))

  def get_keys(self):
    return [code_to_key(k) for k in self.handler.get_keys()]

  def get_joystick(self, index=0):
    """
    Returns the x,y coordinates for a joystick or left gamepad analogue stick.

    index is the device index and defaults to 0 -- the first joystick device

    The values are returned as a tuple. All values are -1.0 to +1.0 with
    0.0 being centred.
    """
    return (self.handler.absx[index], self.handler.absy[index])

  def get_joystick3d(self, index=0):
    """
    Returns the x,y,z coordinates for a joystick or left gamepad analogue stick

    index is the device index and defaults to 0 -- the first joystick device

    The values are returned as a tuple. All values are -1.0 to +1.0 with
    0.0 being centred.
    """
    return (self.handler.absx[index], self.handler.absy[index], self.handler.absz[index])

  def get_joystickR(self, index=0):
    """
    Returns the x,y coordinates for a right gamepad analogue stick.

    index is the device index and defaults to 0 -- the first joystick device

    The values are returned as a tuple. For some odd reason, the gamepad
    returns values in the Z axes of both joysticks, with y being the first.

    All values are -1.0 to +1.0 with 0.0 being centred.
    """
    #return (self.handler.absz2[index], self.handler.absz[index])
    return (self.handler.absx2[index], self.handler.absz2[index])

  def get_joystickB3d(self, index=0):
    """
    Returns the x,y,z coordinates for a 2nd joystick control

    index is the device index and defaults to 0 -- the first joystick device

    The values are returned as a tuple. All values are -1.0 to +1.0 with
    0.0 being centred.
    """
    return (self.handler.absx2[index], self.handler.absy2[index], self.handler.absz2[index])

  def get_hat(self, index=0):
    """
    Returns the x,y coordinates for a joystick hat or gamepad direction pad

    index is the device index and defaults to 0 -- the first joystick device

    The values are returned as a tuple.  All values are -1.0 to +1.0 with
    0.0 being centred.
    """
    return (self.handler.abshatx[index], self.handler.abshaty[index])

  def get_mouse_movement(self, index=0):
    """
    Returns the accumulated mouse movements since the last call.

    index is the device index and defaults to 0 -- the first mouse device

    The returned value is a tuple: (X, Y, WHEEL, H-WHEEL)
    """
    return self.handler.get_rel_movement(index)

  def grab_by_type(self, deviceType, deviceIndex=None, grab=True):
    """
    Grab (or release) exclusive access to all devices of the given type.

    The devices are grabbed if grab is True and released if grab is False.
    If the deviceIndex is given, only that device is grabbed, otherwise all
    the devices of the same type are grabbed.

    All devices are grabbed to begin with. We might want to ungrab the
    keyboard for example to use it for text entry. While not grabbed, all key-down
    and key-hold events are filtered out, but that only works if the events
    are received and handled while the keyboard is still grabbed, and the loop
    may not have been running. So if we are grabbing a device, we call the
    handling loop first, so there are no outstanding events.

    Note that the filtering means that if you trigger the ungrab from a
    key-down event, the corrosponding key-up will be actioned before the
    subsequent grab, and you wont end up looping continuously. However it
    also means that you will see key-up events for all the text entry. Since
    it only affects a user-supplied key-handler, and key-ups do not usually
    trigger actions anyway, this is not likely to be a problem. If it is,
    you will have to filter them yourself.
    """
    if grab:
      self.do_input_events()
    EventStream.grab_by_type(deviceType, deviceIndex, grab, self.streams)

  def release(self):
    """
    Ungrabs all streams and closes all files.

    Only do this when you're finished with this object. You can't use it again.
    """
    for s in self.streams:
      s.release()

