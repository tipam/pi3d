#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

import experiment

import pi3d
import sys
import time

from six.moves import xrange

DEFAULT_SLEEP = 0.0
DEFAULT_ITERATIONS = 5000

SLEEP = DEFAULT_SLEEP if len(sys.argv) < 2 else float(sys.argv[1])
ITERATIONS = DEFAULT_ITERATIONS if len(sys.argv) < 3 else float(sys.argv[2])

for i in xrange(ITERATIONS):
  d = pi3d.Display.create()
  d.destroy()
  print(i)
  if SLEEP > 0:
    time.sleep(SLEEP)
