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
    
    img = pi3d.load_texture("COFFEE.PNG")
    print "texID:",img.texID
    
    # Setup display and initialise pi3d
    display = pi3d.glDisplay()
    display.create(100,100,600,400)
    display.setBackColour(0,0.7,1,1)    

    # Create my cuboid
    mycuboid = pi3d.create_cuboid(1,1.5,1)
    mycuboid.translate(0,0,-5)
    
    # Create plane for texturing
    myplane = pi3d.create_plane(2,2)
    myplane.translate(0,0,-7)
    
    # Display scene and rotate cuboid
    while 1:
	display.clear()
	
        mycuboid.draw()
	mycuboid.rotateIncY( 3 )
	mycuboid.rotateIncX( 1 )
	
	myplane.draw(img.texID)
	
	display.swap_buffers()
        time.sleep(0.01)
