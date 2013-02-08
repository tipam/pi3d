import re

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
  with open("/proc/bus/input/devices","r") as filehandle:
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
            else:
              ret.append((index, int(eventindex)))
              index += 1

  return ret

