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

# Setup display and initialise pi3d
display = pi3d.glDisplay()
display.create()   	# x,y,width,height
display.setBackColour(0,0.7,1,1)    		# r,g,b,alpha

# Load textures
coffimg = pi3d.load_texture("Textures/COFFEE.PNG")
patnimg = pi3d.load_texture("Textures/PATRN.PNG")
raspimg = pi3d.load_textureAlpha("Textures/Raspi256x256.png")
	
# Create my cuboid (width, height, depth, x,y,z)
mycuboid = pi3d.create_cuboid(1,1.5,1, 2,0,-7)
    
# Create planes for texturing (width, height, x,y,z)
myplane = pi3d.create_plane(2,2, -2,0,-7)
bkplane = pi3d.create_plane(10,10, 0,0,-12)

# Fetch key presses
mykeys = pi3d.key()
   
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

    #Press ENTER to terminate
    if mykeys.read() == 10:       
		display.destroy()
		break
    
    display.swap_buffers()
    time.sleep(0.01)
