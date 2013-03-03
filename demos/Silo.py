#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Show how to use the Building class. This has the facility to define solid
objects that cannot pass through other solid objects. The walls of Building
are constructed of solid object. There are two examples of solid corridor
created near to the silo.
This demonstration also shows in a fairly rough way how lighting can be changed
as the view point moves (from inside to outside in this instance).
"""
import math

import demo

from pi3d import Display
from pi3d.Texture import Texture

from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.Building import Building, corridor, SolidObject, Size, Position

from pi3d.util.Screenshot import screenshot

from pi3d.Light import Light

from pi3d.event.Event import InputEvents

# Setup display and initialise pi3d
DISPLAY = Display.create(x=150, y=150, background=(0.4, 0.8, 0.8, 1))
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#############################

# Load textures
blockimg = Texture("textures/squareblocks4.png")
roofedgeimg = Texture("textures/roofedging.png")
roofimg = Texture("textures/Roof.png")
greenimg = Texture("textures/squareblocks4green.png")
ectex = loadECfiles("textures/ecubes", "sbox", "jpg")
myecube = EnvironmentCube(size=900.0, maptype="FACES")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
floorimg = Texture("textures/dunes3_512.jpg")
bumpimg = Texture("textures/mudnormal.jpg")
mymap = ElevationMap(mapfile="textures/mountainsHgt2.png",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=64, divy=64)
mymap.set_draw_details(shader,[floorimg, bumpimg],128.0, 0.0)
mymap.set_fog((0.3,0.25,0.1,0.2), 500.0)

#Create some random block models elsewhere on the map!
corridor(150, 10, mymap, details = [shader, [blockimg, blockimg], 1.0, 0.0, 4.0, 4.0], walls="ns")
corridor(120, -40, mymap, details = [shader, [blockimg, blockimg], 1.0, 0.0, 4.0, 4.0], walls="ew")

# openSectionScheme: black is wall, white is corridor or room, grey has no ceiling, there is one model
# Model 0: wall
# Model 1: wall in the open
# Model 2: roof
# Model 3: roof edge
openSectionSchemeMultimodel = {"#models": 4,
              (0,None) : [["R",2]],           # black cell has a roof
              (2,None):[["C", 0], ["R", 2]],      # white cell has a ceiling and roof
              (0,0,"edge"):[["W",0], ["CE", 3]],    # black cell on the edge next to a black cell has a wall and ceiling edge
              (1,0,"edge"):[["W",0], ["CE", 3]],    # grey cell on the edge next to a black cell has a wall and ceiling edge
              (2,0,"edge"):[["W",0], ["CE", 3]],    # white cell on the edge next to a black cell has a wall and ceiling edge
              (2,2,"edge"):[["CE", 3]],         # white cell on the edge next to a white cell a ceiling edge
              (2,0):[["W", 0]],             # white cell next to a black cell has a wall
              (1,0):[["W", 1], ["CE", 3]],       # grey cell next to a black cell has a wall and ceiling edge
              (1,2):[["CE", 3]] }            # grey cell next to a white cell has a ceiling edge

# details is an array of the same size as models array (defined above as part of the dict {"#models":4,..} )
# contains information corresponding with Buffer.set_draw_details()
details = [[shader, [blockimg, blockimg], 1.0, 0.0, 4.0, 12.0],
                [shader, [greenimg, greenimg], 1.0, 0.0, 4.0, 4.0],
                [shader, [roofimg, blockimg], 1.0, 0.0, 4.0, 4.0],
                [shader, [roofedgeimg], 0.0, 0.0, 4.0, 4.0]]

building = Building("textures/silo_map.png", 0, 0, mymap, width=15.0, depth=15.0, height=70.0, name="", draw_details=details, yoff=-15, scheme=openSectionSchemeMultimodel)

outLight = Light(lightpos=(10, -10, 20), lightcol =(1.0, 1.0, 0.7), lightamb=(0.35, 0.35, 0.4))
inLight = Light(lightpos=(10, -10, 20), lightcol =(0.1, 0.1, 0.15), lightamb=(0.05, 0.15, 0.1))
for b in building.model:
  b.set_light(inLight, 0)
mymap.set_light(inLight, 0)
inFlag = True

#screenshot number
scshots = 1

#avatar camera
rot=0.0
tilt=0.0
avhgt = 5.0
aveyelevel = 4.0

aveyeleveladjust = aveyelevel - avhgt/2

man = SolidObject("man", Size(1, avhgt, 1), Position(0, (mymap.calcHeight(5, 5) + avhgt/2), 0), 1)

inputs = InputEvents()

inputs.get_mouse_movement()
mouseOn = True

frame = 400
record = False
CAMERA = Camera.instance()
while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((man.x(), man.y(), man.z() - aveyeleveladjust))

  myecube.position(man.x(), man.y(), man.z() - aveyeleveladjust)

  SolidObject.drawall()

  building.drawAll()

  mymap.draw()
  myecube.draw()

  inputs.do_input_events()
  """On some combined keyboard/mouse arrangements you might need to change
  this to inputs.get_mouse_movement(1) in order to get the correct input
  """
  mx, my, mv, mh, md = inputs.get_mouse_movement()

  rot -= (mx)*0.2
  tilt -= (my)*0.2

  #jrx, jry, jrz = inputs.get_joystickB3d() # xbox 360
  # sudo apt-get install xboxdrv
  # sudo xboxdrv -s -i 0
  jrx, jry = inputs.get_joystickR() # gamepad
  if abs(jrx) > 0.1:
      rot -= jrx*3

  if abs(jry) > 0.1:
      tilt -= jry*3

  xm = man.x()
  ym = man.y()
  zm = man.z()

  jx, jy = inputs.get_joystick()
  if abs(jy) > 0.2:
      xm += math.sin(math.radians(rot))*jy
      zm -= math.cos(math.radians(rot))*jy

  if abs(jx) > 0.2:
      xm -= math.sin(math.radians(rot-90))*jx
      zm += math.cos(math.radians(rot-90))*jx

  if inputs.key_state("BTN_LEFT"):
    xm -= math.sin(math.radians(rot))
    zm += math.cos(math.radians(rot))

  if inputs.key_state("KEY_W"):  #key W
    xm -= math.sin(math.radians(rot))
    zm += math.cos(math.radians(rot))

  if inputs.key_state("KEY_S"): #key S
    xm += math.sin(math.radians(rot))
    zm -= math.cos(math.radians(rot))

  ym = (mymap.calcHeight(xm,zm)+avhgt)
  NewPos = Position(xm, ym, zm)
  collisions = man.CollisionList(NewPos)

  if not collisions:
    man.move(NewPos)

  if inFlag and abs(man.z() - building.zpos) > 55:
    inFlag = False
    for b in building.model:
      b.set_light(outLight, 0)
    mymap.set_light(outLight, 0)

  if inputs.key_state("KEY_APOSTROPHE"):  #key '
    tilt -= 2.0
  if inputs.key_state("KEY_SLASH"):  #key /
    tilt += 2.0
  if inputs.key_state("KEY_A"):  #key A
    rot += 2
  if inputs.key_state("KEY_D"): #key D
    rot -= 2
  if inputs.key_state("KEY_P"): #key P
    #record = not(record)
    while inputs.key_state("KEY_P"):
    	inputs.do_input_events()		# wait for key to go up
    screenshot("silo"+str(scshots)+".jpg")
    scshots += 1
  if inputs.key_state("KEY_ENTER"):  #key RETURN
    mc = 0
  if inputs.key_state("KEY_X"):  #key RETURN
    while inputs.key_state("KEY_X"):
      inputs.do_input_events() # wait for key to go up
    mouseOn != mouseOn
    inputs.grab_by_type("keyboard", grab=mouseOn)

inputs.release()
DISPLAY.destroy()
