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

import pi3d, sys, random, array

# Setup display and initialise pi3d
scnx=1920
scny=1200
display = pi3d.display()
display.create2D(0,0,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.6,0)    	
    

# Ball parameters
maxballs = 15
maxballsize = 150
minballsize = 5
maxspeed = 30

texs=pi3d.textures()
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
    balls.append(pi3d.ball(r,x,y,vx,vy,0.0))
    c=0
    hit = False
    while c<b and not hit:
	if balls[b].hit(balls[c]): 
	    balls[b].r=random.random() * maxballsize+minballsize
	    balls[b].x=random.random() * scnx
	    balls[b].y=random.random() * scny
	    c=0
	    hit = True
	else:
	    c+=1
	    hit = False
	

# Fetch key presses
mykeys = pi3d.key()
scshots = 1

print balls[0].x, balls[0].vx

while True:
    display.clear()
    
    for b in range (0,len(balls)):
	#if balls[b].vx<>0.0 or balls[b].vy<>0.0:
	    #check collisions with other balls and bounce if necessary
	for c in range (b+1,len(balls)):
	    balls[b].collisionBounce(balls[c])
	balls[b].x += balls[b].vx
	balls[b].y += balls[b].vy
	#check if ball hits wall
	if balls[b].x>scnx or balls[b].x<0.0: balls[b].vx = -balls[b].vx
	if balls[b].y>scny or balls[b].y<0.0: balls[b].vy = -balls[b].vy
		
	pi3d.sprite(balltex[0],balls[b].x,balls[b].y,-1,balls[b].radius,balls[b].radius)

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
