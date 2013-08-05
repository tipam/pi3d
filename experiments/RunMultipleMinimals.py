#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess, time

from six.moves import xrange

for i in xrange(500):
  p = subprocess.Popen(["python", "/home/pi/pi3d/demos/Minimal.py"],
          stdin=subprocess.PIPE, stderr=subprocess.PIPE)
  time.sleep(7.0)
  stdoutdata, stderrdata = p.communicate(chr(27))
  with open("/home/pi/pi3d/experiments/minimal_count.txt", "w") as myfile:
    myfile.write(str(i))


