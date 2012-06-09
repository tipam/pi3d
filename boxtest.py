# Rotating box example using pi3d module
# ======================================
#
# Copyright (c) 2012 - Tim Skillman
# 
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#

import time
import pi3d

if __name__ == "__main__":
    
    # Setup display and initialise pi3d
    display = pi3d.init()
    display.create(100,100,600,400)
    display.setBackColour(0,0.7,1,1)    

    # Create my cuboid
    mycuboid = pi3d.create_cuboid(1,1.5,1)
    mycuboid.translate(0,0,-5)
    
    # Display scene and rotate cuboid
    while 1:
	display.clear()
	
        mycuboid.draw()
	mycuboid.rotateIncY( 3 )
	mycuboid.rotateIncX( 1 )
	
	display.swap_buffers()
        time.sleep(0.01)
