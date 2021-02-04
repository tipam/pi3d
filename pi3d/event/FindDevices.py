import re
from .Constants import *

def test_bit(nlst, b):
  index = b // 32
  bit = b % 32
  if len(nlst) <= index:
    return False
  if nlst[index] & (1 << bit):
    return True
  else:
    return False


def EvToStr(events):
  s = [ ]
  if test_bit(events, EV_SYN):       s.append("EV_SYN")
  if test_bit(events, EV_KEY):       s.append("EV_KEY")
  if test_bit(events, EV_REL):       s.append("EV_REL")
  if test_bit(events, EV_ABS):       s.append("EV_ABS")
  if test_bit(events, EV_MSC):       s.append("EV_MSC")
  if test_bit(events, EV_LED):       s.append("EV_LED")
  if test_bit(events, EV_SND):       s.append("EV_SND")
  if test_bit(events, EV_REP):       s.append("EV_REP")
  if test_bit(events, EV_FF):        s.append("EV_FF" )
  if test_bit(events, EV_PWR):       s.append("EV_PWR")
  if test_bit(events, EV_FF_STATUS): s.append("EV_FF_STATUS")
    
  return s

class DeviceCapabilities(object):
  def __init__(self, firstLine, filehandle):
    self.EV_SYNevents = [ ]
    self.EV_KEYevents = [ ]
    self.EV_RELevents = [ ]
    self.EV_ABSevents = [ ]
    self.EV_MSCevents = [ ]
    self.EV_LEDevents = [ ]
    self.EV_SNDevents = [ ]
    self.EV_REPevents = [ ]
    self.EV_FFevents = [ ]
    self.EV_PWRevents = [ ]
    self.EV_FF_STATUSevents = [ ]
    self.eventTypes = [ ]
    
    match = re.search(".*Bus=([0-9A-Fa-f]+).*Vendor=([0-9A-Fa-f]+).*Product=([0-9A-Fa-f]+).*Version=([0-9A-Fa-f]+).*", firstLine)
    if not match:
      print("Do not understand device ID:", line)
      self.bus = 0
      self.vendor = 0
      self.product = 0
      self.version = 0
    else:
      self.bus = int(match.group(1), base=16)
      self.vendor = int(match.group(2), base=16)
      self.product = int(match.group(3), base=16)
      self.version = int(match.group(4), base=16)
    for line in filehandle:
      if len(line.strip()) == 0:
        break
      if line[0] == "N":
        match = re.search('Name="([^"]+)"', line)
        if match:
          self.name = match.group(1)
        else:
          self.name = "UNKNOWN"
      elif line[0] == "P":
        match = re.search('Phys=(.+)', line)
        if match:
          self.phys = match.group(1)
        else:
          self.phys = "UNKNOWN"
      elif line[0] == "S":
          match = re.search('Sysfs=(.+)', line)
          if match:
              self.sysfs = match.group(1)
          else:
              self.sysfs = "UNKNOWN"
      elif line[0] == "U":
        match = re.search('Uniq=(.*)', line)
        if match:
          self.uniq = match.group(1)
        else:
          self.uniq = "UNKNOWN"
      elif line[0] == "H":
        match = re.search('Handlers=(.+)', line)
        if match:
          self.handlers = match.group(1).split()
        else:
          self.handlers = [ ]
      elif line[:5] == "B: EV":
        eventsNums = [int(x,base=16) for x in line [6:].split()]
        eventsNums.reverse()
        self.eventTypes = eventsNums
      elif line[:6] == "B: KEY":
        eventsNums = [int(x,base=16) for x in line [7:].split()]
        eventsNums.reverse()
        self.EV_KEYevents = eventsNums
      elif line[:6] == "B: ABS":
        eventsNums = [int(x,base=16) for x in line [7:].split()]
        eventsNums.reverse()
        self.EV_ABSevents = eventsNums
      elif line[:6] == "B: MSC":
        eventsNums = [int(x,base=16) for x in line [7:].split()]
        eventsNums.reverse()
        self.EV_MSCevents = eventsNums
      elif line[:6] == "B: REL":
        eventsNums = [int(x,base=16) for x in line [7:].split()]
        eventsNums.reverse()
        self.EV_RELevents = eventsNums
      elif line[:6] == "B: LED":
        eventsNums = [int(x,base=16) for x in line [7:].split()]
        eventsNums.reverse()
        self.EV_LEDevents = eventsNums

    for handler in self.handlers:
      if handler[:5] == "event":
        self.eventIndex = int(handler[5:])

    self.isMouse = False
    self.isKeyboard = False
    self.isJoystick = False

  def doesProduce(self, eventType, eventCode):
    if not test_bit(self.eventTypes, eventType):
      return False
    if eventType == EV_SYN and test_bit(self.EV_SYNevents, eventCode): return True
    if eventType == EV_KEY and test_bit(self.EV_KEYevents, eventCode): return True
    if eventType == EV_REL and test_bit(self.EV_RELevents, eventCode): return True
    if eventType == EV_ABS and test_bit(self.EV_ABSevents, eventCode): return True
    if eventType == EV_MSC and test_bit(self.EV_MSCevents, eventCode): return True
    if eventType == EV_LED and test_bit(self.EV_LEDevents, eventCode): return True
    if eventType == EV_SND and test_bit(self.EV_SNDevents, eventCode): return True
    if eventType == EV_REP and test_bit(self.EV_REPevents, eventCode): return True
    if eventType == EV_FF  and test_bit(self.EV_FFevents, eventCode): return True
    if eventType == EV_PWR and test_bit(self.EV_PWRevents, eventCode): return True
    if eventType == EV_FF_STATUS and test_bit(self.EV_FF_STATUSevents, eventCode): return True
    return False
      
  def __str__(self):
    return self.name+"\nBus: "+str(self.bus)+" Vendor: "+str(self.vendor)+ \
        " Product: "+str(self.product)+" Version: "+str(self.version) + \
        "\nPhys: " + self.phys + "\nSysfs: " + self.sysfs + "\nUniq: " + self.uniq + \
        "\nHandlers: " + str(self.handlers) + " Event Index: "+ str(self.eventIndex) + \
        "\nKeyboard: " + str(self.isKeyboard) + " Mouse: " + str(self.isMouse) + \
        " Joystick: " + str(self.isJoystick) + \
        "\nEvents: " + str(EvToStr(self.eventTypes))
                
        
deviceCapabilities = [ ]

def get_devices(filename="/proc/bus/input/devices"):
  global deviceCapabilities
  with open("/proc/bus/input/devices", "r") as filehandle:
    for line in filehandle:
      if line[0] == "I":
        deviceCapabilities.append(DeviceCapabilities(line, filehandle))
              
  return deviceCapabilities
        
def find_devices(identifier, butNot= [ ]):
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
  # print "Looking for", identifier
  with open("/proc/bus/input/devices", "r") as filehandle:
    for line in filehandle:
      if line[0] == "H":
        if identifier in line:
          # print line
          match = re.search("event([0-9]+)", line)
          eventindex = match and match.group(1)
          if eventindex:
            for old in butNot:
              if old[1] == int(eventindex):
                # print "Removing", old[1]
                break
              else:
                pass
                # print "No need to remove", old[1]
            else: # i.e. there was no break from above for loop (horrible for-else syntax!)
              ret.append((index, int(eventindex)))
              index += 1

  return ret

if __name__ == "__main__":
  devs = get_devices()
  for dev in devs:
    print(str(dev))
    print("   ABS: {}".format([x for x in range(64) if test_bit(dev.EV_ABSevents, x)]))
    print("   REL: {}".format([x for x in range(64) if test_bit(dev.EV_RELevents, x)]))
    print("   MSC: {}".format([x for x in range(64) if test_bit(dev.EV_MSCevents, x)]))
    print("   KEY: {}".format([x for x in range(512) if test_bit(dev.EV_KEYevents, x)]))
    print("   LED: {}".format([x for x in range(64) if test_bit(dev.EV_LEDevents, x)]))
    print()
