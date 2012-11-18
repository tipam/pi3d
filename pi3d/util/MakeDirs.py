import os
import os.path

# This is code duplicated from
# https://github.com/rec/echomesh/blob/master/python/util/MakeDirs.py

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

