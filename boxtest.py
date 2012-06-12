# Rotating box example using pi3d module
# ======================================
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

import time
import pi3d

if __name__ == "__main__":
    
    # Setup display and initialise pi3d
    display = pi3d.glDisplay()
    display.create(100,100,1200,800)
    display.setBackColour(0,0.7,1,1)    

    # Load textures
    coffimg = pi3d.load_texture("COFFEE.PNG")
    patnimg = pi3d.load_texture("PATRN.PNG")
    raspimg = pi3d.load_textureAlpha("Raspi256x256.png")
	
    # Create my cuboid
    mycuboid = pi3d.create_cuboid(1,1.5,1)
    mycuboid.translate(2,0,-7)
    
    # Create plane for texturing
    myplane = pi3d.create_plane(2,2)
    myplane.translate(-2,0,-7)

    bkplane = pi3d.create_plane(10,10)
    bkplane.translate(0,0,-12)
    
    #Create a light (0), its colour and position ...
    #mylight = pi3d.light(0, 1,1,1, 3,3,-50)
    #mylight.on()
    
    # Display scene and rotate cuboid
    while 1:
	display.clear()

	bkplane.draw(coffimg)
	bkplane.rotateIncZ(-0.02)

	myplane.draw(raspimg)
	myplane.rotateIncZ(0.5)

	mycuboid.draw(patnimg)
	mycuboid.rotateIncY( 1 )
	mycuboid.rotateIncX( 0.2 )

	display.swap_buffers()
        time.sleep(0.01)
