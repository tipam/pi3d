import array
import fcntl
from threading import Lock
import os
import re
import select
import struct
import sys

from event_consts import *
import ioctl

EVIOCGRAB = ioctl._IOW(ord("E"), 0x90, "i")          # Grab/Release device

def EVIOCGABS(axis):
  return	ioctl._IOR(ord('E'), 0x40 + axis, "ffffff")	# get abs value/limits

EventFormat = "llHHi"
EventSize = struct.calcsize(EventFormat)

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
	def __init__(self, stream, time=None, eventType=None, eventCode=None, eventValue=None):
		"""
		create a new event

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
		standard __str__ function

		Uses the stream to give the device type and whether it is currently grabbed.
		"""
		return "Input event %s[%d], %d -- %f: 0x%x(0x%x) = 0x%x" % (self.stream.deviceType, self.stream.deviceIndex, self.stream.grabbed, self.time, self.eventType, self.eventCode, self.eventValue)

	def __repr__(self):
		"""
		standard __repr__ function
		"""
		return "EventStruct(%s, %f, 0x%x, 0x%x, 0x%x)" % (repr(self.stream), self.time, self.eventType, self.eventCode, self.eventValue)

	def encode(self):
		"""
		encode this event into a Linux input event structure

		The output is packed into a string. It is unlikely that this function
		will be required, but it might as well be here.
		"""
		tint = long(self.time)
		tfrac = long((self.time - tint)*1000000)
		return struct.pack(EventFormat, tsec, tfrac,  self.eventType, self.eventCode, self.eventValue)

	def decode(self,s):
		"""
		decode a Linux input event into the fields of this object

		The input parameter is a binary structure packed into a string.
		"""
		tsec, tfrac,  self.eventType, self.eventCode, self.eventValue = struct.unpack(EventFormat,s)
		self.time = tsec + tfrac / 1000000.0


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

		self.mutex = Lock()

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
					ret= None
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
							self.relHandler(event.stream.deviceType, event.stream.deviceIndex, event.eventValue, 0,0,0)
						ret = None
					elif event.eventCode == REL_Y:
						self.rely[event.stream.deviceIndex] += event.eventValue
						if self.relHandler:
							self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0, event.eventValue, 0,0)
						ret = None
					elif event.eventCode == REL_WHEEL:
						self.relv[event.stream.deviceIndex] += event.eventValue
						if self.relHandler:
							self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0,0, event.eventValue, 0)
						ret = None
					elif event.eventCode == REL_HWHEEL:
						self.relh[event.stream.deviceIndex] += event.eventValue
						if self.relHandler:
							self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0,0,0, event.eventValue)
					elif event.eventCode == REL_DIAL:
						self.relh[event.stream.deviceIndex] += event.eventValue
						if self.relHandler:
							self.relHandler(event.stream.deviceType, event.stream.deviceIndex, 0,0,0, event.eventValue)
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
			ret = (self.relx[index], self.rely[index],
				self.relv[index], self.relh[index],
				self.reld[index])

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
			self.buttons[buttonCode]=0
		except KeyError:
			pass


class get_abs_info(object):
	"""
	fetches and implements the EV_ABS axis scaling

	The constructor fetches the scaling values from the given stream for the
	given axis using an ioctl.

	There is a scale method, which scales a given value to the range -1..+1.
	"""
	def __init__(self,stream, axis):
		"""
		Fetch the scale values for this stream and fill in the instance
		variables accordingly.
		"""
		s = array.array("f",[1,2,3,4,5,6])
 		try:
 			x = fcntl.ioctl(stream.filehandle, EVIOCGABS(axis), s)
 		except IOError:
 			self.value = 1
 			self.minimum = 1
 			self.maximum = 1
 			self.fuzz = 1
 			self.flat = 1
 			self.resolution = 1
 		else:
 			self.value, self.minimum, self.maximum, self.fuzz, self.flat, self.resolution = struct.unpack("llllll", s)

 	def __str__(self):
 		return "Value {0} Min {1}, Max {2}, Fuzz {3}, Flat {4}, Res {5}".format(self.value, self.minimum, self.maximum, self.fuzz, self.flat, self.resolution)

	def scale(self, value):
		"""
		scales the given value into the range -1..+1
		"""
		return (float(value)-float(self.minimum))/float(self.maximum-self.minimum)*2.0 - 1.0

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
	axisX = 0; 	axisY = 1; 	axisZ = 2
	axisRX = 3;	axisRY = 4; axisRZ = 5
	axisHat0X = 6;	axisHat0Y = 7
	axisHat1X = 8;	axisHat1Y = 9
	axisHat2X = 10;	axisHat2Y = 11
	axisHat3X = 12;	axisHat3Y = 13
	axisThrottle = 14; axisRudder = 15
	axisWheel=16; axisGas = 17;	axisBrake=18
	axisPressure = 19;	axisDistance = 20
	axisTiltX = 21; axisTiltY = 22; axisToolWidth = 23
	numAxes = 24

	axisToEvent = [ABS_X, ABS_Y, ABS_Z,	ABS_RX, ABS_RY,	ABS_RZ,
		ABS_HAT0X, ABS_HAT0Y, ABS_HAT1X, ABS_HAT1Y,
		ABS_HAT2X, ABS_HAT2Y, ABS_HAT3X, ABS_HAT3Y,
		ABS_THROTTLE, ABS_RUDDER, ABS_WHEEL, ABS_GAS, ABS_BRAKE,
		ABS_PRESSURE, ABS_DISTANCE, ABS_TILT_X, ABS_TILT_Y, ABS_TOOL_WIDTH]

	def __init__(self, index, deviceType):
		"""
		opens the given /dev/input/event file and grabs it.

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
		self.absInfo = [None]*EventStream.numAxes

	#def acquire_abs_info(self, axis):
	#	assert (axis < EventStream.numAxes), "Axis number out of range"
	#	self.absinfo[axis] = get_abs_info(EventStream.axisToEvent[axis])
	def acquire_abs_info(self):
		"""
		Acquires the axis limits for all the ABS axes.

		This will only be called for joystick-type devices.
		"""
		for axis in range(EventStream.numAxes):
			self.absInfo[axis] = get_abs_info(self, EventStream.axisToEvent[axis])

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
			s = os.read(self.filehandle,EventSize)
			if s:
				event = EventStruct(self)
				event.decode(s)
				return event

		return None

	@classmethod
	def grab_by_type(self, deviceType, deviceIndex=None, grab=True, streams=None):
		"""
		Grabs all streams of the given type.
		"""
		if streams == None:
			streams = EventStream.AllStreams

		reqdStreams = filter(lambda x: x.deviceType == deviceType and (deviceIndex == None or x.deviceIndex == deviceIndex), streams)
		map(lambda x: x.grab(grab), reqdStreams)

	@classmethod
	def allNext(self, streams=None):
		"""
		A generator fuction returning all waiting events in the given streams

		If the streams parameter is not given, then all streams are selected.
		"""
		#print EventStream.AllStreams
		#print map(lambda(x):x.filehandle, EventStream.AllStreams)
		if streams == None:
			streams = EventStream.AllStreams

		selectlist = map(lambda(x):x.filehandle, streams)

		ready = select.select(selectlist,[ ], [ ], 0)[0]
		if not ready: return
		while ready:
			for fd in ready:
				stream = filter(lambda x: x.filehandle == fd, streams)[0]
				s = os.read(fd,EventSize)
				if s:
					event = EventStruct(stream)
					event.decode(s)
					yield event
			ready = select.select(selectlist,[ ], [ ], 0)[0]

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
	listed in event_consts.py or /usr/include/linux/input.h Note that the key
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

		self.handler = EventHandler(keyboardHandler, mouseHandler, joystickHandler, synHandler)

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


