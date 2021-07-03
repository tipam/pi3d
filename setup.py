#!/usr/bin/env python
""" to create a Distutils distribution package you need to run from
a terminal cd to the pi3d directory with this file in:

  $ python setup.py sdist
  
and, as the now preferred, wheel format.
  
  $ python setup.py bdist_wheel --universal

[for uploading to pypi then:

  $ twine upload dist/pi3d-2.27* -u USERNAME -p PASSWORD #or whatever version it's up to]

this will create the directory 'dist' containing pi3d-1.10.tar.gz (and wheel)
this can then be extracted somewhere and in that directory run (probably sudo):

  $ python setup.py install

which will put all of the pi3d files in /usr/local/lib/python2.7/dist-packages
or equivalent. After that you won't need the line in the demos:

  import demo

which really just does this:

  import sys
  sys.append('/home/pi/pi3d')

# see the pull request from stuaxo here https://github.com/tipam/pi3d/pull/183
as to why you might want to use setuptools rather than distutils. Hopefull
works ok this time... """
try:
    from setuptools.commands import setup
except ImportError:
    from distutils.core import setup
from os import listdir

with open('pi3d/constants/__init__.py', 'r') as f:
  for l in f:
    if l.find('__version__') == 0:
      version = (l.split('=')[1]).strip().strip("\'\"")
      break

setup(name='pi3d',
      version=version,
      description='pi3d OpenGLES2 3D graphics library',
      author='Tim Skillman, Paddy Gaunt, Tom Ritchford',
      author_email='patrick@eldwick.org.uk',
      url='http://pi3d.github.com/html/index.html',
      packages=['pi3d','pyxlib','pi3d.constants','pi3d.shape','pi3d.util',
          'pi3d.event','pi3d.loader','pi3d.sprite','pi3d.'],
      install_requires=['Pillow',
                        'numpy'],
      py_modules=['six_mod'],
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
