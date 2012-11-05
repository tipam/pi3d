from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

SUFFIX = '.py'

def is_demo(f):
  return f[0].isupper() and f.endswith(SUFFIX)

if __name__ == '__main__':
  home = os.getcwd()
  demodir = os.path.join(home, 'demos')
  if not os.path.isdir(demodir):
    print('Demo.py must be called from the root directory of pi3d')
    exit(-1)

  demofiles = [f for f in os.listdir(demodir) if is_demo(f)]
  if not demofiles:
    print('There are no files in the demo directory')
    exit(-1)

  demos = sorted([f[:-len(SUFFIX)] for f in demofiles])

  if len(sys.argv) is 1:
    print('Usage: %s [%s]' % (sys.argv[0], ' | '.join(demos)))

