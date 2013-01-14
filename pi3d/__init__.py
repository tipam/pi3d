from echomesh.util import Log

from pi3d.constants import *

LOGGER = Log.logger(__name__)

def _load_library(name):
  """Try to load a shared library, report an error on failure."""
  try:
    import ctypes
    return ctypes.CDLL('lib%s.so' % name)
  except:
    from echomesh.util import Log
    Log.logger(__name__).error("Couldn't load library %s" % name)

bcm = _load_library('bcm_host')
opengles = _load_library('GLESv2')
openegl = _load_library('EGL')

