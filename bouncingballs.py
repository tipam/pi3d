# Bouncing balls example using pi3d module
# ========================================
# Copyright (c) 2012 - Tim Skillman
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

import pi3d, sys, random, array

# Setup display and initialise pi3d
scnx=800
scny=600
display = pi3d.glDisplay()
display.create(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.8,1)    	
    
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

ball = []
ball.append(pi3d.load_textureAlpha("Textures/red_ball.png"))
ball.append(pi3d.load_textureAlpha("Textures/grn_ball.png"))
ball.append(pi3d.load_textureAlpha("Textures/blu_ball.png"))
bar = pi3d.load_texture("Textures/bar.png")
bbtitle = pi3d.load_textureAlpha("Textures/pi3dbbd.png")

camera = pi3d.camera()
camera.orthographic(0, scnx, 0, scny)

while True:
	
    display.clear()
	
    for b in range (0, maxballs):
			    
	# Draw ball (tex,x,y,z,width,height,rotation)
	pi3d.sprite(ball[bi[b]],bx[b],by[b],-1,bs[b],bs[b])
	
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
    pi3d.rectangle(bar,0,scny-32,scnx,32)
    pi3d.rectangle(bbtitle,5,scny-32,256,32)
    
    display.swap_buffers()
