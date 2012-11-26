# Shapes using pi3d module
# ========================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 03Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#

from pi3d import Display
from pi3d.Font import Font
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.context.Light import Light

from pi3d.shape.Cone import Cone
from pi3d.shape.Cylinder import Cylinder
from pi3d.shape.Extrude import Extrude
from pi3d.shape.Helix import Helix
from pi3d.shape.Lathe import Lathe
from pi3d.shape.Sphere import Sphere
from pi3d.shape.TCone import TCone
from pi3d.shape.Torus import Torus
from pi3d.shape.Tube import Tube
from pi3d.shape.Plane import Plane

from pi3d.util import Draw
from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create()
DISPLAY.setBackColour(0,0,0,1)    	# r,g,b,alpha

# Load textures
patimg = Texture("textures/PATRN.PNG")
coffimg = Texture("textures/COFFEE.PNG")

#Create inbuilt shapes
mysphere = Sphere(1,24,24,0.0,"sphere",-4,2,-7)
mytcone = TCone(0.8,0.6,1,24,"TCone", -2,2,-7)
myhelix = Helix(0.4,0.1,12,24,1.5,3.0,"helix", 0,2,-7)
mytube = Tube(0.4,0.1,1.5,24,"tube",2,2,-7, 30,0,0)
myextrude = Extrude( ((-0.5, 0.5), (0.5,0.7), (0.9,0.2), (0.2,0.05), (1.0,0.0), (0.5,-0.7), (-0.5, -0.5)), 0.5,"Extrude",4,2,-7)

mycone = Cone(1,2,24,"Cone",-4,-1,-7)
mycylinder = Cylinder(.7,1.5,24,"Cyli",-2,-1,-7)
myhemisphere = Sphere(1,24,24,0.5,"hsphere",0,-1,-7)
mytorus = Torus(1,0.3,12,24,"Torus", 2,-1,-7)
#NB Lathe needs to start at the top otherwise normals are calculated in reverse, also inside surfaces need to be defined otherwise normals are wrong
mylathe = Lathe( ((0,1),(0.6,1.2),(0.8,1.4),(1.09,1.7), (1.1,1.7),(0.9, 1.4),(0.7,1.2),(0.08,1),(0.08,0.21),(0.1,0.2),(1,0.05),(1,0),(0,0)), 24,"Cup",4,-1,-7, 0,0,0, 0.8,0.8,0.8)

myPlane = Plane(4,4,"plane",0,0,0)
myPlane.translate(0,0,-10)

arialFont = Font("AR_CENA","#dd00aa")   #load AR_CENA font and set the font colour to 'raspberry'
destineFont = Font("AR_Destine", "#0055ff")


# Fetch key presses
mykeys = Keyboard()

#create a light
mylight = Light(0, 2,2,2, "", 1,0,0, 0.1,0.1,0.1, 0)
mylight.on()

# Display scene
while 1:
  DISPLAY.clear()

  mysphere.draw(patimg)
  mysphere.rotateIncY( 0.5 )

  myhemisphere.draw(coffimg)
  myhemisphere.rotateIncY( .5 )

  myhelix.draw(patimg)
  myhelix.rotateIncY(3)
  myhelix.rotateIncZ(1)

  mytube.draw(coffimg)
  mytube.rotateIncY(3)
  mytube.rotateIncZ(2)

  myextrude.draw(coffimg,patimg,patimg)
  myextrude.rotateIncY(-2)
  myextrude.rotateIncX(0.37)

  mycone.draw(coffimg)
  mycone.rotateIncY(-2)
  mycone.rotateIncZ(1)

  mycylinder.draw(patimg)
  mycylinder.rotateIncY(2)
  mycylinder.rotateIncZ(1)

  mytcone.draw(coffimg)
  mytcone.rotateIncY(2)
  mytcone.rotateIncZ(-1)

  mytorus.draw(patimg)
  mytorus.rotateIncY(3)
  mytorus.rotateIncZ(1)

  mylathe.draw(patimg)
  mylathe.rotateIncY(2)
  mylathe.rotateIncZ(1)

  myPlane.draw(coffimg)
  myPlane.rotateIncY(9)

  Draw.string(arialFont, "Raspberry Pi ROCKS!",
              -0.8, -0.7, -2.2, 10.0, 0.003, 0.003)
  #pi3d.drawString(destineFont,"Some nice OpenGL bitmap fonts to play with",-1.3,-0.3,-2.2, 10.0, 0.002,0.002)

  k = mykeys.read()
  if k >-1:
    if k==112: screenshot("shapesPic.jpg")
    elif k==27:
      mykeys.close()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
