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

from pi3d.Display import Display
from pi3d.Key import Key
from pi3d.Texture import Textures

from pi3d.util import Draw

# Setup display and initialise pi3d
scnx=800
scny=600
display = Display()
display.create2D(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.6,1)

# Ball parameters
maxballs = 40
maxballsize = 60
minballsize = 30
maxspeed = 30

# Ball x,y position
bx=[]
by=[]

# Ball direction vector
dx=[]
dy=[]

# Ball size (scale), ball image reference
bs=[]
bi=[]

# Setup ball positions, sizes, directions and colours
for b in range (0, maxballs):
    bx.append(random.random() * scnx)
    by.append(random.random() * scny)
    dx.append((random.random() - 0.5) * maxspeed)
    dy.append((random.random() - 0.5) * maxspeed)
    bs.append(random.random() * maxballsize + minballsize)
    bi.append(int(random.random() * 3))

texs = Textures()
ball = []
ball.append(texs.loadTexture("textures/red_ball.png"))
ball.append(texs.loadTexture("textures/grn_ball.png"))
ball.append(texs.loadTexture("textures/blu_ball.png"))
bar = texs.loadTexture("textures/bar.png")
bbtitle = texs.loadTexture("textures/pi3dbbd.png",True)

# Fetch key presses
mykeys = Key()
scshots = 1

while True:

    display.clear()

    for b in range (0, maxballs):

	# Draw ball (tex,x,y,z,width,height,rotation)
	Draw.sprite(ball[bi[b]],bx[b],by[b],-2.0,bs[b],bs[b])

	# Increment ball positions
	bx[b]=bx[b]+dx[b]
	by[b]=by[b]+dy[b]

	# X coords outside of drawing area?  Then invert X direction
	if bx[b]>scnx or bx[b]<0:
		dx[b]=-dx[b]

	# Y coords outside of drawing area?  Then invert Y direction
	if by[b]>scny or by[b]<0:
		dy[b]=-dy[b]

    #draw a bar at the top of the screen
    Draw.rectangle(bar,0,scny,scnx,32)
    Draw.rectangle(bbtitle,5,scny,256+5,32)

    k = mykeys.read()
    if k >-1:
	if k==112:
	    display.screenshot("screen3D"+str(scshots)+".jpg")
	    scshots += 1
	if k==27:
		mykeys.close()
		texs.deleteAll()
		display.destroy()
		break

    display.swapBuffers()
