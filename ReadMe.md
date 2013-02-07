## **Pi3D ReadMe**

![Pi3D logo](http://pi3d.github.com/html/_images/rpilogoshad128.png)

**Pi3D (vsn 0.08) written by Tim Skillman, Paddy Gaunt, Tom Ritchford Copyright (c) 2013**

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

A short introduction to using pi3d can be found on this github. There are links from there
to the full documentation of the different modules.
http://pi3d.github.com/html/ReadMe.html

# Files and folders in this repository

1.  **pi3d** The main pi3d module files 540 kB
2.  **shaders** Shader files used by the pi3d module 33 kB
3.  **echomesh** Utility functions 14kB
4.  **textures** Various textures to play with 13 MB
5.  **models** Demo obj and egg models 26 MB
6.  **fonts** ttf and Bitmap fonts that can be using for drawing text see in
    /usr/share/fonts/truetype for others, or look online. 1.0 MB
7.  **demos** Source code of the demos included 96 kB
8.  **screenshots** Example screenshots of the demos included 860 kB
9.  **documentation** Where this documentation lives 5.7 MB
10.  **ChangeLog.txt** Latest changes of Pi3D
11.  **ReadMe.md** Simplified markdown summary of this file

Please note that Pi3D functions may change significantly during it's development.

Bug reports, comments, feature requests and fixes are most welcome!

Please email on pi3d@googlegroups.com or contact us through the Raspberry Pi forums.

# Acknowledgements

Pi3D started with code based on Peter de Rivaz 'pyopengles' (https://github.com/peterderivaz/pyopengles)
with some tweaking from Jon Macey's code (jonmacey.blogspot.co.uk/2012/06/). 

Many Thanks, especially to Peter de Rivaz, Jon Macey, Richard Urwin, Peter Hess, David Wallin
and others who have contributed to Pi3D - keep up the good work!

**PLEASE READ LICENSING AND COPYRIGHT NOTICES ESPECIALLY IF USING FOR COMMERCIAL PURPOSES**
