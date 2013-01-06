from pi3d.util.DefaultInstance import DefaultInstance

class Light(DefaultInstance):
  def __init__(self,
               lightpos=(10, -10, 20),
               lightcol=(1.0, 1.0, 1.0),
               lightamb=(0.2, 0.2, 0.2)):
    super(Light, self).__init__()
    self.lightpos = lightpos
    self.lightcol = lightcol
    self.lightamb = lightamb

  def position(self, lightpos):
    self.lightpos = lightpos

  def color(self, lightcol):
    self.lightcol = lightcol

  def ambient(self, lightamb):
    self.lightamb = lightamb

  @staticmethod
  def _default_instance():
    return Light()

