from __future__ import absolute_import, division, print_function, unicode_literals

import Image

from pi3d import *
from pi3d.util import Log

LOGGER = Log.logger(__name__)

def screenshot(filestring):
  from pi3d.Display import DISPLAY
  LOGGER.info('Taking screenshot of "%s"', filestring)

  w, h = DISPLAY.width, DISPLAY.height
  size = h * w * 3
  img = (c_char * size)()
  opengles.glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(img))

  im = Image.frombuffer('RGB', (w, h), img, 'raw', 'RGB', 0, 1)
  im = im.transpose(Image.FLIP_TOP_BOTTOM)
  im.save(filestring)

