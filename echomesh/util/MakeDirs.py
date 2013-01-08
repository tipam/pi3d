from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path

def _makedirs(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
      pass
    else:
      raise

def makedirs(path):
  _makedirs(os.path.expanduser(path))

def parent_makedirs(file):
  _makedirs(os.path.dirname(os.path.expanduser(path)))

