class Light(object):
  def __init__(self,lightpos=(100,100,-100),lightcol=(1.0,1.0,1.0),lightamb=(0.2,0.2,0.2)):
    self.lightpos = lightpos
    self.lightcol = lightcol
    self.lightamb = lightamb

  def position(self, lightpos):
    self.lightpos = lightpos

  def color(self, lightcol):
    self.lightcol = lightcol

  def ambient(self, lightamb):
    self.lightamb = lightamb
