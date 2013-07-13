from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.util import Log

LOGGER = Log.logger(__name__)

def screenshot(filestring):
  """
  Save whatever's in the display to a file.

  Will save whatever has been rendered since the last call to Display.clear().

  The file will be saved in the top-level directory if you don't add a path
  to it!
  """

  from pi3d.Display import Display
  LOGGER.info('Taking screenshot of "%s"', filestring)

  w, h = Display.INSTANCE.width, Display.INSTANCE.height
  size = h * w * 3
  img = (ctypes.c_char * size)()
  opengles.glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))

  im = Image.frombuffer('RGB', (w, h), img, 'raw', 'RGB', 0, 1)
  im = im.transpose(Image.FLIP_TOP_BOTTOM)
  im.save(filestring)

