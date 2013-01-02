import ctypes

from pi3d import *

# By paddywwoof 12-12-2012

class Fog():
  def __init__(self, density=0.005, color=(0.3, 0.6, 0.8, 0.5)):
    opengles.glFogf(GL_FOG_MODE, GL_EXP) # defaults to this anyway
    opengles.glFogf(GL_FOG_DENSITY, ctypes.c_float(density)) # exponent factor
    opengles.glFogfv(GL_FOG_COLOR, c_floats(color))
    # don't think the alpha value alters the target object alpha

  def on(self):
    opengles.glEnable(GL_FOG)

  def off(self):
    opengles.glDisable(GL_FOG)

