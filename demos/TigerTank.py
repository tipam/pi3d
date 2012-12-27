# Tiger Tank in TK window
# Version 0.02 - 23Nov12
#
# First tank demo - more to come!

import math, random, time, traceback

from pi3d import *

from pi3d import Display
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.context.Fog import Fog
from pi3d.context.Light import Light

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model

from pi3d.util.Screenshot import screenshot
from pi3d.util import Log
from pi3d.util.TkWin import TkWin

# TODO(rec): why doesn't this work when True?  It should be executing the same
# code!
USE_EXTERNAL_LOOP = not True

LOGGER = Log.logger(__name__)

# Create a Tkinter window
winw, winh, bord = 1200, 600, 0     #64MB GPU memory setting
# winw,winh,bord = 1920,1200,0   #128MB GPU memory setting

DISPLAY = Display.create(tk=True, window_title='Tiger Tank demo in Pi3D',
                         mouse=True, w=winw, h=winh - bord,
                         far=2200.0, background=(0.4, 0.8, 0.8, 1))

win = DISPLAY.tkwin

camera = Camera((0, 0, 0), (0, 0, -1),
                (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))

light = Light((10, 10, -20))
shader = Shader('shaders/uv_reflect')
flatsh = Shader('shaders/uv_flat')

#========================================

ectex = EnvironmentCube.loadECfiles('textures/ecubes/Miramar', 'miramar_256',
                                    suffix='png')
myecube = EnvironmentCube.EnvironmentCube(camera, light, 1800.0, 'FACES')
for i, b in enumerate(myecube.buf):
  b.set_draw_details(flatsh, [ectex[i]], 0.0, -1.0)

# Create elevation map
mapwidth = 2000.0
mapdepth = 2000.0
mapheight = 100.0
mountimg1 = Texture('textures/mountains3_512.jpg')
bumpimg = Texture('textures/grasstile_n.jpg')
tigerbmp = Texture('models/Tiger/tiger_bump.jpg')
topbmp = Texture('models/Tiger/top_bump.jpg')
#roadway = Texture('textures/road5.png')
mymap = ElevationMap(camera=camera, light=light,
                     mapfile='textures/mountainsHgt2.png',
                     width=mapwidth, depth=mapdepth,
                     height=mapheight, divx=64, divy=64)

mymap.buf[0].set_draw_details(shader, [mountimg1, bumpimg], 128.0, 0.0)

FOG = (0.7, 0.8, 0.9, 0.5)

def set_fog(shape):
  shape.set_fog(FOG, 1000.0)

def make_model(filename, name, x=0, y=0, z=0, rx=0, ry=0, rz=0):
  model = Model(camera, light, 'models/' + filename,
                name=name, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz,
                sx=0.1, sy=0.1, sz=0.1)
  model.set_shader(shader)
  set_fog(model)
  return model

set_fog(mymap)

#Load tank
tank_body = make_model('Tiger/bodylow.egg', 'TigerBody')
tank_body.set_normal_shine(tigerbmp)

tank_gun = make_model('Tiger/gunlow.egg', 'TigerGun')

tank_turret = make_model('Tiger/turretlow.egg', 'TigerTurret')
tank_turret.set_normal_shine(topbmp)


#Load church
x, z = 20, -320
y = mymap.calcHeight(x,z)

church = make_model('AllSaints/AllSaints.egg', 'church1', x, y, z)
church = make_model('AllSaints/AllSaints-lowpoly.egg', 'church1', x, y, z)

#Load cottages
x, z = 250,-40
y = mymap.calcHeight(x,z)

cottages = make_model('Cottages/cottages_low.egg', 'cottagesLo', x, y, z, ry=-5)
#cottagesHi = Model(camera, light, 'models/Cottages/cottages.egg', 'cottagesHi',
#                   x,y,z, -90,-5,0, .1,.1,.1)

#player tank vars
tankrot = 180.0
turret = 0.0
tankroll = 0.0     #side-to-side roll of tank on ground
tankpitch = 0.0   #too and fro pitch of tank on ground

#position vars
mouserot = 0.0
tilt = 0.0
avhgt = 0.85
xm, oxm = 0.0, -1.0
zm, ozm = -200.0, -1.0
dxm = 0.0
dzm = -1.0
ym = mymap.calcHeight(xm, zm) + avhgt

#enemy tank vars
#etx = 130
#etz = -320
etx = 130
etz = -100
etr = 0.0

omx, omy = DISPLAY.mouse.x, DISPLAY.mouse.y

myfog = Fog(0.0014, FOG)

ltm = 0.0 #last pitch roll check

def drawTiger(x, y, z, rot, roll, pitch, turret, gunangle):
  tank_body.position(x, y, z)
  tank_body.rotateToX(pitch)
  tank_body.rotateToY(rot)
  tank_body.rotateToZ(roll)
  tank_body.draw()
  tank_turret.position(x, y, z)
  tank_turret.rotateToX(pitch)
  tank_turret.rotateToY(turret)
  tank_turret.rotateToZ(roll)
  tank_turret.draw()
  tank_gun.position(x, y, z)
  tank_gun.rotateToX(pitch + gunangle)
  tank_gun.rotateToY(turret)
  tank_gun.rotateToZ(roll)
  tank_gun.draw()

is_running = True

def loop():
  global tilt, roll, pitch, xm, ym, zm, ltm, tankpitch, tankroll, tankrot, turret
  global etx, ety, etz, etr, omx, omy, oxm, ozm, tankpitch_to, tankpitch_fr, mouserot
  global tankroll_to, ltm

  #update mouse/keyboard input
  mx, my = DISPLAY.mouse.x, DISPLAY.mouse.y
  if mx != omx or my != omy or xm != oxm or zm != ozm:
    mouserot -= (mx - omx) * 0.6
    tilt += (my - omy) * 0.2
    omx, omy = mx, my

    camera.reset()
    # tilt can be used to prevent the view from going under the landscape!
    sf = 60 - 55.0 / abs(tilt) if tilt < -1 else 5.0
    xoff = sf * math.sin(math.radians(mouserot))
    yoff = abs(1.25 * sf * math.sin(math.radians(tilt))) + 3.0
    zoff = -sf * math.cos(math.radians(mouserot))

    #xoff, yoff, zoff = 0,0,0
    #camera.translate((xm, ym-10*sf-5.0, zm-40*sf))
    #zoom camera out so we can see our robot
    camera.rotate(tilt, mouserot, 0)           #Tank still affected by scene tilt
    camera.translate((xm + xoff, ym + yoff + 5, zm + zoff))
    oxm, ozm = xm, zm
    #zoom camera out so we can see our robot

  #draw player tank
  tmnow = time.time()
  if tmnow > (ltm + 0.5):
    tankpitch_to, tankroll_to = mymap.pitch_roll(xm, zm)
  tankpitch += (tankpitch_to - tankpitch)/3.0
  tankroll += (tankroll_to - tankroll)/3.0
  drawTiger(xm, ym, zm, tankrot, tankroll, tankpitch, 180 - turret, 0.0)

  mymap.draw()           # Draw the landscape

  #Draw enemy tank
  etdx = -math.sin(math.radians(etr))
  etdz = -math.cos(math.radians(etr))
  etx += etdx
  etz += etdz
  ety = mymap.calcHeight(etx, etz) + avhgt
  etr += 0.5
  if tmnow > (ltm + 0.5):
    pitch, roll = mymap.pitch_roll(etx, etz)
    ltm = tmnow # updating this here but not for users tank relies on everything
                # being done in the right order
  drawTiger(etx, ety, etz, etr, roll, pitch, etr, 0)

  #Draw buildings
  #Draw.lodDraw3(-xm, -ym, -zm, 300, church, 1000, churchlow)
  church.draw()
  cottages.draw()

  myecube.position(xm, ym, zm)
  myecube.draw()  #Draw environment cube

  # turns player tankt turret towards center of screen which will have a crosshairs
  if turret + 2.0 < mouserot:
    turret += 2.0
  if turret - 2.0 > mouserot:
    turret -= 2.0

  # Handle window events
  try:
    win.update()
  except:
    print 'bye bye 3'
    DISPLAY.stop()
    return

  if win.ev=='key':
    if win.key == 'w':
      dxm = -math.sin(math.radians(tankrot)) * 2
      dzm = -math.cos(math.radians(tankrot)) * 2
      xm += dxm
      zm += dzm
      ym = (mymap.calcHeight(xm, zm) + avhgt)

    elif win.key == 's':
      xm += math.sin(math.radians(tankrot)) * 2
      zm += math.cos(math.radians(tankrot)) * 2
      ym = (mymap.calcHeight(xm, zm) + avhgt)
    elif win.key == 'a':
      tankrot -= 2
    elif win.key == 'd':
      tankrot += 2
    elif win.key == 'p':
      screenshot('TigerTank.jpg')
    elif win.key == 'Escape':
      DISPLAY.stop()
      return

  elif win.ev == 'resized':
    DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)
    win.resized = False
    # This flag must be reset otherwise no further events will be detected

  win.ev = ''  # Clear the event so it doesn't repeat.

  camera.movedFlag = False

if USE_EXTERNAL_LOOP:
  # This fails.
  while DISPLAY.loop_running():
    loop()

else:
  # This works.
  while DISPLAY.is_running:
    DISPLAY.clear()
    loop()
    DISPLAY.swapBuffers()

DISPLAY.destroy()

