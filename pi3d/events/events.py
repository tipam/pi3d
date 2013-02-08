import os
import re
import struct
import sys
import threading

from pi3d.events import EventHandler
from pi3d.events.EventStream import EventStream
from pi3d.events import Format
from pi3d.events.Constants import *


def _findevent(s):
	"""
	Finds the event index in the given Handlers line.

	This line comes from the /proc/bus/input/devices file.
	"""
	match = re.search("event([0-9]+)", s)
	if match:
		return match.group(1)
	else:
		return None

def _find_devices(identifier, butNot= [ ]):
	"""
	finds the event indecies of all devices that have the given identifier.

	The identifier is a string on the Handlers line of /proc/bus/input/devices.
	Keyboards use "kbd", mice use "mouse" and joysticks (and gamepads) use "js".

	Returns a list of integer indexes N, where /dev/input/eventN is the event
	stream for each device.

	If except is given it holds a list of tuples which the returned values should not match.

	All devices of each type are returned; if you have two mice, they will both
	be used.
	"""
	ret = [ ]
	index = 0
	print "Looking for", identifier
	with open("/proc/bus/input/devices","r") as filehandle:
		for line in filehandle:
			if line[0] == "H":
				if identifier in line:
					print line
					eventindex = _findevent(line)
					if eventindex:
						for old in butNot:
							if old[1] == int(eventindex):
								print "Removing", old[1]
								break
							else:
								print "No need to remove", old[1]
						else:
							ret.append((index, int(eventindex)))
							index += 1

	return ret

class InputEvents(object):
	"""
	Encapsulates the entire InputEvents subsystem.

	This is generally all you need to import. For efficiency reasons you may
	want to make use of CodeOf[ ], but everything else is hidden behind this class.

	On instanciation, we open all devices that are keyboards, mice or joysticks.
	That means we might have two of one sort of another, and that might be a problem,
	but it would be rather rare.

	There are several ABS (joystick, touch) events that we do not handle. In
	particular:	THROTTLE, RUDDER, WHEEL, GAS, BRAKE, HAT1, HAT2, HAT3, PRESSURE,
	DISTANCE, TILT, TOOL_WIDTH. Implementing these is left as an exercise
	for the interested reader. Similarly, we make no attempt to handle multi-touch.

	Handlers can be supplied, in which case they are called for each event, but
	it isn't necessary; API exists for all the events.
	The handler signatures are:
		def mouse_handler_func(sourceType, SourceIndex, x, y, v, h):
		def joystick_handler_func(sourceType, SourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty):
		def key_handler_func(sourceType, SourceIndex, key, value):
		def syn_handler_func(sourceType, SourceIndex, code, value):
		def unhandled_handler_func(event):
	Where "sourceType" is the device type string (keyboard, mouse, joystick),
	sourceIndex is an incrementing number for each device of that type, starting
	at zero, and event is an EventStruct object. Key is the key code, not it's
	ASCII value or anything	simple. Use codeOf[ ] to convert from the name of a
	key to its code, and nameOf[ ] to convert a code to a name. The keys are
	listed in pi3d.events.Constants.py or /usr/include/linux/input.h Note that the key
	names refer to a US keyboard.
	"""
	def __init__(self, keyboardHandler=None, mouseHandler=None, joystickHandler=None, synHandler=None, unhandledHandler=None, wantKeyboard=True, wantMouse=True, wantJoystick=True):
		self.unhandledHandler = unhandledHandler
		self.streams = [ ]
		if wantKeyboard:
			keyboards =  _find_devices("kbd")
			self.streams += map(lambda x: EventStream(x, "keyboard"),keyboards)
		else:
			keyboards = [ ]
		print "keyboards =", keyboards
		if wantMouse:
			mice = _find_devices("mouse", butNot=keyboards)
			print "mice = ", mice
			self.streams += map(lambda x: EventStream(x, "mouse"), mice)
		else:
			mice = [ ]
		if wantJoystick:
			joysticks = _find_devices("js", butNot=keyboards+mice)
			print "joysticks =", joysticks
			js_streams = map(lambda x: EventStream(x, "joystick"), joysticks)
			self.streams += js_streams
		for x in self.streams:
			x.acquire_abs_info()

		self.handler = EventHandler.EventHandler(
                  keyboardHandler, mouseHandler, joystickHandler, synHandler)

	def do_input_events(self):
		"""
		Handle all events that have been triggered since the last call.
		"""
		for event in EventStream.allNext(self.streams):
			if self.handler.event(event) and self.unhandledHandler:
				self.unhandledHandler(event)

	def key_state(self,key):
		"""
		Returns the state of the given key.

		The returned value will be 0 for key-up, or 1 for key-down. This method
		returns a key-held(2) as 1 to aid in using the returned value as a
		movement distance.

		This function accepts either the key code or the string name of the key.
		It would be more efficient to look-up and store the code of
		the key with codeOf[ ], rather than using the string every time. (Which
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
		if isinstance(key, basestring):
			return 1 if self.handler.key_state(codeOf[str(key)]) else 0
		else:
			return 1 if self.handler.key_state(key) else 0

	def clear_key(self,key):
		"""
		Clears the state of the given key.

		Emulates a key-up, but does not call any handlers.
		"""
		if isinstance(key, basestring):
			return self.handler.clear_key(codeOf[str(key)])
		else:
			return self.handler.clear_key(key)

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

	def get_joystickR(self,index=0):
		"""
		Returns the x,y coordinates for a right gamepad analogue stick.

		index is the device index and defaults to 0 -- the first joystick device

		The values are returned as a tuple. For some odd reason, the gamepad
		returns values in the Z axes of both joysticks, with y being the first.

		All values are -1.0 to +1.0 with 0.0 being centred.
		"""
		return (self.handler.absz2[index], self.handler.absz[index])

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

codeOf = dict()
nameOf = dict()
for pair in KEY_PAIRS:
	codeOf[pair[0]] = pair[1]
	nameOf[pair[1]] = pair[0]

if __name__ == "__main__":
	def mouse_handler_func(sourceType, sourceIndex, x, y, v, h):
		print "Relative[%d] (%d, %d), (%d, %d)" %(sourceIndex, x, y, v, h)
		pass

	def joystick_handler_func(sourceType, sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty):
		print "Absolute[%d] (%6.3f, %6.3f, %6.3f), (%6.3f, %6.3f, %6.3f), (%2.0f, %2.0f)" %(sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty)
		pass

	def unhandled_handler_func(event):
		print "Unknown:", event
		pass

	def key_handler_func(sourceType, sourceIndex, key, value):
		print nameOf[key],"[",sourceIndex,"] =",value
		pass

	def syn_handler_func(sourceType, sourceIndex, code, value):
		#print "SYN",code,value
		pass

	inputs = InputEvents( key_handler_func, mouse_handler_func, joystick_handler_func, syn_handler_func, unhandled_handler_func)
	#inputs = InputEvents(key_handler_func)


	while not inputs.key_state("KEY_ESC"):
		inputs.do_input_events()
		if inputs.key_state("KEY_LEFTCTRL"):
			inputs.grab_by_type("keyboard", grab=False)
			print "Name:",
			s = raw_input()
			print "Hello",s
			inputs.grab_by_type("keyboard", True)
		if inputs.key_state("BTN_LEFT"):
			v = inputs.get_mouse_movement()
			if v != (0,0,0,0,0):
					print v
		if inputs.key_state("BTN_RIGHT"):
			v = inputs.get_mouse_movement(1)
			if v != (0,0,0,0,0):
					print v
		if inputs.key_state("BTN_TOP2"):			#gamepad L1
			print inputs.get_joystick()				#gamepad Left Analogue
		if inputs.key_state("BTN_BASE"):			#gamepad R1
			print inputs.get_joystickR()			#gamepad Right Analogue
		if inputs.key_state("BTN_PINKIE"):			#gamepad L2
			v = inputs.get_hat()					#gamepad Direction pad
			if v != (0,0):
					print v
		if inputs.key_state("BTN_BASE2"):			#gamepad R2
			print inputs.get_joystickR(1)			#gamepad Right Analogue (2nd device)


