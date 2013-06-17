#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Various standard shapes demonstrates different ways of setting draw details
either prior to or while drawing.
The demo also shows the way to import all the pi3d modules and using the String
and Font classes (see /usr/share/fonts/truetype/ for other fonts) The string
is a 3d object like the others. See the Blur demo for use of an orthographic (2D)
string object.
"""
# just allow this to run in a subdirectory
import demo
# Load *all* the classes
import pi3d
# Load diplay, nearly full screen
DISPLAY = pi3d.Display.create(x=20, y=20)
# Load shaders
shader = pi3d.Shader("shaders/uv_reflect")
flatsh = pi3d.Shader("shaders/uv_flat")
##########################################
# Load textures
patimg = pi3d.Texture("textures/PATRN.PNG")
coffimg = pi3d.Texture("textures/COFFEE.PNG")
shapebump = pi3d.Texture("textures/floor_nm.jpg")
shapeshine = pi3d.Texture("textures/stars.jpg")

#Create inbuilt shapes
mysphere = pi3d.Sphere(radius=1, sides=24, slices=24, name="sphere",
        x=-4, y=2, z=10)
mytcone = pi3d.TCone(radiusBot=0.8, radiusTop=0.6, height=1, sides=24, name="TCone", 
        x=-2, y=2, z=10)
myhelix = pi3d.Helix(radius=0.4, thickness=0.1, ringrots=12, sides=24, rise=1.5, 
        loops=3.0, name="helix",x=0, y=2, z=10)
mytube = pi3d.Tube(radius=0.4, thickness=0.1, height=1.5, sides=24, name="tube",
        x=2, y=2, z=10, rx=30)
myextrude = pi3d.Extrude(path=((-0.5, 0.5), (0.5,0.7), (0.9,0.2),
        (0.2,0.05), (1.0,0.0), (0.5,-0.7), (-0.5, -0.5)), height=0.5, name="Extrude",
        x=4, y=2, z=10)
# Extrude can use three different textures if they are loaded prior to draw()
myextrude.set_shader(shader)
myextrude.buf[0].set_draw_details(shader, [coffimg, shapebump, shapeshine], 4.0, 0.2)
myextrude.buf[1].set_draw_details(shader, [patimg, shapebump, shapeshine], 4.0, 0.2)
myextrude.buf[2].set_draw_details(shader, [shapeshine, shapebump, shapeshine], 4.0, 0.2)

mycone = pi3d.Cone(radius=1, height=2, sides=24, name="Cone",
        x=-4, y=-1, z=10)
mycylinder = pi3d.Cylinder(radius=0.7, height=1.5, sides=24, name="Cyli",
        x=-2, y=-1, z=10)
myhemisphere = pi3d.Sphere(radius=1, sides=24, slices=24, hemi=0.5, name="hsphere",
        x=0, y=-1, z=10)
mytorus = pi3d.Torus(radius=1, thickness=0.3, ringrots=12, sides=24, name="Torus",
        x=2, y=-1, z=10)
# NB Lathe needs to start at the top otherwise normals are calculated in reverse,
# also inside surfaces need to be defined otherwise normals are wrong
mylathe = pi3d.Lathe(path=((0,1),(0.6,1.2),(0.8,1.4),(1.09,1.7), (1.1,1.7),
        (0.9, 1.4),(0.7,1.2),(0.08,1),(0.08,0.21),(0.1,0.2),(1,0.05),(1,0),(0,0)), 
         sides=24, name="Cup", x=4, y=-1, z=10, sx=0.8, sy=0.8, sz=0.8)
myPlane = pi3d.Plane(w=4, h=4, name="plane", z=12)
# Load ttf font and set the font colour to 'raspberry'
arialFont = pi3d.Font("fonts/FreeMonoBoldOblique.ttf", "#dd00aa")
mystring = pi3d.String(font=arialFont, string="Now the Raspberry Pi really does rock", z=4)
mystring.set_shader(flatsh)

# Fetch key presses
mykeys = pi3d.Keyboard()
angl = 0.0
# Display scene
while DISPLAY.loop_running():

  mysphere.draw(shader, [patimg])
  mysphere.rotateIncY( 0.5 )

  myhemisphere.draw(shader, [coffimg])
  myhemisphere.rotateIncY( .5 )

  myhelix.draw(shader, [patimg])
  myhelix.rotateIncY(3)
  myhelix.rotateIncZ(1)

  mytube.draw(shader, [coffimg, shapebump, shapeshine], 4.0, 0.1)
  mytube.rotateIncY(3)
  mytube.rotateIncZ(2)

  # Extrude has different textures for each Buffer so has to use
  # set_draw_details() above, rather than having arguments passed to draw()
  myextrude.draw()
  myextrude.rotateIncY(-2)
  myextrude.rotateIncX(0.37)

  mycone.draw(shader, [coffimg])
  mycone.rotateIncY(-2)
  mycone.rotateIncZ(1)

  mycylinder.draw(shader, [patimg, shapebump, shapeshine], 4.0, 0.1)
  mycylinder.rotateIncY(2)
  mycylinder.rotateIncZ(1)

  mytcone.draw(shader, [coffimg])
  mytcone.rotateIncY(2)
  mytcone.rotateIncZ(-1)

  mytorus.draw(shader, [patimg, shapebump, shapeshine], 4.0, 0.6)
  mytorus.rotateIncY(3)
  mytorus.rotateIncZ(1)

  mylathe.draw(shader, [patimg])
  mylathe.rotateIncY(2)
  mylathe.rotateIncZ(1)

  myPlane.draw(shader, [coffimg])
  myPlane.rotateIncX(9)

  mystring.draw()
  mystring.rotateIncZ(0.5)

  k = mykeys.read()
  if k >-1:
    if k==112: pi3d.screenshot("shapesPic.jpg")
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
