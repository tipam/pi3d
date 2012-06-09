# Rotating box example using pi3d module
#
# Copyright (c) 2012 - Tim Skillman
# 

import time, math, random, pymouse, pi3d

# Define rotation variables
rotx = 0
roty = 0

if __name__ == "__main__":
    display = pi3d.init()
    display.create(100,100,600,400)
    display.setBackColour(0,0.7,1,1)    

    #Create my own cuboid
    mycuboid = pi3d.create_cuboid(1,1.5,1)
    mycuboid.translate(0,0,-5)
    
    #display scene
    while 1:
	display.clear()
	
        mycuboid.draw()
	
	mycuboid.rotatey(roty)
	roty += 3
	mycuboid.rotatex(rotx)
	rotx += 1
	
	display.swap_buffers()
        time.sleep(0.01)
