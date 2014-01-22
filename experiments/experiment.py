import os
import sys

from os.path import dirname

root = dirname(dirname(__file__))
sys.path.append(root)
os.chdir(root)
