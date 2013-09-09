#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

""" PostProcess. The rendered scene can be processed by the
shader passed to the PostProcess class. The PostProcess.draw() method can
have a dict of unif keys and variable passed to it which can then be used
by the shader to create dynamic effects
"""
import math, random, time
from subprocess import Popen, PIPE, STDOUT

import demo
import pi3d

print("shapes change with mouse movement!")
# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=40,
          mouse=True)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

persp_cam = pi3d.Camera.instance() # default instance camera perspecive view

#setup textures, light position and initial model position
pi3d.Light((0, 5, 0))
#create shaders
shader = pi3d.Shader("star")
flatsh = pi3d.Shader("uv_flat")
post = pi3d.PostProcess("post_base1")

#Create textures
shapeimg = pi3d.Texture("textures/straw1.jpg")
shapebump = pi3d.Texture("textures/floor_nm.jpg", True)

#Create shape
myshape = pi3d.MergeShape(camera=persp_cam) #specify perspective view
asphere = pi3d.Sphere(sides=32, slices=32)
myshape.radialCopy(asphere, step=72)
myshape.position(0.0, 0.0, 5.0)
myshape.set_draw_details(shader, [shapeimg], 8.0, 0.1)

mysprite = pi3d.Sprite(w=10.0, h=10.0, camera=persp_cam)
mysprite.position(0.0, 0.0, 15.0)
mysprite.set_draw_details(flatsh, [shapebump])

# Fetch key presses.
mykeys = pi3d.Keyboard()
tm = 0.0
dt = 0.02
sc = 0.0
ds = 0.001
x = 0.0
dx = 0.001

p = Popen(['mpg321', '-R', '-F', 'testPlayer'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p.stdin.write('LOAD 05Kids.mp3\n')
rgb = {48:0.0, 49:0.0, 50:0.0}

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
  for i in range(11):
    l = p.stdout.readline()
  if b'FFT' in l:
    val_str = l.split()
    rgb[48] = float(val_str[2]) / 127.0
    rgb[49] = float(val_str[6]) / 127.0
    rgb[50] = float(val_str[10]) / 127.0
  post.draw(rgb)

  mx, my = DISPLAY.mouse.position()
  myshape.scale(1.0 + mx/1000.0, 1.0 + my/1000.0, 1.0 + mx/1000.0)
  myshape.rotateIncY(0.6471)
  myshape.rotateIncX(0.0613)

  k = mykeys.read()
  if k==112:
    pi3d.screenshot("post.jpg")
  elif k==27:
    p.stdin.write('QUIT\n')
    mykeys.close()
    DISPLAY.destroy()
    break

p.stdin.write('QUIT\n')
