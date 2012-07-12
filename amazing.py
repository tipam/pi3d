# Maze with water example using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman, Paddy Gaunt
# Version 0.01 - 12Jul12
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

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1600,800, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha

# Load textures
rockimg = pi3d.loadTexture("textures/rock1.jpg")
secretimg = pi3d.loadTexture("textures/maze1.jpg")
tree2img = pi3d.loadTextureAlpha("textures/tree2.png")
raspimg = pi3d.loadTextureAlpha("textures/Raspi256x256.png")

ectex = pi3d.loadTexture("textures/SkyBox.png")
myecube = pi3d.createEnvironmentCube(900.0,"CROSS")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mymap = pi3d.createElevationMapFromTexture("textures/maze1.jpg",mapwidth,mapdepth,mapheight,128,128,64) #testislands.jpg

myfog = pi3d.fog(0.05, (0.1,0.1,0.1,1.0)) 

secretmap = pi3d.createPlane(mapwidth, mapdepth)
secretmap.rotateToX(-90.0)
secretmap.position(0, -50, 0)

# water cards
wimg = []
iFiles = glob.glob("textures/water/water???.png")
iFiles.sort() # order is vital to animation!
for f in iFiles:
    wimg.append(pi3d.loadTextureAlpha(f))
nImg = len(wimg)

tSize = 5.0
wTile = pi3d.createPlane(tSize, tSize, "water")

water = pi3d.createMergeShape("water")
for k in range(7):
    for j in range(7):
	water.add(wTile, (k-3.5)*tSize, 0, (j-3.5)*tSize, -90,0,0)

#Create tree models
treeplane = pi3d.createPlane(4.0,5.0)

treemodel1 = pi3d.createMergeShape("baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.createMergeShape("trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,900.0,900.0,30,"",8.0,3.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)
raspberry = pi3d.createMergeShape("rasp")
raspberry.cluster(treemodel1, mymap,0.0,0.0,990.0,990.0,10,"",8.0,1.0)

light = pi3d.createLight(0, 10,10,10, "", 50,100,0)
light.on()

#screenshot number
scshots = 1

#energy counter
hp = 50
wLevel = -1.0

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)
lastX0=0.0
lastZ0=0.0

# Fetch key presses
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y
mxMin, mxMax, myMin, myMax = omx, omx, omy, omy

i = 0 #water surface image index
lastTm = time.time()
dt = 0.1 #time between frames for water
m = pi3d.matrix()
# Display scene and rotate cuboid
while 1:
    display.clear()
    
    pi3d.identity()
    pi3d.rotate(tilt,0,0)
    pi3d.rotate(0,rot,0)
    pi3d.position(xm,ym,zm)
    
    myecube.draw(ectex,xm,ym,zm)
    myfog.enable()
    mymap.draw(rockimg)
    mytrees1.drawAll(tree2img)
    raspberry.drawAll(raspimg)

    x0 = tSize * math.floor((xm -9.0*math.sin(rot*rads))/tSize)
    z0 = tSize * math.floor((zm + 9.0*math.cos(rot*rads))/tSize)
    m.push()
    if x0 != lastX0 or z0 != lastZ0:
	water.position(-x0, wLevel, -z0)
	lastX0 = x0
	lastZ0 = z0
    water.drawAll(wimg[i])
    m.pop()
    myfog.disable()
    #secretmap.draw(secretimg)
    
    nowTm = time.time()
    if (nowTm - lastTm) > dt:
        i = (i + 1) % nImg
	if wLevel < 1.5: wLevel += 0.005
        lastTm = nowTm

    mx=mymouse.x
    my=mymouse.y
    if mx > mxMax: mxMax = mx
    if mx < mxMin: mxMin = mx
    if my > myMax: myMax = my
    if my < myMin: myMin = my
    
    #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
    rot += (mx-(mxMax + mxMin)/2.0)*0.004 + (mx - omx)*0.2
    tilt -= (my-(mxMax + mxMin)/2.0)*0.004 + (my - omy)*0.2
    omx=mx
    omy=my

    #Press ESCAPE to terminate
    k = mykeys.read()
    if k >-1:
        if k==119: #key W
	    dx = -math.sin(rot*rads)
	    dz = math.cos(rot*rads)
	    dy = -(mymap.calcHeight(xm + dx, zm + dz)+avhgt) - ym
	    if dy > -0.5:
		xm += dx
		zm += dz
		ym += dy
        elif k==115: #kry S
	    dx = math.sin(rot*rads)
	    dz = -math.cos(rot*rads)
	    dy = -(mymap.calcHeight(xm + dx, zm + dz)+avhgt) - ym
	    if dy > -0.5:
		xm += dx
		zm += dz
		ym += dy
        elif k==39: #key '
            tilt -= 2.0
            print tilt
        elif k==47: #key /
	    tilt += 2.0
        elif k==97: #key A
	    rot -= 2
        elif k==100: #key D
	    rot += 2
        elif k==112: #key P
	    display.screenshot("critters3D"+str(scshots)+".jpg")
	    scshots += 1
        elif k==32 and hp > 0: #key SPACE
	    dx = -math.sin(rot*rads)*5.0
	    dz = math.cos(rot*rads)*5.0
	    dy = -(mymap.calcHeight(xm + dx, zm + dz)+avhgt) - ym
	    xm += dx
	    zm += dz
	    ym += dy
	    hp -= 1
        elif k==27: #Escape key
            display.destroy()
            mykeys.close()
            break
        #else:
	    #print k
   
    display.swapBuffers()
