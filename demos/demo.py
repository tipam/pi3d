import os
import sys

from os.path import dirname

def demo(name):
  if name == '__main__':
    root = dirname(dirname(__file__))
    sys.path.append(root)
    os.chdir(root)



