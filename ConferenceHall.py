#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" A large 3D model with shadows baked into textures
"""
import math, random, time

import demo
import pi3d

rads = 0.017453292512  # degrees to radians

#Create a Tkinter window in Display
winw,winh = 800, 600   	#64MB GPU memory setting
#winw,winh = 1920,1180	#128MB GPU memory setting

DISPLAY = pi3d.Display.create(tk=True, window_title='ConferenceHall demo in Pi3D',
                        w=winw, h=winh, far=2200.0, fov = 60,
                        background=(0.4, 0.8, 0.8, 1), frames_per_second=20)
win = DISPLAY.tkwin

#Setup shaders
flatsh = pi3d.Shader("uv_flat")
shade2d = pi3d.Shader('2d_flat')

# create splash screen and draw it
splash = pi3d.ImageSprite("textures/pi3d_splash.jpg", shade2d, w=10, h=10, z=0.2)
splash.draw()
DISPLAY.swap_buffers()

#Setup environment cube
ectex = pi3d.loadECfiles("textures/ecubes/Miramar", "miramar_256", "png", nobottom = True)
myecube = pi3d.EnvironmentCube(size=1800.0, maptype="FACES", nobottom=True)
myecube.set_draw_details(flatsh, ectex)

#Load Hall model
hall = pi3d.Model(file_string="models/ConferenceHall/conferencehall.egg", name="Hall", sx=0.1, sy=0.1, sz=0.1)
hall.set_shader(flatsh)

#key presses
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()

#position vars
mouserot = -70.0
tilt = 10.0
avhgt = 4.0
xm = 0.0
zm = 0.0
ym = avhgt

CAMERA = pi3d.Camera.instance()

try:
  while DISPLAY.loop_running():
    CAMERA.reset()

    #update mouse
    #inputs.do_input_events()
    """on some keyboard mouse setups you need to use inputs.get_mouse_movement(1)"""
    #mx, my, mv, mh, md = inputs.get_mouse_movement()
    #mouserot -= mx*0.2
    #tilt -= my*0.2

    #tilt can be used as a means to prevent the view from going under the landscape!
    if tilt < -1: sf = 1.0/-tilt
    else: sf = 1.0
    CAMERA.rotate(tilt, mouserot, 0)
    CAMERA.position((xm,ym,zm))

    #Draw scene
    hall.draw()
    myecube.rotateIncY(0.02) #Slowly rotate sky for effect
    myecube.draw() #Draw environment cube

    #Get inputs

    mx, my = mymouse.position()
    mouserot -= (mx-omx)*0.2
    tilt += (my-omy)*0.2
    omx=mx
    omy=my
    try:
      win.update()
    except Exception as e:
      print("bye,bye2", e)
      DISPLAY.destroy()
      try:
        win.destroy()
      except:
        pass
      mymouse.stop()
      exit()
    if win.ev == "resized":
      print("resized")
      DISPLAY.resize(win.winx, win.winy, win.width, win.height)
      CAMERA.reset((DISPLAY.near, DISPLAY.far, DISPLAY.fov,
                  DISPLAY.width / float(DISPLAY.height)))
      win.resized = False
    if win.ev == "key":
      if win.key == "w":
        xm-=math.sin(mouserot*rads)*2
        zm+=math.cos(mouserot*rads)*2
      if win.key == "s":
        xm+=math.sin(mouserot*rads)*2
        zm-=math.cos(mouserot*rads)*2
      if win.key == "a":
        mouserot -= 2
      if win.key == "d":
        mouserot += 2
      if win.key == "p":
        pi3d.screenshot("ConferenceHall.jpg")
      if win.key == "Escape":
        try:
          print("bye,bye1")
          DISPLAY.destroy()
          try:
            win.destroy()
          except:
            pass
          mymouse.stop()
          exit()
        except:
          pass
    if win.ev=="drag" or win.ev=="click" or win.ev=="wheel":
      xm-=math.sin(mouserot*rads)*2
      zm+=math.cos(mouserot*rads)*2
    else:
      win.ev=""  #clear the event so it doesn't repeat

except Exception as e:
  print("bye,bye3", e)
  DISPLAY.destroy()
  try:
    win.destroy()
  except:
    pass
  mymouse.stop()
  exit()

