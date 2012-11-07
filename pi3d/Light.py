import ctypes

from pi3d import *
from pi3d import Utility

class Light(object):
  def __init__(self, no=0, red=1.0, grn=1.0, blu=1.0, name="",
               x=0, y=0, z=0, ambR=0.5, ambG=0.5, ambB=0.5):

    if VERBOSE:
      print "Creating light ..."

    self.ambient = c_floats((ambR, ambG, ambB, 1.0))
    self.diffuse = c_floats((red, grn, blu, 1.0))
    self.specular = c_floats((red, grn, blu, 1.0))
    self.xyz = c_floats((x, y, z, 1))
    self.no = ctypes.c_int(GL_LIGHT0 + no)
    self.name = name
    self.lighton = False

    #opengles.glLightModelfv(GL_LIGHT_MODEL_COLOUR_CONTROL, GL_SEPERATE_SPECULAR_COLOR)   #Turns on specular highlights for textures
    #opengles.glMaterialfv(GL_FRONT, GL_SHININESS, self.mShininess)#TIM: don't think this works but would like it to
    opengles.glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient)
    opengles.glLightfv(self.no, GL_AMBIENT, self.ambient)
    opengles.glLightfv(self.no, GL_DIFFUSE, self.diffuse)
    opengles.glLightfv(self.no, GL_SPECULAR, self.specular)
    opengles.glLightfv(self.no, GL_POSITION, self.xyz)
    # 0 for a distant light and -1 for a spot. LIGHT0 comes predefined as a distant light but that's changed here
    # I would have thought either w needs to be passed as a parameter to __init__ and not overwritten in position
    # and/or define global values SPOT, DIST, POINT = -1, 0, 1

  def position(self, x, y, z):
    mtrx = (ctypes.c_float * 16)()
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
    Utility.load_identity()
    self.xyz = c_floats((x, y, z ,1))
    opengles.glLightfv(self.no, GL_POSITION, self.xyz)
    opengles.glLoadMatrixf(mtrx)

  def on(self):
    #load view matrix
    opengles.glEnable(GL_LIGHTING)
    opengles.glEnable(self.no)
    opengles.glLightfv(self.no, GL_POSITION, self.xyz) #TIM: fv
    self.lighton = True

  def off(self):
    opengles.glDisable(self.no)
    opengles.glDisable(GL_LIGHTING)
    self.lighton = False
