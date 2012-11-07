# Maze with water example using pi3d module
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
print "Esc to quit, W to go forward, Mouse to steer, Space to jump."

print "N.B. W now works as a TOGGLE one press to go one to stop."

print "At the edge you will turn into a ghost and be able to fly "
print "and pass through rocks! There are limited numbers of jumps."
print "Good turnings are often greener and tend to be near"
print "(but in the opposite direction to) big holes"
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
rockimg1 = texs.loadTexture("textures/techy1.jpg")
rockimg2 = texs.loadTexture("textures/rock1.png", True)
tree2img = texs.loadTexture("textures/tree2.png")
raspimg = texs.loadTexture("textures/Raspi256x256.png")
# environment cube
ectex = texs.loadTexture("textures/ecubes/skybox_stormydays.jpg")
myecube = pi3d.createEnvironmentCube(900.0,"CROSS")

# Create elevation map
mapwidth=1000.0                              
mapdepth=1000.0
mapheight=110.0
mymap = pi3d.createElevationMapFromTexture("textures/maze1.jpg",mapwidth,mapdepth,mapheight,128,128,1,"sub",0,0,0, smooth=False)
mymap2 = pi3d.createElevationMapFromTexture("textures/maze1.jpg",mapwidth,mapdepth,mapheight+0.1,128,128 ,64,"detail",0.0, 0.01, 0.0, smooth=True) 

myfog = pi3d.fog(0.02, (0.1,0.1,0.1,1.0)) 

#Create tree models
treeplane = pi3d.createPlane(4.0,5.0)

treemodel1 = pi3d.createMergeShape("baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

shed = pi3d.loadModel("models/shed1.obj",texs,"shed",0,3,0, 0,0,0, 2,2,2)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.createMergeShape("trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,900.0,900.0,10,"",8.0,3.0)
# (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)
raspberry = pi3d.createMergeShape("rasp")
raspberry.cluster(treemodel1, mymap,-250,+250,470.0,470.0,5,"",8.0,1.0)
# createMergeShape can be used to join loadModel object for much greater rendering speed
# however, because these objects can contain multiple vGroups, each with their own texture image
# it is necessary to make a merge for each vGroup and, later, draw each merged object using each
# of the textures 
# The cluster method can be used where there is only one vGroup but with more than one the different
# parts of the object get split up by the randomisation! Here I manually do the same thing as cluster
# by first generating an array of random locations and y-rotations

shedgp = {}
xArr = []
yArr = []
zArr = []
rArr = []
for i in range(20):
    xval = (random.random()-0.5)*50 + 19
    xArr.append(xval)
    zval = (random.random()-0.5)*50 - 19
    zArr.append(zval)
    yArr.append(mymap.calcHeight(-xval, -zval))
    rArr.append(180.0 + random.random()*45)
for g in shed.vGroup:
    thisAbbGp = pi3d.createMergeShape("shed")
    for i in range(len(xArr)):
        thisAbbGp.add(shed.vGroup[g], xArr[i], yArr[i], zArr[i], 0, rArr[i], 0)
    shedgp[g] = thisAbbGp

# lighting. The default light is a point light but I have made the position method capable of creating
# a directional light and this is what I do inside the loop. If you want a torch you don't need to move it about
light = pi3d.createLight(0, 4, 4, 2, "", 0,1,2, 0.1,0.1,0.2) #yellowish 'torch' or 'sun' (could be blueish ambient with different env cube)
light.on()

#screenshot number
scshots = 1

#energy counter
hp = 25
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

lastTm = time.time()
m = pi3d.matrix()
fly = False
walk = False
# Display scene and rotate cuboid
angle = 0
while 1:
    display.clear()
    
    pi3d.identity()
    pi3d.rotate(tilt,0,0)
    pi3d.rotate(0,rot,0)
    pi3d.position(xm,ym,zm)
    
    myecube.draw(ectex,xm,ym,zm)
    myfog.on()
    mymap.draw(rockimg1)
    mymap2.draw(rockimg2)
    mytrees1.drawAll(tree2img)
    raspberry.drawAll(raspimg)
    #shed.draw()
    
    # draw the sheds
    for g in shed.vGroup:
        shedgp[g].drawAll(shed.vGroup[g].texID)
    
    myfog.off()
    
    mx=mymouse.x
    my=mymouse.y
    
    rot += (mx-omx)*0.2
    tilt -= (my-omy)*0.2
    omx=mx
    omy=my
    v1 = pi3d.rotateVecY(rot,  0, 1, 2)
    v2 = pi3d.rotateVecX(tilt,v1[0], v1[1], v1[2])
    light.position(v2[0], v2[1], v2[2], 0) #fourth parameter in function sets (1=point light , default) or (0=distant light)
    # the light has to be turned as the scene rotates, it took ages to work out how to do this by reversing the rotation order!!!
    dx = -math.sin(rot*rads)
    dz = math.cos(rot*rads)
    dy = math.sin(tilt*rads)
    if (walk):
        if (fly):
            xm += dx*3
            zm += dz*3
            ym += dy*3
        else:
            dy = -(mymap.calcHeight(xm + dx, zm + dz)+avhgt) - ym
            if dy > -1.0: # limit steepness so can't climb up walls
                xm += dx
                zm += dz
                ym += dy
        if (xm < -490 or xm > 490 or zm < -490 or zm > 490): fly = True #reached the edge of the maze!

    #Press ESCAPE to terminate
    k = mykeys.read()
    if k >-1:
        if k==119: #key W toggle NB no longer need to hold down all the time
            walk = not(walk)
        elif k==115: #kry S
            walk = False
            dy = -(mymap.calcHeight(xm - dx, zm - dz)+avhgt) - ym
            if dy > -1.0:
                xm -= dx
                zm -= dz
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
            walk = False
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
