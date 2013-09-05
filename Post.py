#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

""" PostProcess. The rendered scene can be processed by the
shader passed to the PostProcess class. The PostProcess.draw() method can
have a dict of unif keys and variable passed to it which can then be used
by the shader to create dynamic effects
"""
import math, random, time

import demo
import pi3d

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=10, y=10, w=800, h=800, frames_per_second=40)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

persp_cam = pi3d.Camera.instance() # default instance camera perspecive view

#setup textures, light position and initial model position
pi3d.Light((0, 5, 0))
#create shaders
shader = pi3d.Shader("star")
flatsh = pi3d.Shader("uv_flat")
post = pi3d.PostProcess()

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
  x = (x + dx) % 5.0
  post.draw({48:(2.0 + x)})

  myshape.rotateIncY(0.247)
  myshape.rotateIncX(0.0613)

  k = mykeys.read()
  if k==112:
    pi3d.screenshot("post.jpg")
  elif k==27:
    mykeys.close()
    DISPLAY.destroy()
    break
