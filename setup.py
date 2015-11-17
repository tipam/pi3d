#!/usr/bin/env python
""" to create a Distutils distribution package you need to run from
a terminal cd to the pi3d directory with this file in:

  $ python setup.py sdist

this will create the directory 'dist' containing pi3d-1.10.tar.gz this can
then be extracted somewhere and in that directory run (probably sudo):

  $ python setup.py install

which will put all of the pi3d files in /usr/local/lib/python2.7/dist-packages
or equivalent. After that you won't need the line in the demos:

  import demo

which really just does this:

  import sys
  sys.append('/home/pi/pi3d')
"""
try:
    from setuptools.commands import setup
except ImportError:
    from distutils.core import setup
from os import listdir

setup(name='pi3d',
      version='2.8',
      description='pi3d OpenGLES2 3D graphics library',
      author='Tim Skillman, Paddy Gaunt, Tom Ritchford',
      author_email='http://pi3d.github.com/html/index.html',
      url='http://pi3d.github.com/html/index.html',
      packages=['pi3d','pyxlib','pi3d.constants','pi3d.shape','pi3d.util',
          'pi3d.event','pi3d.loader','pi3d.sprite','pi3d.'],
      py_modules=['six'],
      package_data={'pi3d': ['shaders/*', 'util/icons/*']},
      data_files=[('', ['ChangeLog.txt'])],
      license='MIT generally but see docstrings in specific files',
      platforms=['Raspberry Pi', 'Linux (requires X and mesa-utils-extra)',
                 'Windows (requires pygame and ANGLE dll_s)'],
      long_description=open('README', 'r').read(),
      classifiers=['Development Status :: 5 - Production/Stable',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              'Topic :: Education',
              'Topic :: Games/Entertainment :: First Person Shooters',
              'Topic :: Games/Entertainment :: Simulation',
              'Topic :: Multimedia :: Graphics :: 3D Modeling',
              'Topic :: Multimedia :: Graphics :: 3D Rendering',
              'Topic :: Software Development :: Libraries :: Python Modules',
              ],
     )
