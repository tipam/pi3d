import ctypes

from pi3d import *
from pi3d import Utility

class Light(object):
  def __init__(self, no=0, red=1.0, grn=1.0, blu=1.0, name="",
               x=0, y=0, z=0, ambR=0.5, ambG=0.5, ambB=0.5, w=1):
    """ Set up Light object
    
    arguments:
    no -- each Light has to be assigned a unique int (default 0)
    red -- red value of light, can be greater than 1.0 (default 1.0)
    grn -- green (default 1.0)
    blu -- blue (default 1.0)
    name -- optional string
    x -- x component of location for point light, direction component for directional light (default 0)
    y -- y component (default 0)
    z -- z component (default 0)
    ambR -- red ambient lighting level (default 0.5)
    ambG -- green (default 0.5)
    ambB -- blue (default 0.5)
    w -- type of light 0 for directional, 1 for point (default 1)
    """
    if VERBOSE:
      print "Creating light ..."

    self.ambient = c_floats((ambR, ambG, ambB, 1.0))
    self.diffuse = c_floats((red, grn, blu, 1.0))
    self.specular = c_floats((red, grn, blu, 1.0))
    self.xyz = c_floats((x, y, z, w))
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

  def position(self, x, y, z, w=1):
    """ move or rotate the light and change its type
    
    x,y,z -- location or direction components
    w -- type 0 for directional, 1 for point (default 1)
    """
    mtrx = (ctypes.c_float * 16)()
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX, ctypes.byref(mtrx))
    Utility.load_identity()
    self.xyz = c_floats((x, y, z , w))
    opengles.glLightfv(self.no, GL_POSITION, self.xyz)
    opengles.glLoadMatrixf(mtrx)

  def on(self):
    """ Switch light on. Defaults to off in __init__ 
    """
    #load view matrix
    opengles.glEnable(GL_LIGHTING)
    opengles.glEnable(self.no)
    opengles.glLightfv(self.no, GL_POSITION, self.xyz) #TIM: fv
    self.lighton = True

  def off(self):
    """ Switch light off. Default value in _init__ 
    """
    opengles.glDisable(self.no)
    opengles.glDisable(GL_LIGHTING)
    self.lighton = False
