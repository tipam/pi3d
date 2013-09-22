pi3d_demos
==========

Demos and support files for pi3d (3D graphics python package for the
raspberry pi)

In order to run these demos you need to have pi3d. You should look at
pi3d.github.io/html/index.html for instructions on install and using it.

The zip file is currently about 28MB and unzips to about 40MB of which
a small number of large files used in ConferenceHall, Triceratops, Silo,
TigerTank and Jukebox contribute half.

These demos give examples of how you can structure your work and allow
different projects to share resource. i.e. directory structure::

    /home/pi/
       |-MyWork
       |---images             # general1.jpg
       |---models             # house.obj house.mtl house.jpg
       |---python
       |-----roller           # rollercoaster.py
       |-------roller_images  # rollpic1.jpg
       |-------roller_shaders # rollshader1.vs, .fs
       |---test_results
       |---xyz
       |-Music
        ... etc
       |-pi3d
       |---experiments
       |---images
       |---pi3d
       |-----constants
       |-----event
        ... etc
       |-pi3d_demos
       |---fonts
       |---models
       |-----AllSaints
       |-----Buckfast Abbey
       |-----ConferenceHall
       |... etc
       |---textures
       |-----biplane
       |-----ecubes
       |-------Cloudy
        ... etc

then, say, in /home/pi/MyWork/python/roller/rollercoaster.py::

    ...
    import sys
    sys.path.append("/home/pi/pi3d")
    import pi3d
    ...
    mymodel1 = pi3d.Model("../../models/house.obj")
    mymodel2 = pi3d.Model("/home/pi/pi3d_demos/models/teapot.obj")
    mytex1 = pi3d.Texture("../../images/general1.jpg")
    mytex2 = pi3d.Texture("roller_images/rollpic1.jpg")
    myshader1 = pi3d.Shader("uv_flat") # generic from pi3d package
    mypost = pi3d.PostProcess("roller_shaders/rollshader1")
    ...
