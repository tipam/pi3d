import unittest

from pi3d.loader.parse_mtl_test import ParseMtlTest

def test_suite():
  suite = unittest.TestLoader().loadTestsFromTestCase(ParseMtlTest)
  return suite

if __name__ == '__main__':
  unittest.TextTestRunner().run(test_suite())
