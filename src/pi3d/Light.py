from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.util.DefaultInstance import DefaultInstance

class Light(DefaultInstance):
  """ Holds information about lighting to be used in shaders """
  def __init__(self,
               lightpos=(10, -10, -5),
               lightcol=(1.0, 1.0, 1.0),
               lightamb=(0.1, 0.1, 0.2), is_point=False):
    """ set light values. These are set in Shape.unif as part of the Shape
    constructor. They can be changed using Shape.set_light()
    The pixel shade is calculated as::

      (lightcol * texture) * dot(lightpos, -normal) + (lightamb * texture)

    where * means component multiplying if between two vectors and dot() is
    the dot product of two vectors.

    Arguments:
      *lightpos*
        tuple (x,y,z) vector direction *from* the light i.e. an object at position
        (0,0,0) would appear to be lit from a light at (-3,4,-5) (left, above and
        nearer) if lightpos=(3,-4,5). *ALTERNATIVELY* if is_point is set
        to True then this is the actual position of the light
      *lightcol*
        tuple (r,g,b) defines shade and brightness 0.0 to 1.0 but see below
        for point lights
      *lightamb*
        tuple (r,g,b) ambient lighting values
      *is_point*
        the light behaves as a point and brightness falls off with distance.
        This means that the r,g,b values of lightcol usually have to be set
        higher than 1.0, objects close to the light will 'white out' 
    """
    super(Light, self).__init__()
    self.lightpos = lightpos
    self.lightcol = lightcol
    self.lightamb = lightamb
    self.is_point = 1.0 if is_point else 0.0

  def position(self, lightpos):
    self.lightpos = lightpos

  def color(self, lightcol):
    self.lightcol = lightcol

  def ambient(self, lightamb):
    self.lightamb = lightamb

  def make_point(self):
    self.is_point = 1.0

  def make_directional(self):
    self.is_point = 0.0

  @staticmethod
  def _default_instance():
    return Light()

