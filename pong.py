# Ponh using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman, Paddy Gaunt
# Version 0.02 - 20Aug12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
# $ sudo apt-get install python-imaging
#
# before running this example
#

import pi3d,math,random,glob,time

rads = 0.017453292512 # degrees to radians

#helpful messages
print "############################################################"
print "Mouse to move left and right"
print "############################################################"
print

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(10,10,1200,900, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha

# Load textures
texs=pi3d.textures()
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'rockimg2.blend = False')
groundimg = texs.loadTexture("textures/pong2.jpg")
monstimg = texs.loadTexture("textures/pong3.png")
# environment cube
ectex = texs.loadTexture("textures/ecubes/skybox_stormydays.jpg")
myecube = pi3d.createEnvironmentCube(900.0,"CROSS")
#ball
radius = 1
ball = pi3d.createSphere(radius,12,12,0.0,"sphere",-4,2,-7)
#monster
monster = pi3d.createPlane(5.0, 5.0, "monster", 0,0,0, 0,0,0)
# Create elevation map
mapwidth=50.0                              
mapdepth=50.0
maphalf=20.0
mapheight=20.0
mymap = pi3d.createElevationMapFromTexture("textures/pong.jpg",mapwidth,mapdepth,mapheight,128,128,2,"sub",0,0,0, smooth=False)
# lighting. The default light is a point light but I have made the position method capable of creating
# a directional light and this is what I do inside the loop. If you want a torch you don't need to move it about
light = pi3d.createLight(0, 2, 2, 1, "", 0,1,2, 0.1,0.1,0.2) #yellowish 'torch' or 'sun' (could be blueish ambient with different env cube)
light.on()

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym=mapheight
lastX0=0.0
lastZ0=0.0

#sphere loc and speed
sx, sy, sz = 0, 5, 0
dsx, dsy, dsz = 0.1, 0.0, -0.1
gravity = 0.02
#monster loc and speed
rx, ry, rz = 0, 0, -maphalf
drx, dry, drz = 0, 0, 0
max_speed = 0.05

# Fetch key presses
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

lastTm = time.time()
m = pi3d.matrix()
fly = False
walk = False
# Display scene and rotate cuboid
angle = 0
light.position(1, 1, 1, 0)
while 1:
    display.clear()
    
    pi3d.identity()
    pi3d.position(xm,-2+ym-mapheight,-maphalf-radius)
    
    myecube.draw(ectex,xm,ym,zm)
    mymap.draw(groundimg)
    
    monster.draw(monstimg)
    ball.draw(groundimg)
    
    #monster movement
    
    drx = sx - rx
    if abs(drx) > max_speed: drx = drx/abs(drx) * max_speed
    dry = sy - ry
    if abs(dry) > max_speed: dry = dry/abs(dry) * max_speed
    rx += drx
    ry += dry
    
    monster.position(rx, ry, -maphalf)
    
    dsy -= gravity
    sx += dsx
    sy += dsy
    sz += dsz
    grndy = mymap.calcHeight(sx, sz)
    # bouncing physics
    if sy < grndy + 2*radius: 
		# find map height one unit N and E to get two vectors on surace at 90 degree
		y_a = mymap.calcHeight(sx+1, sz) - grndy
		y_b = mymap.calcHeight(sx, sz+1) - grndy
		# get the cross product of these two tangen vectors to create normal vector
		nx = y_a
		ny = -1
		nz = y_b
		# renormalise normal vector!
		nfact = math.sqrt(nx*nx + ny*ny + nz*nz)
		nx, ny, nz = nx/nfact, ny/nfact, nz/nfact
		# use R = I - 2(N.I)N
		rfact = 2*(nx*dsx + ny*dsy + nz*dsz)
		dsx, dsy, dsz = dsx - rfact*nx, dsy - rfact*ny, dsz - rfact*nz
		if dsx > 0.3: dsx = 0.2
		if dsz > 0.3: dsz = 0.2
		print dsx,
		sy = grndy + 2*radius
    # bounce off edges
    if sx > maphalf: dsx = -1 * abs(dsx) * (1 + random.random())
    if sx < -maphalf: dsx = abs(dsx)
    
    if sz > maphalf: dsz = -1 * abs(dsz) * (1 + random.random())
    if sz < -maphalf: dsz = abs(dsz)
    
    ball.position(sx, sy, sz)
    ball.rotateIncX(dsx*-10)
    ball.rotateIncZ(dsz*-10)

    mx=mymouse.x
    dx = -(mx-omx)*0.02
    omx=mx
    if ((xm >= (-1*maphalf) and dx < 0) or (xm <= maphalf and dx > 0)):  xm += dx

    my=mymouse.y
    dy = -(my-omy)*0.01
    omy=my
    if ((ym >= (0) and dy < 0) or (ym <= mapheight and dy > 0)):  ym += dy

    #Press ESCAPE to terminate
    k = mykeys.read()
    if k==27: #Escape key
		display.destroy()
		mykeys.close()
		break
  
    display.swapBuffers()
