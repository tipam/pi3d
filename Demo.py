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
    print('%s must be called from the root directory of pi3d' % sys.argv[0])
    exit(-1)

  demofiles = [f for f in os.listdir(demodir) if is_demo(f)]
  if not demofiles:
    print('There are no files in the demo directory')
    exit(-1)

  demos = sorted([f[:-len(SUFFIX)] for f in demofiles])
  def usage():
    print('Usage: %s [%s]' % (sys.argv[0], ' | '.join(demos)))
    print()
    print('(Any prefix of a demo will also work)')

  if len(sys.argv) is 1:
    usage()

  elif len(sys.argv) is 2:
    demo = sys.argv[1]
    for d in demos:
      if d.startswith(demo):
        __import__('demos.' + d)
        exit(0)  # None of the demos exit so we'll never get here.

    print("Didn't understand command %s" % demo)
    usage()
    exit(-1)

  else:
    print('Too many arguments to %s' % sys.argv[0])
