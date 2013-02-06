#!/usr/bin/python

""" A large 3D model with shadows baked into textures
"""
import math, random, time

import demo

from pi3d.constants import *

from pi3d import Display
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape import EnvironmentCube
from pi3d.shape.Model import Model
from pi3d.shape.Sprite import ImageSprite

from pi3d.util.Screenshot import screenshot
from pi3d.util.TkWin import TkWin

from pi3d.Light import Light

from pi3d.events.events import InputEvents, nameOf, codeOf

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window in Display
winw,winh,bord = 1200, 600, 0   	#64MB GPU memory setting
#winw,winh,bord = 1920,1080,0	#128MB GPU memory setting

DISPLAY = Display.create(tk=True, window_title='ConferenceHall demo in Pi3D',
                        w=winw, h=winh - bord, far=2200.0,
                        background=(0.4, 0.8, 0.8, 1), frames_per_second=16)

inputs = InputEvents()
Light((1,-1,1), (1.0, 1.0, 1.0), (0.5, 0.5, 0.5))

win = DISPLAY.tkwin

shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
shade2d = Shader('shaders/2d_flat')

#========================================
# create splash screen and draw it TODO as Temporary measure use Tiger Tank!!!
splash = ImageSprite("textures/tiger_splash.jpg", shade2d, w=10, h=10, z=0.2)
splash.draw()
DISPLAY.swap_buffers()

#############################
ectex = EnvironmentCube.loadECfiles("textures/ecubes/Miramar", "miramar_256", "png", nobottom = True)
myecube = EnvironmentCube.EnvironmentCube(size=1800.0, maptype="FACES",
                                          nobottom=True)
myecube.set_draw_details(flatsh,ectex)

x,z = 0.0, 0.0
y = 0.0

cor_win = Model(file_string="models/ConferenceHall/conferencehall.egg",
                name="Hall", x=x, y=y, z=z, sx=0.1, sy=0.1, sz=0.1)
cor_win.set_shader(shader)

#position vars
mouserot = 0.0
tilt = 0.0
avhgt = 2.3
xm = 0.0
zm = -70.0
ym = 0.0
spc = 39.32
mody = ym
opendist = 80

# Update display before we begin (user might have moved window)
win.update()
DISPLAY.resize(win.winx, win.winy, win.width, win.height - bord)

inputs.get_mouse_movement()
CAMERA = Camera.instance()

while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  CAMERA.reset()

  #update mouse
  inputs.do_input_events()
  mx, my, mv, mh, md = inputs.get_mouse_movement()
  mouserot -= (mx)*0.2
  tilt -= (my)*0.2

  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt < -1: sf = 6 - 5.5/abs(tilt)
  else: sf = 0.5
  xoff = sf*math.sin(mouserot*rads)
  yoff = abs(1.25*sf*math.sin(tilt*rads)) + 3.0
  zoff = -sf*math.cos(mouserot*rads)
  CAMERA.rotate(tilt, mouserot, 0)
  CAMERA.position((xm + xoff, ym + yoff +5, zm + zoff)) 

  cor_win.position(0, mody, -spc*1.5)
  cor_win.draw()

  myecube.position(xm, ym, zm)
  myecube.draw()#Draw environment cube

  if inputs.key_state("BTN_LEFT"):
    xm-=math.sin(mouserot*rads)*2
    zm+=math.cos(mouserot*rads)*2
  if inputs.key_state("KEY_W"):  #key W
    xm-=math.sin(mouserot*rads)*2
    zm+=math.cos(mouserot*rads)*2
  if inputs.key_state("KEY_S"): #key S
    xm+=math.sin(mouserot*rads)*2
    zm-=math.cos(mouserot*rads)*2
  if inputs.key_state("KEY_A"):  #key A
    mouserot -= 2
  if inputs.key_state("KEY_D"): #key D
    mouserot += 2
  if inputs.key_state("KEY_P"): #key P
    screenshot("ConferenceHall.jpg")

  if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
    xm-=math.sin(mouserot*rads)*2
    zm+=math.cos(mouserot*rads)*2

  win.ev=""  #clear the event so it doesn't repeat

inputs.release()
DISPLAY.destroy()
