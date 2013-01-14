import sys
from os.path import dirname

def demo(name):
  if name == '__main__':
    sys.path.append(dirname(dirname(__file__)))


