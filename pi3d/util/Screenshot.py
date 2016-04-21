from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes
import numpy as np
from PIL import Image

from pi3d.constants import *
from pi3d.util import Log

def screenshot(filestring=None):
  """
  Save whatever's in the display to a file.

  Will save whatever has been rendered since the last call to Display.clear().

  The file will be saved in the top-level directory if you don't add a path
  to it!
  """

  from pi3d.Display import Display

  w, h = Display.INSTANCE.width, Display.INSTANCE.height
  img = np.zeros((h, w, 4), dtype=np.uint8)
  opengles.glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, img.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)))
  img = img[::-1,:,:].copy()
  if filestring is None:
    return img

  im = Image.frombuffer('RGBA', (w, h), img, 'raw', 'RGBA', 0, 1)
  im.save(filestring, quality=90)

