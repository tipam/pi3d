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
DISPLAY = Display.create(background=(0.1, 0.1, 0.1, 0.9), x=100, y=100)
shader = Shader("shaders/2d_flat")
#############################
slide = [None]*5
sz = [None]*5
iFiles = glob.glob("textures/*.*")
nFiles = len(iFiles)
queue = []
thr = None #to use for thread

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
  thr.join() #makes the main thread wait so the loop doesn't start too early!

# Setup sprite
""" Canvas is just the Shape to draw the 2d onto, it needs to be bigger
than the screen, that's all. z value will be used as depth by the shader
as it decides what to draw and what to discard """
canvas = Canvas()
canvas.set_shader(shader)
canvas_bk = Canvas()
canvas_bk.set_shader(shader)
canvas_bk.positionZ(0.1)

i = 0
canvas_bk.set_texture(slide[i])
canvas_bk.set_2d_size(w=sz[i][0], h=sz[i][1], x=sz[i][2], y=sz[i][3])
i += 1
canvas.set_texture(slide[i])
canvas.set_2d_size(w=sz[i][0], h=sz[i][1], x=sz[i][2], y=sz[i][3])
i += 1

# Fetch key presses
mykeys = Keyboard()
CAMERA = Camera.instance()
CAMERA.was_moved = False #to save a tiny bit of work each loop

while DISPLAY.loop_running():
  canvas_bk.draw()
  canvas.draw()
  ca = canvas.alpha()
  if ca < 1.0:
    canvas.set_alpha(ca + 0.01)
    canvas_bk.set_alpha(1.0)

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
      
    canvas_bk.set_texture(slide[(i-1)%5])
    canvas_bk.set_2d_size(w=sz[(i-1)%5][0], h=sz[(i-1)%5][1], x=sz[(i-1)%5][2],
                          y=sz[(i-1)%5][3])
    canvas_bk.set_alpha(1.0)
    canvas.set_texture(slide[i%5])
    canvas.set_2d_size(w=sz[i%5][0], h=sz[i%5][1], x=sz[i%5][2], y=sz[i%5][3])
    canvas.set_alpha(0.0)

    queue.append([iFiles[(i+nFiles+d1)%nFiles], (i+d2)%5])
    i += 1
  
  if len(queue) > 0 and not (thr.isAlive()):
    ix = queue.pop(0)
    thr = threading.Thread(target=tex_load, args=(ix[0], ix[1], slide, sz))
    thr.daemon = True
    thr.start()
