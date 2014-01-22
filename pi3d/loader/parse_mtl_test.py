import unittest

from pi3d.loader.parse_mtl import parse_mtl

class ParseMtlTest(unittest.TestCase):
  def setUp(self):
    pass

  def test_cow(self):
    self.assertEqual(COW_RESULT, parse_mtl(COW_MTL.splitlines()))

  def test_teapot(self):
    self.assertEqual(TEAPOT_RESULT, parse_mtl(TEAPOT_MTL.splitlines()))

if __name__ == '__main__':
    unittest.main()

COW_MTL = """
# Blender3D MTL File: LD_COW_CC0_2012.blend
# Material Count: 1
newmtl Material_rock1.jpg
Ns 96.078431
Ka 0.000000 0.000000 0.000000
Kd 0.471461 0.471461 0.471461
Ks 0.500000 0.500000 0.500000
Ni 1.000000
d 1.000000
illum 2
map_Kd ../textures/rock1.jpg
"""

COW_RESULT = {
  'Material_rock1.jpg': {
    'colorAmbient': [0.0, 0.0, 0.0],
    'colorDiffuse': [0.471461, 0.471461, 0.471461],
    'colorSpecular': [0.5, 0.5, 0.5],
    'illumination': 2,
    'mapDiffuse': '../textures/rock1.jpg',
    'opticalDensity': 1.0,
    'specularCoef': 96.078431,
    'transparency': 1.0,
    }
    }

TEAPOT_MTL = """
# Blender MTL File: 'None'
# Material Count: 1
newmtl
Ns 0
Ka 0.000000 0.000000 0.000000
Kd 0.8 0.8 0.8
Ks 0.8 0.8 0.8
d 1
illum 2
map_Kd ../textures/Raspi256x256.png
"""

TEAPOT_RESULT = {
  '': {
    'colorAmbient': [0.0, 0.0, 0.0],
    'colorDiffuse': [0.8, 0.8, 0.8],
    'colorSpecular': [0.8, 0.8, 0.8],
    'illumination': 2,
    'mapDiffuse': '../textures/Raspi256x256.png',
    'specularCoef': 0.0,
    'transparency': 1.0,
    }}
