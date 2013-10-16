#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Music and animation with changing images. Needs some mp3 files in the
music subdirectory and mpg321 installed
"""
import math, random, time, glob, threading
from subprocess import Popen, PIPE, STDOUT

import demo
import pi3d

def _tex_load(tex_list, slot, fName):
  tex_list[slot] = pi3d.Texture(fName)
  
# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=40)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

#persp_cam = pi3d.Camera.instance() # default instance camera perspecive view

#setup textures, light position and initial model position
pi3d.Light((0, 5, 0))
#create shaders
shader = pi3d.Shader("star")
flatsh = pi3d.Shader("uv_flat")
post = pi3d.PostProcess("shaders/filter_outline")

#Create textures
tFiles = glob.glob("textures/*.*")
nTex = len(tFiles)
slot = 0
tex_list = [pi3d.Texture(tFiles[slot]), None] #ensure first texture there
slot = 1
#next texture load in background
t = threading.Thread(target=_tex_load, args=(tex_list, slot % 2, tFiles[slot % nTex]))
t.daemon = True
t.start()

#Create shape
myshape = pi3d.MergeShape()
asphere = pi3d.Sphere(sides=32, slices=32)
myshape.radialCopy(asphere, step=72)
myshape.position(0.0, 0.0, 5.0)
myshape.set_draw_details(shader, [tex_list[0]], 8.0, 0.1)

mysprite = pi3d.Sprite(w=15.0, h=15.0)
mysprite.position(0.0, 0.0, 15.0)
mysprite.set_draw_details(flatsh, [tex_list[0]])

# Fetch key presses.
mykeys = pi3d.Keyboard()
pic_next = 5.0
pic_dt = 5.0
tm = 0.0
dt = 0.02
sc = 0.0
ds = 0.001
x = 0.0
dx = 0.001

mFiles = glob.glob("music/*.mp3")
random.shuffle(mFiles)
nMusic = len(mFiles)
iMusic = 0

p = Popen(['mpg321', '-R', '-F', 'testPlayer'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p.stdin.write(b'LOAD ' + mFiles[iMusic] + b'\n')
rgb = {48:0.0, 49:0.0, 50:0.0}
mx, my = 1.0, 1.0
dx, dy = 1.0, 1.0
# Display scene and rotate shape
while DISPLAY.loop_running():
  tm = tm + dt
  sc = (sc + ds) % 10.0
  myshape.set_custom_data(48, [tm, sc, -0.5 * sc])
  post.start_capture()
  # 1. drawing objects now renders to an offscreen texture ####################

  mysprite.draw()
  myshape.draw()

  post.end_capture()
  # 2. drawing now back to screen. The texture can now be used by post.draw()

  # 3. redraw these two objects applying a shader effect ###############
  #read several lines so the video frame rate doesn't restrict the music
  #TODO ought to be a better way of doing this.
  for i in range(11):
    l = p.stdout.readline()
    if b'@P' in l:
      iMusic = (iMusic + 1) % nMusic
      p.stdin.write(b'LOAD ' + mFiles[iMusic] + b'\n')
  if b'FFT' in l: #frequency analysis
    val_str = l.split()
    rgb[48] = float(val_str[2]) / 115.0
    rgb[49] = float(val_str[6]) / 115.0
    rgb[50] = float(val_str[10]) / 115.0
  post.draw(rgb)

  if mx > 3.0:
    dx = -1.0
  elif  mx < 0.0:
    dx = 1.0
  if my > 5.0:
    dy = -1.0
  elif  my < 0.0:
    dy = 1.0
  mx += dx * rgb[49] / 100.0
  my += dy * rgb[50] / 50.0 
  myshape.scale(mx, my, mx)
  myshape.rotateIncY(0.6471 + rgb[48])
  myshape.rotateIncX(0.513 - rgb[50])
  mysprite.rotateIncZ(0.5)

  if tm > pic_next:
    """change the pictures and start a thread to load into tex_list"""
    pic_next += pic_dt
    myshape.set_draw_details(shader, [tex_list[slot % 2]])
    mysprite.set_draw_details(flatsh, [tex_list[slot % 2]])
    slot += 1
    t = threading.Thread(target=_tex_load, args=(tex_list, slot % 2, tFiles[slot % nTex]))
    t.daemon = True
    t.start()


  k = mykeys.read()
  if k==112:
    pi3d.screenshot("post.jpg")
  elif k==27:
    mykeys.close()
    DISPLAY.destroy()
    break

p.stdin.write(b'QUIT\n')
