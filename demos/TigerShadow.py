#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Landscape from ElevationMap with model tanks and buildings. Demonstrates using
a function to draw the various parts of the tank and the ElevationMap.pitch_roll()
method to make models conform (aproximately) to the surface of an ElevationMap.
The tank gun is raised as the mouse view point to looking up. This shows how to
combine various rotations about different axes without the objects falling apart!
This demo also uses a tkinter tkwindow but creates it as method of Display. Compare
with the system used in demos/MarsStation.py
Also look out for:
2D shader usage. Drawing onto an ImageSprite canvas placed in front of the camera
imediately after reset() This is used to generate a splash screed during file
loading and to draw a telescopic site view and a navigation map
"""
import math, random, time, traceback

import demo

from pi3d.constants import *

from pi3d import Display

from pi3d.Camera import Camera
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model
from pi3d.shape.Sprite import ImageSprite

from pi3d.util import Log
from pi3d.util.Screenshot import screenshot
from pi3d.util.TkWin import TkWin
from pi3d.util.ShadowCaster import ShadowCaster

from pi3d.Light import Light

from pi3d.event.Event import InputEvents

LOGGER = Log.logger(__name__)

# Create a Tkinter window
winw, winh, bord = 1200, 600, 0     #64MB GPU memory setting
# winw,winh,bord = 1920,1200,0   #128MB GPU memory setting

DISPLAY = Display.create(tk=True, window_title='Tiger Tank demo in Pi3D',
                        w=winw, h=winh - bord, far=2200.0,
                        background=(0.4, 0.8, 0.8, 1), frames_per_second=16)

#inputs = InputEvents()
#inputs.get_mouse_movement()

mylight = Light(lightpos=(1, -1, 0), lightcol =(0.8, 0.8, 0.8), lightamb=(0.30, 0.30, 0.32))

win = DISPLAY.tkwin

shader = Shader('shaders/uv_reflect')
flatsh = Shader('shaders/uv_flat')
shade2d = Shader('shaders/2d_flat')

#========================================
# create splash screen and draw it
splash = ImageSprite("textures/tiger_splash.jpg", shade2d, w=10, h=10, z=0.2)
splash.draw()
DISPLAY.swap_buffers()

# create environment cube
ectex = EnvironmentCube.loadECfiles('textures/ecubes/Miramar', 'miramar_256',
                                    suffix='png')
myecube = EnvironmentCube.EnvironmentCube(size=1800.0, maptype='FACES')
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth = 2000.0
mapdepth = 2000.0
mapheight = 120.0
mountimg1 = Texture('textures/mountains3_512.jpg')
bumpimg = Texture('textures/grasstile_n.jpg')
tigerbmp = Texture('models/Tiger/tiger_bump.jpg')
topbmp = Texture('models/Tiger/top_bump.jpg')
#roadway = Texture('textures/road5.png')
mymap = ElevationMap(mapfile='textures/mountainsHgt2.png',
                     width=mapwidth, depth=mapdepth,
                     height=mapheight, divx=64, divy=64)

mymap.set_draw_details(shader, [mountimg1, bumpimg], 128.0, 0.0)

FOG = (0.7, 0.8, 0.9, 0.5)

def set_fog(shape):
  shape.set_fog(FOG, 1000.0)

def make_model(filename, name, x=0, y=0, z=0, rx=0, ry=0, rz=0):
  model = Model(file_string='models/' + filename,
                name=name, x=x, y=y, z=z, rx=rx, ry=ry, rz=rz,
                sx=0.1, sy=0.1, sz=0.1)
  model.set_shader(shader)
  set_fog(model)
  return model

set_fog(mymap)

#Load tank
tank_body = make_model('Tiger/body.obj', 'TigerBody')
tank_body.set_normal_shine(tigerbmp)

tank_gun = make_model('Tiger/gun.obj', 'TigerGun')

tank_turret = make_model('Tiger/turret.obj', 'TigerTurret')
tank_turret.set_normal_shine(topbmp)


#Load church
x, z = 20, -320
y = mymap.calcHeight(x,z)

church = make_model('AllSaints/AllSaints.obj', 'church', x, y, z)

#Load cottages
x, z = 250,-40
y = mymap.calcHeight(x,z)

cottages = make_model('Cottages/cottages_low.obj', 'cottagesLo', x, y, z, ry=-5)

#ShadowCaster
myshadows = ShadowCaster(emap=mymap, light=mylight)

#cross-hairs in gun sight
targtex = Texture("textures/target.png", blend=True)
target = ImageSprite(targtex, shade2d, w=10, h=10, z=0.4)
target.set_2d_size(targtex.ix, targtex.iy, (DISPLAY.width - targtex.ix)/2,
                  (DISPLAY.height - targtex.iy)/2)

#telescopic gun sight
sniptex = Texture("textures/snipermode.png", blend=True)
sniper = ImageSprite(sniptex, shade2d, w=10, h=10, z=0.3)
scx = DISPLAY.width/sniptex.ix
scy = DISPLAY.height/sniptex.iy
if scy > scx:
  scx = scy # enlarge to fill screen but use same scale for both directions
scw, sch = sniptex.ix * scx, sniptex.iy * scx
sniper.set_2d_size(scw, sch, (DISPLAY.width - scw)/2,(DISPLAY.height - sch)/2)

#corner map and dots
smmap = ImageSprite(mountimg1, shade2d, w=10, h=10, z=0.2)
smmap.set_2d_size(w=200, h=200, x=DISPLAY.width - 200, y=DISPLAY.height - 200)
#dot1tex = Texture("textures/red_ball.png")
dot1 = ImageSprite("textures/red_ball.png", shade2d, w=10, h=10, z=0.1)
dot1.set_2d_size(w=10, h=10) # 10x10 pixels
dot2 = ImageSprite("textures/blu_ball.png", shade2d, w=10, h=10, z=0.05)
dot2.set_2d_size(w=10, h=10)

#player tank vars
tankrot = 180.0
turret = 0.0
tankroll = 0.0     #side-to-side roll of tank on ground
tankpitch = 0.0   #too and fro pitch of tank on ground lol catface

#key presses
mymouse = Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()

#position vars
mouserot = 0.0
tilt = 0.0
avhgt = 0.85
xm, oxm = 0.0, -1.0
zm, ozm = -200.0, -1.0
ym = mymap.calcHeight(xm, zm) + avhgt

#enemy tank vars
etx = 120
etz = -120
etr = 0.0

ltm = 0.0 #last pitch roll check
smode = False #sniper mode

def drawTiger(x, y, z, rot, roll, pitch, turret, gunangle, shadows=None):
  tank_body.position(x, y, z)
  tank_body.rotateToX(pitch)
  tank_body.rotateToY(rot-90)
  tank_body.rotateToZ(roll)
  tank_body.draw() if shadows == None else shadows.add_shadow(tank_body)
  tank_turret.position(x, y, z)
  tank_turret.rotateToX(pitch)
  tank_turret.rotateToY(turret-90)
  tank_turret.rotateToZ(roll)
  tank_turret.draw() if shadows == None else shadows.add_shadow(tank_turret)
  tank_gun.position(x, y, z)
  # adjust gunangle for tilted plane as turret rotates
  tank_gun.rotateToX(pitch + math.cos(math.radians(turret - 180)) * gunangle)
  tank_gun.rotateToY(turret-90)
  tank_gun.rotateToZ(roll - math.sin(math.radians(turret - 180)) * gunangle)
  tank_gun.draw() if shadows == None else shadows.add_shadow(tank_gun)


# Update display before we begin (user might have moved window)
win.update()
DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)

is_running = True
CAMERA = Camera.instance()

try:
  while DISPLAY.loop_running():
    mx, my = mymouse.position()
    mouserot -= (mx-omx)*0.2
    tilt += (my-omy)*0.2
    omx=mx
    omy=my

    CAMERA.reset()
    dot1.set_2d_location(DISPLAY.width - 105.0 + 200.0*xm/mapwidth,
                        DISPLAY.height - 105.0 - 200.0*zm/mapdepth)
    dot2.set_2d_location(DISPLAY.width - 105.0 + 200.0*etx/mapwidth,
                        DISPLAY.height - 105.0 - 200.0*etz/mapdepth)
    dot1.draw()
    dot2.draw()
    smmap.draw()
    # tilt can be used to prevent the view from going under the landscape!
    sf = 60 - 55.0 / abs(tilt) if tilt < -1 else 5.0
    xoff = sf * math.sin(math.radians(mouserot))
    yoff = abs(1.25 * sf * math.sin(math.radians(tilt))) + 3.0
    zoff = -sf * math.cos(math.radians(mouserot))

    if tilt > -5 and smode == False: # zoom in
      CAMERA.reset(lens=(1, 1000, 12.5, DISPLAY.width / DISPLAY.height))
      smode = True
    elif tilt <= -5 and smode == True: # zoom out
      CAMERA.reset(lens=(1, 1000, 45, DISPLAY.width / DISPLAY.height))
      smode = False

    #adjust CAMERA position in and out so we can see our tank
    CAMERA.rotate(tilt, mouserot, 0)
    CAMERA.position((xm + xoff, ym + yoff + 5, zm + zoff))
    oxm, ozm = xm, zm

    myshadows.start_cast((xm, -ym, zm))
    #shadows player tank with smoothing on pitch and roll to lessen jerkiness
    tmnow = time.time()
    if tmnow > (ltm + 0.5):
      tankpitch_to, tankroll_to = mymap.pitch_roll(xm, zm)
    tankpitch += (tankpitch_to - tankpitch)/3.0
    tankroll += (tankroll_to - tankroll)/3.0
    drawTiger(xm, ym, zm, tankrot, tankroll, tankpitch, 180 - turret,
          (tilt*-2.0 if tilt > 0.0 else 0.0), shadows=myshadows)

    #shadows enemy tank
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
    drawTiger(etx, ety, etz, etr, roll, pitch, etr, 0, shadows=myshadows)
    myshadows.add_shadow(church)
    myshadows.add_shadow(cottages)
    myshadows.end_cast()

    #Tanks and buildings for real
    drawTiger(xm, ym, zm, tankrot, tankroll, tankpitch, 180 - turret,
          (tilt*-2.0 if tilt > 0.0 else 0.0))
    drawTiger(etx, ety, etz, etr, roll, pitch, etr, 0)
    church.draw()
    cottages.draw()

    #mymap.draw()           # Draw the landscape
    myshadows.draw_shadow()

    myecube.position(xm, ym, zm)
    myecube.draw()  #Draw environment cube

    if smode:
      """ because some of the overlays have blend=True they must be done AFTER
      other objects have been rendered.
      """
      target.draw()
      sniper.draw()

    # turns player tankt turret towards center of screen which will have a crosshairs
    if turret + 2.0 < mouserot:
      turret += 2.0
    if turret - 2.0 > mouserot:
      turret -= 2.0
    """
    if inputs.key_state("BTN_LEFT"):
      xm -= math.sin(math.radians(tankrot)) * 2
      zm -= math.cos(math.radians(tankrot)) * 2
      ym = (mymap.calcHeight(xm, zm) + avhgt)
    if inputs.key_state("KEY_W"):  #key W
      xm -= math.sin(math.radians(tankrot)) * 2
      zm -= math.cos(math.radians(tankrot)) * 2
      ym = (mymap.calcHeight(xm, zm) + avhgt)
    if inputs.key_state("KEY_S"): #key S
      xm += math.sin(math.radians(tankrot)) * 2
      zm += math.cos(math.radians(tankrot)) * 2
      ym = (mymap.calcHeight(xm, zm) + avhgt)
    if inputs.key_state("KEY_A"):  #key A
      tankrot -= 2
    if inputs.key_state("KEY_D"): #key D
      tankrot += 2
    if inputs.key_state("KEY_P"): #key P
      screenshot('TigerTank.jpg')

    elif win.ev == 'resized':
      DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)
      win.resized = False
      # This flag must be reset otherwise no further events will be detected

    win.ev = ''  # Clear the event so it doesn't repeat.

    CAMERA.was_moved = False
    """
    try:
      win.update()
    except Exception as e:
      print("bye,bye2", e)
      DISPLAY.destroy()
      try:
        win.destroy()
      except:
        pass
      mymouse.stop()
      exit()
    if win.ev == "resized":
      print("resized")
      DISPLAY.resize(win.winx, win.winy, win.width, win.height-bord)
      CAMERA.reset((DISPLAY.near, DISPLAY.far, DISPLAY.fov,
                  DISPLAY.width / float(DISPLAY.height)))
      win.resized = False
    if win.ev == "key":
      if win.key == "w":
        xm -= math.sin(math.radians(tankrot)) * 2
        zm -= math.cos(math.radians(tankrot)) * 2
        ym = (mymap.calcHeight(xm, zm) + avhgt)
      if win.key == "s":
        xm += math.sin(math.radians(tankrot)) * 2
        zm += math.cos(math.radians(tankrot)) * 2
        ym = (mymap.calcHeight(xm, zm) + avhgt)
      if win.key == "a":
        tankrot -= 2
      if win.key == "d":
        tankrot += 2
      if win.key == "p":
        screenshot("TigerTank.jpg")
      if win.key == "Escape":
        try:
          print("bye,bye1")
          DISPLAY.destroy()
          try:
            win.destroy()
          except:
            pass
          mymouse.stop()
          exit()
        except:
          pass
    if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
      xm -= math.sin(math.radians(tankrot)) * 2
      zm -= math.cos(math.radians(tankrot)) * 2
      ym = (mymap.calcHeight(xm, zm) + avhgt)
    else:
      win.ev=""  #clear the event so it doesn't repeat

except Exception as e:
  print("bye,bye3", e)
  DISPLAY.destroy()
  try:
    win.destroy()
  except:
    pass
  mymouse.stop()
  exit()
