# Forest walk example using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.04 - 20Jul12
# 
# grass added, new environment cube using FACES
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

import pi3d,math,random

rads = 0.017453292512  # degrees to radians

# Setup display and initialise pi3d
display = pi3d.display()
display.create3D(100,100,1600,800, 0.5, 800.0, 60.0)   	# x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1)    	# r,g,b,alpha

# Load textures
texs = pi3d.textures()
tree2img = texs.loadTexture("textures/tree2.png")
tree1img = texs.loadTexture("textures/tree1.png")
grassimg = texs.loadTexture("textures/grass.png")
hb2img = texs.loadTexture("textures/hornbeam2.png")

#ectex = pi3d.loadTexture("textures/SkyBox.png")
#myecube = pi3d.createEnvironmentCube(900.0,"HALFCROSS")

ectex=pi3d.loadECfiles("textures/ecubes","sbox",texs)
myecube = pi3d.createEnvironmentCube(900.0,"FACES")

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = texs.loadTexture("textures/mountains3_512.jpg")
mymap = pi3d.createElevationMapFromTexture("textures/mountainsHgt.jpg",mapwidth,mapdepth,mapheight,64,64) #testislands.jpg
 
#Create tree models	
treeplane = pi3d.createPlane(4.0,5.0)

treemodel1 = pi3d.createMergeShape("baretree")
treemodel1.add(treeplane, 0,0,0)
treemodel1.add(treeplane, 0,0,0, 0,90,0)

treemodel2 = pi3d.createMergeShape("bushytree")
treemodel2.add(treeplane, 0,0,0)
treemodel2.add(treeplane, 0,0,0, 0,60,0)
treemodel2.add(treeplane, 0,0,0, 0,120,0)

#Create grass model	
grassplane = pi3d.createPlane(1.0,0.3,"",0,-2,0)
grassmodel = pi3d.createMergeShape("grass")
grassmodel.add(grassplane, 0,0,0)
grassmodel.add(grassplane, 0,0,0, 0,60,0)
grassmodel.add(grassplane, 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.createMergeShape("trees1")
mytrees1.cluster(treemodel1, mymap,0.0,0.0,200.0,200.0,30,"",8.0,3.0)
#               (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees2 = pi3d.createMergeShape("trees2")
mytrees2.cluster(treemodel2, mymap,0.0,0.0,200.0,200.0,30,"",6.0,3.0)
#               (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees3 = pi3d.createMergeShape("trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,30,"",4.0,2.0)
#               (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mygrass = pi3d.createMergeShape("grass")
mygrass.cluster(grassmodel, mymap,0.0,0.0,100.0,100.0,100,"",10.0,4.0)

#mygrass2 = pi3d.createMergeShape("grass2")
#mygrass2.cluster(mygrass, mymap,100.0,0.0,100.0,100.0,1,"",1.0,1.0)

#               (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)


#screenshot number
scshots = 1  

#avatar camera
rot=0.0
tilt=0.0
avhgt = 2.0
xm=0.0
zm=0.0
ym= -(mymap.calcHeight(xm,zm)+avhgt)

# setup matrices
mtrx = pi3d.matrix()

# Fetch key presses
mykeys = pi3d.key()
mymouse = pi3d.mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

# Display scene and rotate cuboid
while 1:
    display.clear()
    
    mtrx.identity()
    mtrx.rotate(tilt,0,0)
    mtrx.rotate(0,rot,0)
    mtrx.translate(xm,ym,zm)
    
    myecube.draw(ectex,xm,ym,zm)
    mymap.draw(mountimg1)
    mygrass.drawAll(grassimg)
    mytrees1.drawAll(tree2img)
    mytrees2.drawAll(tree1img)
    mytrees3.drawAll(hb2img)

    mx=mymouse.x
    my=mymouse.y
    
    #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
    rot += (mx-omx)*0.2
    tilt -= (my-omy)*0.2
    omx=mx
    omy=my
		
    #Press ESCAPE to terminate
    k = mykeys.read()
    if k >-1:
	if k==119:    #key W
	    xm-=math.sin(rot*rads)
	    zm+=math.cos(rot*rads)
	    ym = -(mymap.calcHeight(xm,zm)+avhgt)
	elif k==115:  #kry S
	    xm+=math.sin(rot*rads)
	    zm-=math.cos(rot*rads)
	    ym = -(mymap.calcHeight(xm,zm)+avhgt)
	elif k==39:   #key '
	    tilt -= 2.0
	    print tilt
	elif k==47:   #key /
	    tilt += 2.0
	elif k==97:   #key A
	    rot -= 2
	elif k==100:  #key D
	    rot += 2
	elif k==112:  #key P
	    display.screenshot("forestWalk"+str(scshots)+".jpg")
	    scshots += 1
	elif k==10:   #key RETURN
	    mc = 0
	elif k==27:    #Escape key
	    mykeys.close()
	    texs.deleteAll()
	    display.destroy()
	    break
	else:
	    print k
   
    display.swapBuffers()
