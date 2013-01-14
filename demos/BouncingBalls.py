# Bouncing demonstrates pi3d sprites over the desktop.
# It uses the orthographic view scaled to the size of the window;
# this means that sprites can be drawn at pixel resolution
# which is more common for 2D.  Also demonstrates a mock title bar.

import sys, random

import demo
demo.demo(__name__)

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Texture import Texture

from pi3d.util import Draw
from pi3d.util.Font import Font
from pi3d.util.Screenshot import screenshot
from pi3d.util.String import drawString2D

# Setup display and initialise pi3d
scnx = 800
scny = 600
DISPLAY = Display.create(is_3d=False, x=100, y=100, w=scnx, h=scny,
                         background=(0,0.2,0.6,1))

# Ball parameters
maxballs = 40
maxballsize = 60
minballsize = 30
maxspeed = 30

# Ball x,y position
bx=[]
by=[]

# Ball direction vector
dx=[]
dy=[]

# Ball size (scale), ball image reference
bs=[]
bi=[]

# Setup ball positions, sizes, directions and colours
for b in range (0, maxballs):
  bx.append(random.random() * scnx)
  by.append(random.random() * scny)
  dx.append((random.random() - 0.5) * maxspeed)
  dy.append((random.random() - 0.5) * maxspeed)
  bs.append(random.random() * maxballsize + minballsize)
  bi.append(int(random.random() * 3))

ball = []
ball.append(Texture("textures/red_ball.png"))
ball.append(Texture("textures/grn_ball.png"))
ball.append(Texture("textures/blu_ball.png"))

bar = Texture("textures/bar.png")
bbtitle = Texture("textures/pi3dbbd.png",True)

arialFont = Font("AR_CENA","#ddff88")   #load AR_CENA font and set the font colour

# Fetch key presses
mykeys = Keyboard()
scshots = 1

while True:
  DISPLAY.clear()

  for b in range(maxballs):
    Draw.sprite(ball[bi[b]],bx[b],by[b],-2.0,bs[b],bs[b])

    # Increment ball positions
    bx[b]=bx[b]+dx[b]
    by[b]=by[b]+dy[b]

    # X coords outside of drawing area?  Then invert X direction
    if bx[b]>scnx or bx[b]<0:
      dx[b]=-dx[b]

    # Y coords outside of drawing area?  Then invert Y direction
    if by[b]>scny or by[b]<0:
      dy[b]=-dy[b]

  drawString2D(arialFont,"Raspberry Pi ROCKS!",100,300,80)

  #draw a bar at the top of the screen
  Draw.rectangle(bar,0,scny,scnx,32)
  Draw.rectangle(bbtitle,5,scny,256+5,32)

  k = mykeys.read()
  if k >-1:
    if k==112:
      screenshot("screen3D"+str(scshots)+".jpg")
      scshots += 1
    if k==27:
      mykeys.close()
      DISPLAY.destroy()
      break

  DISPLAY.swapBuffers()

