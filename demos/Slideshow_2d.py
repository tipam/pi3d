#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
"""This demo shows the use of the Canvas shape for 2D drawing. Also threading
is used to allow the file access to be done in the background. Textures are 
held in an array (5 long) so that the next, or previous (key s) image appears
instantly
"""
import random, time, glob, threading

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture
from pi3d.Camera import Camera
from pi3d.Shader import Shader
from pi3d.shape.Canvas import Canvas

print("#########################################################")
print("press ESC to escape, S to go back, any key for next slide")
print("#########################################################")

# Setup display and initialise pi3d
DISPLAY = Display.create(background=(0.0, 0.0, 0.0, 0.0), x=100, y=100)
shader = Shader("shaders/2d_flat")
#############################
slide = [None]*5
sz = [None]*5
iFiles = glob.glob("textures/*.jpg")
nFiles = len(iFiles)

def tex_load(fname, j, slide, sz):
  """ here the images are scaled to fit the Display size, if they were to be
  rendered pixel for pixel as the original then the mipmap=False argument would
  be used, which is faster, and w and h values set to the Texture size i.e.

  tex = Texture(f, mipmap=False)
  ...
  wi, hi = tex.ix, tex.iy

  NB if some textures are set with different values of mipmap then the last one
  loaded will define how the global behaviour is set. Arguments:
  
    *fname*
      path and name of the texture image file to load
    *j*
      the position in the buffer arrays (slide and sz) use
  """
  tex = Texture(fname)
  slide[j] = tex
  xrat = DISPLAY.width/tex.ix
  yrat = DISPLAY.height/tex.iy
  if yrat < xrat:
    xrat = yrat
  wi, hi = tex.ix * xrat, tex.iy * xrat
  xi = (DISPLAY.width - wi)/2
  yi = (DISPLAY.height - hi)/2
  sz[j] = [wi, hi, xi, yi]

for i in range(5):
  thr = threading.Thread(target=tex_load,
                        args=(iFiles[(i+nFiles-1)%nFiles], i, slide, sz))
  thr.daemon = True #allows the program to exit even if a Thread is still running
  thr.start()
  if i > 3:
    thr.join() #makes the main thread wait so the loop doesn't start too early!

# Setup sprite
""" Canvas is just the Shape to draw the 2d onto, it needs to be bigger
than the screen, that's all. z value will be used as depth by the shader
as it decides what to draw and what to discard """
canvas = Canvas()
canvas.set_shader(shader)

i = 1
canvas.set_texture(slide[i])
canvas.set_2d_size(w=sz[i][0], h=sz[i][1], x=sz[i][2], y=sz[i][3])
i += 1

# Fetch key presses
mykeys = Keyboard()
CAMERA = Camera.instance()
CAMERA.was_moved = False #to save a tiny bit of work each loop

while DISPLAY.loop_running():
  canvas.draw()

  k = mykeys.read()
  if k >-1:
    d1, d2 = 2, 3
    if k==27: #ESC
      mykeys.close()
      DISPLAY.stop()
      break
    if k==115: #S go back a picture, not quite right but you can sort out why!
      i -= 2
      d1, d2 = -2, -1
    #all other keys load next picture
      
    canvas.set_texture(slide[i%5])
    canvas.set_2d_size(w=sz[i%5][0], h=sz[i%5][1], x=sz[i%5][2], y=sz[i%5][3])
    thr = threading.Thread(target=tex_load,
                          args=(iFiles[(i+nFiles+d1)%nFiles], (i+d2)%5, slide, sz))
    thr.daemon = True
    thr.start()
    i += 1
    
