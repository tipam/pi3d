# Bouncing balls example using pi3d module
# ========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 03Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#
# Bouncing demonstrates pi3d sprites over the desktop.
# It uses the orthographic view scaled to the size of the window;
# this means that sprites can be drawn at pixel resolution
# which is more common for 2D.  Also demonstrates a mock title bar.

import sys, random

from pi3d import Draw

from pi3d.Ball import Ball
from pi3d.Display import Display
from pi3d.Key import Key
from pi3d.Texture import Textures

# Setup display and initialise pi3d
display = Display()
scnx=display.max_width
scny=display.max_height
display.create2D(0,0,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.6,0)


# Ball parameters
maxballs = 15
maxballsize = 100
minballsize = 5
maxspeed = 30

texs=Textures()
balltex = []
balltex.append(texs.loadTexture("textures/red_ball.png"))
balltex.append(texs.loadTexture("textures/grn_ball.png"))
balltex.append(texs.loadTexture("textures/blu_ball.png"))

#create balls and positions and make sure they don't touch to start with
balls = []
b=0
hit = True
for b in range (0,maxballs):

    r = random.random() * maxballsize+minballsize
    x = random.random() * scnx
    y = random.random() * scny

    vx = random.random() * 20.0-10.0
    vy = random.random() * 20.0-10.0
    balls.append(Ball(r,x,y,vx,vy,0.0))
    c=0
    hit = False
    while c < b and not hit:
      Bb = balls[b]
      if Bb.hit(balls[c]):
        Bb.radius = random.random() * maxballsize + minballsize
        Bb.x = random.random() * scnx
        Bb.y = random.random() * scny
        c=0
        hit = True
      else:
        c+=1
        hit = False


# Fetch key presses
mykeys = Key()
scshots = 1

print balls[0].x, balls[0].vx

while True:
  display.clear()

  for b in range (0,len(balls)):
    Bb = balls[b]
    #check collisions with other balls and bounce if necessary
    for c in range (b+1,len(balls)):
      Bb.collisionBounce(balls[c])
    Bb.x += Bb.vx
    Bb.y += Bb.vy
    #check if ball hits wall (to avoid getting stuck just off the edge)
    if Bb.x > (scnx - Bb.radius): Bb.vx = -abs(Bb.vx)
    elif Bb.x < Bb.radius: Bb.vx = abs(Bb.vx)
    if Bb.y > (scny - Bb.radius): Bb.vy = -abs(Bb.vy)
    elif Bb.y < Bb.radius: Bb.vy = abs(Bb.vy)

    Draw.sprite(balltex[0], Bb.x, Bb.y, -1, Bb.radius, Bb.radius)

  k = mykeys.read()
  if k >-1:
    if k==27:  #ESCAPE key
      mykeys.close()
      texs.deleteAll()
      display.destroy()
      break
    if k==112:
      display.screenshot("collisionballs.jpg")

  display.swapBuffers()
