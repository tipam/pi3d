from collections import namedtuple

from pi3d.util import Log

RAISE_EXCEPTION_ON_ERROR = True
LOGGER = Log.logger(__name__)

def _error(args, exception=None):
  LOGGER.error(*args)
  if RAISE_EXCEPTION_ON_ERROR:
    raise exception or Exception()

class Materials(object):
  NEW_MATERIAL_CHUNK = 'newmtl'

  float3_f = lambda x, y, z: [float(x), float(y), float(z)]
  float_f = lambda x: float(x)
  int_f = lambda x: int(x)
  str_f = lambda x: str(x)

  Prop = namedtuple('Prop', ['name', 'func'])
  PROPERTIES = {
    'Ka': Prop('colorAmbient', float3_f),
    'Kd': Prop('colorDiffuse', float3_f),
    'Ks': Prop('colorSpecular', float3_f),
    'Ke': Prop('colorEmissive', float3_f),
    'Ni': Prop('opticalDensity', float_f),
    'Ns': Prop('specularCoef', float_f),
    'Tr': Prop('transparency', float_f),
    'Tf': Prop('colorTransparency', float3_f),
    'bump': Prop('mapBump', str_f),
    'd': Prop('transparency', float_f),
    'illum': Prop('illumination', int_f),
    'map_Ka': Prop('mapAmbient', str_f),
    'map_Kd': Prop('mapDiffuse', str_f),
    'map_Ks': Prop('mapSpecular', str_f),
    'map_Bump': Prop('mapBump', str_f),
    'map_d': Prop('mapAlpha', str_f),
    }

  def __init__(self):
    self.identifier = None
    self.materials = {}
    self.material = {}

  def parse_lines(self, lines):
    for line in lines:
      self.parse_line(line)
    return self.materials

  def parse_line(self, line):
    line = line.strip()
    if not line.startswith('#'):
      chunks = line.strip().split()
      if chunks:
        name = chunks[0]
        args = chunks[1:]
        if name == Materials.NEW_MATERIAL_CHUNK:
          self.set_identifier(args, line)
        else:
          self.set_property(name, args)

  def set_identifier(self, args, line):
    if not args:
      self.identifier = ''
    else:
      self.identifier = args[0].strip()
      if len(args) > 1:
        LOGGER.warning('too many arguments in identifier line "%s"', line)
    self.material = self.materials.get(self.identifier, {})
    self.materials[self.identifier] = self.material

  def set_property(self, name, args):
    prop = Materials.PROPERTIES.get(name, None)
    if not prop:
      LOGGER.error('ERROR: Don\'t understand property "%s"', name)
      if RAISE_EXCEPTION_ON_ERROR:
        raise Exception()
    else:
      if prop.name in self.material:
        LOGGER.warning('duplicate property %s in %s', prop.name, name)
      try:
        self.material[prop.name] = prop.func(*args)
      except:
        LOGGER.error('Couldn\'t set %s with args "%s"', name, args)
        if RAISE_EXCEPTION_ON_ERROR:
          raise

def parse_mtl(lines):
  """Parse MTL file.
  """
  return Materials().parse_lines(lines)
