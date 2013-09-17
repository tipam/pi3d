#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Same as ForestWalk demo but with moving Camera and application of a
series of PostProcess filters
"""
import math, random, time

import demo
import pi3d
pi3d.Log.set_logs(file="/home/annon/pi3d_demos/templog.txt")
LOGGER = pi3d.Log.logger(__name__)
LOGGER.info("\n\nAs yet there is no system for freeing gpu memory taken by shader\n"\
            "programs. On the pi after loading a total of 16 (2 base + 14 demo)\n"\
            "shaders, the screen will go black. Normally you wouldn't keep\n"\
            "loading lots of shaders in this way. Comment out some of the lines\n"\
            "where filter_list is defined\nTODO - free shader memory?\n")
            

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(w=1280, h=720)
DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
# yellowish directional light blueish ambient light
pi3d.Light(lightpos=(1, -1, -3), lightcol =(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

#========================================

# load shader
shader = pi3d.Shader("uv_reflect")
flatsh = pi3d.Shader("uv_flat")

tree2img = pi3d.Texture("textures/tree2.png")
tree1img = pi3d.Texture("textures/tree1.png")
hb2img = pi3d.Texture("textures/hornbeam2.png")
bumpimg = pi3d.Texture("textures/grasstile_n.jpg")
reflimg = pi3d.Texture("textures/stars.jpg")
rockimg = pi3d.Texture("textures/rock1.jpg")

FOG = ((0.3, 0.3, 0.4, 0.5), 650.0)
TFOG = ((0.2, 0.24, 0.22, 0.3), 150.0)

#myecube = pi3d.EnvironmentCube(900.0,"HALFCROSS")
ectex=pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="cube")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
mapheight = 60.0
mountimg1 = pi3d.Texture("textures/mountains3_512.jpg")
mymap = pi3d.ElevationMap("textures/mountainsHgt.jpg", name="map",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32) #testislands.jpg
mymap.set_draw_details(shader, [mountimg1, bumpimg, reflimg], 128.0, 0.0)
mymap.set_fog(*FOG)

#Create tree models
treeplane = pi3d.Plane(w=4.0, h=5.0)

treemodel1 = pi3d.MergeShape(name="baretree")
treemodel1.add(treeplane.buf[0], 0,0,0)
treemodel1.add(treeplane.buf[0], 0,0,0, 0,90,0)

treemodel2 = pi3d.MergeShape(name="bushytree")
treemodel2.add(treeplane.buf[0], 0,0,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,60,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.MergeShape(name="trees1")
mytrees1.cluster(treemodel1.buf[0], mymap,0.0,0.0,200.0,200.0,20,"",8.0,3.0)
mytrees1.set_draw_details(flatsh, [tree2img], 0.0, 0.0)
mytrees1.set_fog(*TFOG)

mytrees2 = pi3d.MergeShape(name="trees2")
mytrees2.cluster(treemodel2.buf[0], mymap,0.0,0.0,200.0,200.0,20,"",6.0,3.0)
mytrees2.set_draw_details(flatsh, [tree1img], 0.0, 0.0)
mytrees2.set_fog(*TFOG)

mytrees3 = pi3d.MergeShape(name="trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,20,"",4.0,2.0)
mytrees3.set_draw_details(flatsh, [hb2img], 0.0, 0.0)
mytrees3.set_fog(*TFOG)

#Create monument
monument = pi3d.Model(file_string="models/pi3d.obj", name="monument")
monument.set_shader(shader)
monument.set_normal_shine(bumpimg, 16.0, reflimg, 0.5)
monument.set_fog(*FOG)
monument.translate(100.0, -mymap.calcHeight(100.0, 230) + 5.8, 230.0)
monument.scale(20.0, 20.0, 20.0)
monument.rotateToY(65)

#screenshot number
scshots = 1

#avatar camera
rot = 0.0
tilt = 0.0
avhgt = 3.5
xm = 0.0
zm = 0.0
ym = mymap.calcHeight(xm, zm) + avhgt

# Fetch key presses
mykeys = pi3d.Keyboard()

CAMERA = pi3d.Camera.instance()
CAM2D = pi3d.Camera(is_3d=False)

font = pi3d.Font("fonts/FreeMonoBoldOblique.ttf", "#dddd80")
# list [[name, [list of custom vals -> unif[48:]], [list increments each frame]]]
filter_list =   [ ["shaders/filter_blurradial", [0.0, 0.0, 0.0, 0.0, 0.05]], # centre_x, y, NA, radial_amount, rotation_amount
                  ["shaders/filter_shiftrgb", [0.25, 0.3, 0.1]], # direction, shift, hue
                  ["shaders/filter_noise", [15.0, 100.0, 0.25], [0.01]], # time,  NB slow on the raspberry pi
                  ["shaders/filter_crystalog", [10.0, 100.0, 0.25], [0.0005]], # time, scale, limit
                  ["shaders/filter_patterns", [1.0, 0.3],[0.01, 0.001]], # time, size
                  ["shaders/filter_displace", [14.0],[0.05]], # time
                  ["shaders/filter_space_dist", [2.0],[0.01]], # time
                  ["shaders/filter_color_dist", [21.0, 3.0, 7.0],[0.002, -0.002]], # distortion_r, g, b
                  ["shaders/filter_lens", [-0.2, -0.2, 0.3]], # centre_x, y, radius
                  ["post_base", [2.5]], # sampling distance for convolution sampling
                  ["shaders/filter_outline", [0.0, 0.0, 0.0]], # outline_colour_r, g, b
                  ["shaders/filter_colorize", [1.0, 0.5, 0.0, 0.0, 1.0, 0.5, 0.5, 0.0, 1.0]], # colour0_r, g, b, colour1_r, g, b, colour2_r, g, b
                  ["shaders/filter_neg", [0.0, 0.0, 0.0]], #NA
                  ["shaders/filter_charcoal", [0.0, 0.0, 0.0, 1.0, 1.0, 0.7]], # charcoal_colour_r, g, b, paper_colour_r, g, b
                  ["shaders/filter_toon", [0.0, 0.0, 0.0]], # outline_colour_r, g, b
                  ["shaders/filter_hatch", [0.1, 0.0, 0.0]], # solid_colour_r, g, b
                  ["shaders/filter_sepia", [0.0, 0.0, 0.0]]] # NA

n_filter = len(filter_list)
i_filter = -1 # as incremented prior to loading
cx, cz = 70.0, 190.0
c_rad = 80.0
frame = 0
st_time = time.time()
while DISPLAY.loop_running():
  if rot % 360.0 == 0.0: #NB this has to happen first loop!
    LOGGER.info("{} FPS was {:.5}".format(filter_list[i_filter % n_filter][0],
                  360.0 / (time.time() - st_time)))
    i_filter = (i_filter + 1) % n_filter
    texetc = [reflimg] if (i_filter < 2) else None
    post = pi3d.PostProcess(filter_list[i_filter][0], add_tex=texetc, divide=24, mipmap=False)
    post.sprite.set_custom_data(48, filter_list[i_filter][1])
    string = pi3d.String(font=font, string=filter_list[i_filter][0],
              camera=CAM2D, is_3d=False, x=0, y=-220, z=0.5)
    string.set_shader(flatsh)
    st_time = time.time()
  if len(filter_list[i_filter]) > 2:
    for i, delta in enumerate(filter_list[i_filter][2]):
      post.sprite.set_custom_data(48 + i, [filter_list[i_filter][1][i] + rot * delta])
  xm = cx + math.sin(math.radians(rot)) * c_rad
  zm = cz - math.cos(math.radians(rot)) * c_rad
  ym = mymap.calcHeight(xm, zm) + avhgt
  rot += 1.0
  CAMERA.reset()
  CAMERA.rotate(tilt, rot + 15.0, 0)
  CAMERA.position((xm, ym, zm))

  post.start_capture()##<<<<<<<<<<<<<<
  monument.draw()
  mytrees1.draw()
  mytrees2.draw()
  mytrees3.draw()
  mymap.draw()
  myecube.draw()
  post.end_capture()##>>>>>>>>>>>>>>

  post.draw()
  string.draw()
  #pi3d.screenshot("/home/annon/pi3d_demos/temppics/pic{:0>5}.jpg".format(frame))
  frame += 1

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==112:  #key P
      pi3d.screenshot("forestWalk"+str(scshots)+".jpg")
      scshots += 1
    elif k==10:   #key RETURN
      mc = 0
    elif k==27:  #Escape key
      mykeys.close()
      DISPLAY.stop()
      break

  CAMERA.was_moved = False
