Introduction to Pi3D
====================

.. image: images/rpilogoshad128.png

**Pi3D written by Tim Skillman, Paddy Gaunt, Tom Swirly Copyright (c) 2013**

There's plenty of 3D code flying around at the moment for the Raspberry Pi,
but much of it is rather complicated to understand and most of it can sit
under the bonnet!

pi3d is a Python module that aims to greatly simplify writing 3D in Python
whilst giving access to the power of the Raspberry Pi GPU. It enables both
3D and 2D rendering and aims to provide a host of exciting commands to load
in textured/animated models, create fractal landscapes, shaders and much more.

This is the fourth release of the pi3d module which now uses the OpenGLES2.0
functionality of the Raspberry Pi directly. This makes it generally *faster*
and opens up the world of *shaders* that allow effects such as normal and 
reflection maps, blurring and many others. It has various demos of built-in
shapes, landscapes, model loading, walk-about camera and much more! See the demos
included with this code and experiment with them ..


Demo's included with Pi3D
=========================

1) **ForestWalk.py** Walk about a forest on a landscape generated from a bitmap
.. image: images/forestwalk_sml.png
2) **Triceratops.py** Large model loading with several bitmaps
.. image: images/triceratops_sml.png
3) **BuckfastAbbey.py** Explore a model of the beautiful Buckfast Abbey in
Buckfastleigh, Devon, England
.. image: images/buckfast_sml.png
4) **Earth.py** Demonstrates semi-transparent clouds and hierarchical rotations
.. image: images/earth_sml.png
5) **Raspberry_Rain.py** Raining Raspberries,  full-screen, over the desktop
.. image: images/raspberryrain_sml.png
6) **Clouds3D.py** Blended sprites in perspective view
.. image: images/clouds3d_sml.png
7) **CollisionBalls.py** More bouncing balls across the screen - this time
bouncing off each other on the desktop
8) **EnvironmentCube.py** New environment cubes to try out in texture/ecubes -
some high quality ones!
.. image: images/envcube_sml.png
9) **RobotWalkabout.py** Another off-planet example of a basic avatar robot
drifting about
.. image: images/walkabout_sml.png
10) **Shapes.py** Demos available shapes and text in a 3D context
.. image: images/shapes_sml.png
11) **MarsStation.py** Navigate around an abandoned Mars base-station with
open/shut doors. Implements a new Level-Of-Detail (LOD) feature and TKwindow
interface
.. image: images/marsstation_sml.png)
12) **TigerTank.py** Ever played World Of Tanks (WOT)? This tank emulates how
a WOT tank works. Uses realistic modelling in a TKwindow
.. image: images/tigertank_sml.png
13) **Amazing.py** Can you find yourself around the amazing maze?
.. image: images/amazing_sml.png
14) **Pong.py**  A snazzy 3D version of landscape pinball and pong against
a Raspberry!
.. image: images/pong_sml.png
15) **Blur.py** Simulates giving the camera a focal distance and blurs nearer
and further objects
.. image: images/blur_sml.png
16) **LoadModelObj.py** Loads a model from obj file (quicker) and applies
a normal map and relfection map
.. image: images/teapot_sml.png
17) **Silo.py** Uses the Building class to create a claustrophobic maze set
in the desert.
.. image: images/silo_sml.png
18) **ClashWalk.py** The graphics processor calculates where the camera can
or cannot go depending on what is drawn in front of it. Potentially useful for
first person navigation
19) **Water.py** A series of wave normal maps are used to animate a surface
and produce a realistic moving reflection.
.. image: images/water_sml.png

Files and folders in this repository
====================================

1. **pi3d** The main pi3d module files
2. **shaders** Shader files used by the pi3d module
3. **textures** Various textures to play with
4. **models** Demo obj and egg models
5. **fonts** ttf and Bitmap fonts that can be using for drawing text
6. **screenshots** Example screenshots of the demos included
7. **documentation** Where this documentation lives
8. **ChangeLog.txt** Latest changes of Pi3D
9. **ReadMe.md** This file TODO
10. **ReadMe.htm** HTML readme TODO


Setup on the Raspberry Pi
=========================

1) **Memory Split setup**

Although most demos work on 64MB of memory, you are strongly advised to have
a 128MB of graphics memory split, especially for full-screen 3D graphics.
In the latest Raspbian build you need to edit the config.txt file (in the
boot directory) and set the variable 'gpu_mem=128' for 128MB of graphics memory.


2) **Install Python Imaging**

Before trying any of the demos or Pi3D, you must download the Python Imaging
Library as this is needed for importing any graphics used by Pi3. To install
on the terminal, type:

      sudo apt-get install python-imaging

3) **Install Geany to run Pi3D**

Geany is by far the easiest and most compatible application to use for creating
and running Python scripts. Download and install it with:

      sudo apt-get install geany xterm

4) **Optionally, install tk.**

Some of the demos require the tk graphics toolkit.  To download and install it:

    sudo apt-get install tk

5) **Load and run**

Load any of the demos into Geany and run (using the cogs icon)



Documentation
=============

A short 'manual' on using pi3d can be found on this github. Please note that
Pi3D functions may change significantly during it's development.

Bug reports, comments, feature requests and fixes are most welcome!

Please email on timskillman@gmail.com or contact me through the Raspberry Pi
forums.


Acknowledgements
================

Pi3D started with code based on Peter de Rivaz 'pyopengles'
(https://github.com/peterderivaz/pyopengles) with some tweaking from Jon Macey's
code (jonmacey.blogspot.co.uk/2012/06/).

The Panda3D loaderEgg.py and LoaderObj.py modules are written by Paddy Gaunt
(Copyright (c) 2013)

Many Thanks, especially to Paddy Gaunt, Peter de Rivaz, Tom Swirly, Jon Macey
and others who have contributed to Pi3D - keep up the good work!


**PLEASE READ LICENSING AND COPYRIGHT NOTICES ESPECIALLY IF USING FOR COMMERCIAL PURPOSES**


