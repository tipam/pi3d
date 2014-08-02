Introduction to Pi3D
====================

.. image:: images/rpilogoshad128.png
   :align: left 

**Pi3D written by Tim Skillman, Paddy Gaunt, Tom Ritchford Copyright (c) 2014**

There's plenty of 3D code flying around at the moment for the Raspberry Pi,
but much of it is rather complicated to understand and most of it can sit
under the bonnet!

Pi3D is a Python module that aims to greatly simplify writing 3D in Python
whilst giving access to the power of the Raspberry Pi GPU. It enables both
3D and 2D rendering and aims to provide a host of exciting commands to load
in textured/animated models, create fractal landscapes, shaders and much more.

v1.9 release of the Pi3D module adds support for
running on platforms other than the raspberry pi (X on linux) and runs with
python 3 as well as 2 The OpenGLES2.0 functionality of the Raspberry Pi
is used directly or via mesa on 'big' machines. This makes it generally *faster*
and opens up the world of *shaders* that allow effects such as normal and 
reflection maps, blurring and many others. It has various demos of built-in
shapes, landscapes, model loading, walk-about camera and much more! See the demos
included with this code and experiment with them ..

If you are reading this document as the ReadMe in the repository then you
can find the full version of the documentation here
http://pi3d.github.com/html/index.html

Demos for Pi3D are now stored at https://github.com/pi3d/pi3d_demos
===================================================================
N.B. Shaders are now integrated into programs differently. The syntax used
to be::

    myshader = pi3d.Shader('shaders/uv_flat')

and is now::

    myshader = pi3d.Shader('uv_flat')

this will use the default shaders 'bundled' with the package. The old format
will be interpreted as 'look in a subdirectory of the directory where the demo
is being run from.' This is probably what you would do if you rolled your own
special shaders for your own project.

Demos on github.com/pi3d/pi3d_demos include
===========================================

#.  **ForestWalk.py** Walk about a forest on a landscape generated from a
    bitmap
      .. image:: images/forestwalk_sml.jpg
         :align: right

#.  **Triceratops.py** Large model loading with several
    bitmaps
      .. image:: images/triceratops_sml.jpg

#.  **BuckfastAbbey.py** Explore a model of the beautiful Buckfast Abbey in 
    Buckfastleigh, Devon, England
      .. image:: images/buckfast_sml.jpg
         :align: right

#.  **Earth.py** Demonstrates semi-transparent clouds and hierarchical
    rotations
      .. image:: images/earth_sml.jpg

#.  **Clouds3D.py** Blended sprites in
    perspective view
      .. image:: images/clouds3d_sml.jpg
         :align: right

#.  **Raspberry_Rain.py** Raining Raspberries,  full-screen, over the
    desktop
      .. image:: images/raspberryrain_sml.jpg

#.  **RobotWalkabout.py** Another off-planet example of a basic avatar robot
    drifting about
      .. image:: images/walkabout_sml.jpg
         :align: right

#.  **EnvironmentCube.py** New environment cubes to try out in texture/ecubes -
    some high quality ones!
      .. image:: images/envcube_sml.jpg

#.  **Shapes.py** Demos available shapes and text
    in a 3D context
      .. image:: images/shapes_sml.jpg
         :align: right

#.  **MarsStation.py** Navigate around an abandoned Mars base-station with
    open/shut doors. Implements a new Level-Of-Detail (LOD) feature and TKwindow
    interface
      .. image:: images/marsstation_sml.jpg

#.  **Amazing.py** Can you find yourself around the
    amazing maze?
      .. image:: images/amazing_sml.jpg
         :align: right

#.  **TigerTank.py** Ever played World Of Tanks (WOT)? This tank emulates
    how a WOT tank works. Uses realistic modelling in a TKwindow
      .. image:: images/tigertank_sml.jpg

#.  **Pong.py**  A snazzy 3D version of landscape pinball and pong
    against a Raspberry!
      .. image:: images/pong_sml.jpg
         :align: right

#.  **Blur.py** Simulates giving the camera a focal distance and blurs
    nearer and further objects
      .. image:: images/blur_sml.jpg

#.  **LoadModelObj.py** Loads a model from obj file (quicker) and applies
    a normal map and relfection map
      .. image:: images/teapot_sml.jpg
         :align: right

#.  **Silo.py** Uses the Building class to create a claustrophobic maze
    set in the desert.
      .. image:: images/silo_sml.jpg

#.  **Water.py** A series of wave normal maps are used to animate a surface
    and produce a realistic moving reflection.
      .. image:: images/water_sml.jpg
        :align: right
     
#.  **ClashWalk.py** The graphics processor calculates where the camera can
    or cannot go depending on what is drawn in front of it. Potentially useful
    for first person navigation

#.  **CollisionBalls.py** More bouncing balls across the screen -
    this time  bouncing off each other on the desktop


Files and folders in this repository
====================================

Total zipped download from github c. 24 MB

#.  **pi3d** The main pi3d module files 540 kB
#.  **shaders** Shader files used by the pi3d module 33 kB
#.  **echomesh** Utility functions 14kB
#.  **textures** Various textures to play with 13 MB
#.  **models** Demo obj and egg models 26 MB
#.  **fonts** ttf and Bitmap fonts that can be using for drawing text see in
    /usr/share/fonts/truetype for others, or look online. 1.0 MB
#.  **demos** Source code of the demos included 96 kB
#.  **screenshots** Example screenshots of the demos included 860 kB
#.  **pyxlib** Library to enable use on general linux machines 209 kB
#.  **ChangeLog.txt** Latest changes of Pi3D
#.  **ReadMe.rst** This file


Setup on the Raspberry Pi
=========================

#.  **Download, Extract and install**

    If you have pip installed you should be able to open a terminal and
    type::

      sudo pip install pi3d
        or for python3
      sudo pip3 install pi3d
        
    (or pip-3.2 or whatever see below*) Otherwise you can download from
    https://pypi.python.org/pypi/pi3d and extract the package then in a
    terminal::

      sudo python setup.py install
        or for python3
      sudo python3 setup.py install

    This will put the package into the
    relevant location on your device (for instance
    /usr/local/lib/python2.7/dist-packages/) allowing it to be imported
    by your applications.

    The latest code can be obtained from https://github.com/tipam/pi3d/
    where there is a ``Download ZIP`` link, or you can install git then
    clone using ``git clone https://github.com/tipam/pi3d.git`` this git
    method will give you the option to update the code by running, from
    the pi3d directory ``git pull origin master``

#.  **Memory Split setup**

    Although most demos work on 64MB of memory, you are strongly advised to have
    a 128MB of graphics memory split, especially for full-screen 3D graphics.
    In the latest Raspbian build you need to either run ``sudo raspi-config``
    or edit the config.txt file (in the boot directory) and set the variable
    ``gpu_mem=128`` for 128MB of graphics memory.


#.  **Install Python Imaging**

    Before trying any of the demos or Pi3D, you must download the Python
    Imaging Library as this is needed for importing any graphics used by
    Pi3D. The original Imaging library is no longer really maintained and
    doesn't run on python_3. The better equivalent replacement is Pillow.
    In the near future Pillow will be the default imaging library but at the 
    time of writing you have to use the raspbian jessie repository.
    This is the 'trial' version of raspbian and to install packages from
    there you need to add an additional line to /etc/apt/sources.list::

      deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi

    (i.e. the same as the existing line but with jessie for wheezy) then
    run::
    
      sudo apt-get update
      sudo apt-get install python-pil
         or
      sudo apt-get install python3-pil

    alternatively you need to::

      sudo apt-get install python-dev python-setuptools libjpeg-dev zlib1g-dev libpng12-dev libfreetype6-dev
      sudo apt-get install python-pip
      sudo pip install Pillow
      ...

    If you miss any of the dependent libraries and need to add them later
    you will have to ``pip uninstall`` then re ``pip install``

    For python_3 support the first above will provide the required graphics
    libraries used by Pillow but you will need to swap to ``python3-dev``
    and ``python3-setuptools`` also pip is different::

      sudo apt-get install python3-pip
      sudo pip3 install Pillow

    (*used to be ``pip-3.2``, google for the latest botch!) If you do not
    intend to run python_3 you can install the old PIL: in the terminal,
    type::

      sudo apt-get install python-imaging

    If you later switch to Pillow you will need to sudo remove python-imaging
    first

    To run on Arch linux you will need to install::

      pacman -S python2
      pacman -S python2-pillow
      pacman -S python2-numpy

    this worked for me. You could install python2-imaging rather than pillow
    but that's probably a retrograde step. The Arch repository doesn't seem
    to have python3-pillow or python3-pip etc. See `FAQ`_ for a description
    of all the steps to get a quick loading stand-alone Pi3D SD card.

Setup on alternative Linux platforms
====================================

#.  The machine will need to have a gpu that runs OpenGL2+ and obviously
    it will need to have python installed. If the Linux is running in vmware
    you will need to 'enable 3d acceleration'. You need to install libraries
    that emulate OpenGLES behaviour for the gpu::

      sudo apt-get install mesa-utils-extra

    This should install libEGL.so.1 and libGLESv2.so.2 if these change
    (which I suppose they could in time) then the references will need to
    be altered in pi3d/constants/__init__.py

    The installation of PIL or Pillow should be the same as above but you
    are more likely to need to manually install python-numpy or python3-numpy

Editing scripts and running
===========================

#.  **Install Geany to run Pi3D**

    Although you can use any editor and run the scripts in a terminal using python,
    Geany is by far the easiest and most compatible application to use for creating
    and running Python scripts. Download and install it with::

      sudo apt-get install geany xterm

#.  **Optionally, install tk.**

    Some of the demos require the tk graphics toolkit.  To download and install it::

      sudo apt-get install tk

#.  **Load and run**

    Either run from the terminal ``python3 ~/pi3d_demos/Minimal.py`` or
    load any of the demos into Geany and run (using the cogs icon). As a minimum,
    scripts need these elements in order to use the Pi3D library::

      import pi3d
      DISPLAY = pi3d.Display.create(w=128, h=128)
      shader = pi3d.Shader("uv_flat")
      sprite = pi3d.ImageSprite("textures/PATRN.PNG", shader, w=10.0, h=10.0) # path relative to program dir
      while DISPLAY.loop_running():
        sprite.draw()

    But.. a real application will need other code to actually do something, for
    instance to get user input in order to stop the program!


A Very Brief Explanation
========================

The whole idea of Pi3D is that you don't have to get involved in too many of
the nuts and bolts of how the OpenGL graphics processor works however it might
help to get an overview of the layout of Pi3D. More detailed explanations can
be found in the documentation of each of the modules. Read `FAQ`_ before
you try anything ambitious or if anything goes wrong, obviously. There is a
`3D Graphics Explanation`_ where I try to explain in some more detail what
is going on.


  **Display** The `Display`_ class is the core and is used to hold screen dimension information,
  to initiate the graphics functionality and for 'central' information, such as timing,
  for the animation. There needs to be an instance of `Display`_ in existence
  before some of the other objects are created so it's a good idea to create one
  first job.
  
  **Shape** `All objects to be drawn by Pi3D`_ inherit from the `Shape`_ class which holds
  details of position, rotation, scale as well as specific data needed for
  drawing the shape. Each `Shape`_ contains an array of `Buffer`_ objects; normally
  only containing one but there could be more in complicated models created
  with external 3D applications. 
  
  **Buffer** The `Buffer`_ objects contain the arrays of values representing vertices,
  normals, faces and texture coordinates in a form that can be quickly read by
  the graphics processor. Each Buffer_ object within a `Shape`_ can be textured
  using a different image or shade (RGB) value and, if needed, a different `Shader`_
  
  **Shader** The `Shader`_ class is used to compile *very fast* programs that are run on
  the graphics processor. They have two parts: *Vertex Shaders* that do calculation
  for each of the vertices of the `Buffer`_ and *Fragment Shaders* applied to
  each pixel. In Pi3D we have kept the shaders out of the main python files
  and divided them using the two extensions .vs and .fs The shader language
  is C like, very clever indeed, but rather hard to fathom out.
  
  **Camera** In order to draw a `Shape`_ on the `Display`_ the `Shader`_ needs to be passed the
  vertex information in the Buffers and needs know how the `Shape`_ has been moved.
  But it also needs to know how the `Camera`_ has moved. The `Camera`_ class generally
  has just one instance and if you do not create one explicitly then `Display`_ will
  generate a default one when you first try to draw something. The `Camera`_
  has position and rotation information similar to Shapes but also information
  to create the view, such as how wide-angle or telephoto the lens is.
  
  **Texture** The `Texture`_ objects are used to load images from file into a form that
  can be passed to the `Shader`_ to draw onto a surface. They can also be applied as
  normal maps to give much finer local detail or as reflection maps - a much
  faster way to make surfaces look shiny than ray tracing.
  
  **Light** To produce a 3D appearance most of the Shaders use directional lighting and
  if you draw a `Shape`_ without creating a `Light`_ a default instance will be
  created by the `Display`_. The `Light`_ has properties defining the direction,
  the colour (and strength i.e. RGB values) and ambient colour (and strength).

  When you look through the demos you will see one or two things that may
  not be immediately obvious. All the demos start with::
  
    #!/usr/bin/python
    from __future__ import absolute_import, division, print_function, unicode_literals

  Although these lines can often be left out, the first tells any process running the file
  as a script that it's python and the second is basically to help the transition
  of this code to run using python 3::
  
    import demo

  Allows the demo files to be put in a subdirectory but still run. If you install
  Pi3D using pip or ``python setup.py install`` then you can take this out::
  
    import pi3d

  Is an alternative to importing just what you need i.e.::
  
    from pi3d.constants import *
    from pi3d import Display
    from pi3d.Texture import Texture
    from pi3d.Keyboard import Keyboard
    from pi3d.Light import Light
    from pi3d.Shader import Shader
    from pi3d.util.String import String
    ...
    from pi3d.shape.Sphere import Sphere
    from pi3d.shape.Sprite import Sprite

  If you import the whole lot using ``import pi3d`` then you need to prefix classes
  and functions with ``pi3d.`` A third way to import the modules would be to use
  ``from pi3d import *`` this saves having to use the ``pi3d.`` prefix but
  is **much harder to debug** if there is a name conflict.
  
.. _Display: pi3d.html#pi3d.Display.Display
.. _Shape: pi3d.html#pi3d.Shape.Shape
.. _Buffer: pi3d.html#pi3d.Buffer.Buffer
.. _Shader: pi3d.html#pi3d.Shader.Shader
.. _Camera: pi3d.html#pi3d.Camera.Camera
.. _Texture: pi3d.html#pi3d.Texture.Texture
.. _Light: pi3d.html#pi3d.Light.Light
.. _`All objects to be drawn by Pi3D`: pi3d.shape.html#module-pi3d.shape.Cone
.. _`FAQ`: FAQ.html
.. _`3D Graphics Explanation`: GPUexplain.html


Documentation
=============

Please note that Pi3D functions may change significantly during its development.

Bug reports, comments, feature requests and fixes are most welcome!

Please email on pi3d@googlegroups.com or contact us through the Raspberry Pi forums
or on http://pi3d.github.com/html/index.html


Acknowledgements
================

Pi3D started with code based on Peter de Rivaz 'pyopengles'
(https://github.com/peterderivaz/pyopengles) with some tweaking from Jon Macey's
code (jonmacey.blogspot.co.uk/2012/06/).

Many Thanks, especially to Peter de Rivaz, Jon Macey, Richar Urwin, Peter Hess,
David Wallin, Avishay Orpaz (avishorp) and others who have contributed to Pi3D
- keep up the good work!


**PLEASE READ LICENSING AND COPYRIGHT NOTICES ESPECIALLY IF USING FOR COMMERCIAL PURPOSES**

