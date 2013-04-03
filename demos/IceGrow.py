#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" An example of making objects change shape by re-creating them inside the while loop
the textures are also offset by a different amount each frame.
"""
from math import sin, cos, radians
from time import time

import demo
import pi3d

DISPLAY = pi3d.Display.create(x=250, y=250, frames_per_second=16)
shader = pi3d.Shader("shaders/uv_reflect")
tex = pi3d.Texture("textures/metalhull.jpg")
bump = pi3d.Texture("textures/rocktile2.jpg")
shine = pi3d.Texture("textures/stars2.jpg")

tetras = [] 
# tetras[n][0] is a Tetrahedron object
# tetras[n][1] is an array of [time, (position tables for each tetrahedron)]
tetras.append([None,[[0.0, ((-0.3,0,-0.1),(0.2,0,-0.2),(-0.1,0,0.3),(-0.2,0,0))],
                    [70.0, ((-0.6,0,-0.2),(0.4,0,-0.4),(-0.2,0,0.6),(-0.6,0.5,1.0))],
                    [150.0, ((-3,0,-1),(2,0,-2),(-1,0,3),(-1.3,0.6,0.5))],
                    [260.0, ((-3,0,-1),(2,0,-2),(-1,0,3),(-2,4.0,0))],
                    [300.0, ((-0.3,0,-0.1),(0.2,0,-0.2),(-0.1,0,0.3),(-0.2,0,0))]]])
tetras.append([None,[[0.0, ((-0.1,0,-0.2),(0.1,0,-0.2),(0,0,0.3),(0,0,0))],
                    [50.0, ((-0.1,0,-0.2),(0.1,0,-0.9),(0,0,0.3),(0,0.5,0))],
                    [150.0, ((-0.1,0,-0.5),(0.4,0,-1.4),(0,0,0.9),(0.4,1,0.4))],
                    [240.0, ((-1,0,-2),(1,0,-2),(0,0,3),(1.5,3,1))],
                    [300.0, ((-0.1,0,-0.2),(0.1,0,-0.2),(0,0,0.3),(0,0,0))]]])
tetras.append([None,[[0.0, ((0,0,-0.1),(0.15,0,-0.1),(0.1,0,0.1),(0.1,0.2,0.0))],
                    [150.0, ((0,0,-1),(1.5,0,-1),(1,0,1),(1,4.2,0))],
                    [200.0, ((0,0,-0.5),(1.5,0,-0.5),(1,0,1),(1,6.2,0))],
                    [300.0, ((0,0,-0.1),(0.15,0,-0.1),(0.1,0,0.1),(0.1,0.2,0.0))]]])

tm = time()
st_tm = tm # start time for this sequence
sc = 0.0 # offset for texture
ds = -0.0001 # offset change per frame
dgrow = 0.1 # time between 'growing' the shapes
nextgrow = 0.0 # time to do next growing
camRad = 4.0 # radius of camera position
mouserot = 0.0 # rotation of camera
tilt = 5.0 # tilt of camera

#key presses
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()

mykeys = pi3d.Keyboard()
CAMERA = pi3d.Camera.instance()

###################################
#function for interpolating vertex values at a given time
###################################
def interpolate(v_arr, tm):
  plast = None
  found_flg = False
  for p in v_arr: # each p is animation data for a tetrahedron
    if p[0] > tm:
      found_flg = True
      pthis = p
      break
    plast = p
  if not found_flg:
    return plast[1]
  else:
    r = (tm - plast[0]) / (pthis[0] - plast[0])
    rval = []
    for i in range(4):
      rval.append([])
      for j in range(3):
        rval[i].append(plast[1][i][j] + r * (pthis[1][i][j] - plast[1][i][j]))
    return tuple(tuple(x) for x in rval)
###################################

# main display loop
while DISPLAY.loop_running():
  tm = time() - st_tm
  mx, my = mymouse.position() # camera can move around object with mouse move
  mouserot -= (mx-omx)*0.2
  tilt -= (my-omy)*0.1
  omx=mx
  omy=my
  CAMERA.reset()
  CAMERA.rotate(-tilt, mouserot, 0)
  CAMERA.position((camRad * sin(radians(mouserot)) * cos(radians(tilt)), 
                   camRad * sin(radians(tilt)), 
                   -camRad * cos(radians(mouserot)) * cos(radians(tilt))))

  for tetra in tetras:
    #as moving slowly only need to regenerate shapes now and then
    if tm  > nextgrow: #need to make sure this happens first time round loop!
      tetra[0] = pi3d.Tetrahedron(x=0.0, y=0.0, z=0.0, 
          corners=interpolate(tetra[1], tm))
      tetra[0].set_draw_details(shader,[tex, bump, shine], 1.0, 0.4)
        
    tetra[0].set_offset((0.0, sc))
    tetra[0].draw()

  if tm  > nextgrow: # can't do this inside the tetra for loop otherwise only first one updated
    nextgrow += dgrow

  if tm > 305.0:
    st_tm = time()
    nextgrow = 0.0
    tm = 0.0

  sc = (sc + ds) % 10.0 # increase the offset

  if mykeys.read() == 27:
    mykeys.close()
    mymouse.stop()
    DISPLAY.destroy()
    break
