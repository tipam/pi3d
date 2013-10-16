#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

"""This demo shows the use of the Orthographic Camerae for 2D drawing. Also
threading is used to allow the file access to be done in the background.

Schuitz screwed around with this a lot to handle an arbitrary number of
textures (within reasonable limits) fading in and out on top of each
other without breaking the UI.  I settled on 8.

The method is a little involved.  There are a small number of Canvases (8)
that get recycled.  A "Carousel" class keeps track of which canvas has focus and
what texture file index (from the file list) it contains.  Handy % operators keep the
'carousel' and texture file indices wrapping around properly at the ends.

The init condition has the 0th file somewhere in the middle, with focus,
to pre-buffer some images in either direction.

Conceptually, when the slides are navigated left or right, a canvas slot falls off the
far end and tacked on the approaching end, where a thread fills in a texture from
the file list in the same direction.

Confused yet?

Everything gets straighted out with the Carousel.draw() function which knows to
draw out the canvases far to near (thanks to opengl transparency gotchas), so it
will know which to start drawing first from the currently focused canvas.  At least the
canvasses are always in a spatial sequential order, except for the wraparound.

An update() function checks the fade directions and visibility of each canvas and
adjusts the alphas every time it is called.  Other transforms could happen in here later.

In a future version I want to employ a lock to hold threads from starting until a
screen draw activity flag has gone quiet, or some timeout happens.

There is still some interesting behaviour when the UI overruns the thread progress.
You see the previously loaded texture until the thread catches up.  See for example
'falling down barn' and, 8 slides later, 'pi3d splash screen'.  Now go back 8.

"""
import random, time, glob, threading
import demo
import pi3d

from six.moves import queue

print("#########################################################")
print("press ESC to escape, S to go back, any key for next slide")
print("#########################################################")

LOGGER = pi3d.Log.logger(__name__)
LOGGER.info("Log using this expression.")

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(background=(0.0, 0.0, 0.0, 1.0), frames_per_second=20)
shader = pi3d.Shader("uv_flat")

CAMERA = pi3d.Camera(is_3d=False)

#iFiles = glob.glob("/home/pi/slidemenu/testdir/*.*")
iFiles = glob.glob("textures/*.*")
nFi = len(iFiles)
fileQ = queue.Queue() # queue for loading new texture files

alpha_step = 0.025
nSli = 8
drawFlag = False

def tex_load():
  """ This function runs all the time in a background thread. It checks the
  fileQ for images to load that have been inserted by Carousel.next() or prev()

  here the images are scaled to fit the Display size, if they were to be
  rendered pixel for pixel as the original then the mipmap=False argument would
  be used, which is faster, and w and h values set to the Texture size i.e.

  tex = pi3d.Texture(f, mipmap=False)
  ...
  wi, hi = tex.ix, tex.iy

  mipmap=False can also be used to speed up Texture loading and reduce the work
  required of the cpu
  """
  while True:
    item = fileQ.get()
    # reminder, item is [filename, target Slide]
    fname = item[0]
    slide = item[1]
    #block until all the dawing is done TBD
    #tex = pi3d.Texture(item[0], mipmap=False) #pixelly but faster 3.3MB in 3s
    tex = pi3d.Texture(item[0], blend=True, mipmap=True) #nicer but slower 3.3MB in 4.5s
    xrat = DISPLAY.width/tex.ix
    yrat = DISPLAY.height/tex.iy
    if yrat < xrat:
      xrat = yrat
    wi, hi = tex.ix * xrat, tex.iy * xrat
    slide.set_draw_details(shader,[tex])
    slide.scale(wi, hi, 1.0)
    slide.set_alpha(0)
    fileQ.task_done()


class Slide(pi3d.Sprite):
  def __init__(self):
    super(Slide, self).__init__(w=1.0, h=1.0)
    self.visible = False
    self.fadeup = False
    self.active = False


class Carousel:
  def __init__(self):
    self.slides = [None]*nSli
    half = 0
    for i in range(nSli):
      self.slides[i] = Slide()
    for i in range(nSli):
      # never mind this, hop is just to fill in the first series of images from
      # inside-out: 4 3 5 2 6 1 7 0.
      half += (i%2)
      step = (1,-1)[i%2]
      hop = 4 + step*half

      self.slides[hop].positionZ(0.8-(hop/10))
      item = [iFiles[hop%nFi], self.slides[hop]]
      fileQ.put(item)

    self.focus = 3 # holds the index of the focused image
    self.focus_fi = 0 # the file index of the focused image
    self.slides[self.focus].visible = True
    self.slides[self.focus].fadeup = True

  def next(self):
    self.slides[self.focus].fadeup = False
    self.focus = (self.focus+1)%nSli
    self.focus_fi = (self.focus_fi+1)%nFi
    # the focused slide is set to z = 0.1.
    # further away as i goes to the left (and wraps)
    for i in range(nSli):
      self.slides[(self.focus-i)%nSli].positionZ(0.1*i + 0.1)
    self.slides[self.focus].fadeup = True
    self.slides[self.focus].visible = True

    item = [iFiles[(self.focus_fi+4)%nFi], self.slides[(self.focus-4)%nSli]]
    fileQ.put(item)

  def prev(self):
    self.slides[self.focus].fadeup = False
    self.focus = (self.focus-1)%nSli
    self.focus_fi = (self.focus_fi-1)%nFi
    for i in range(nSli):
      self.slides[(self.focus-i)%nSli].positionZ(0.1*i + 0.1)
    self.slides[self.focus].fadeup = True
    self.slides[self.focus].visible = True

    item = [iFiles[(self.focus_fi-3)%nFi], self.slides[(self.focus+5)%nSli]]
    fileQ.put(item)

  def update(self):
    # for each slide check the fade direction, bump the alpha and clip
    for i in range(nSli):
      a = self.slides[i].alpha()
      if self.slides[i].fadeup == True and a < 1:
        a += alpha_step
        self.slides[i].set_alpha(a)
        self.slides[i].visible = True
        self.slides[i].active = True
      elif self.slides[i].fadeup == False and a > 0:
        a -= alpha_step
        self.slides[i].set_alpha(a)
        self.slides[i].visible = True
        self.slides[i].active = True
      else:
        if a <= 0:
          self.slides[i].visible = False
        self.slides[i].active = False


  def draw(self):
    # slides have to be drawn back to front for transparency to work.
    # the 'focused' slide by definition at z=0.1, with deeper z
    # trailing to the left.  So start by drawing the one to the right
    # of 'focused', if it is set to visible.  It will be in the back.
    for i in range(nSli):
      ix = (self.focus+i+1)%nSli
      if self.slides[ix].visible == True:
        self.slides[ix].draw()


crsl = Carousel()

t = threading.Thread(target=tex_load)
t.daemon = True
t.start()

# block the world, for now, until all the initial textures are in.
# later on, if the UI overruns the thread, there will be no crashola since the
# old texture should still be there.
fileQ.join()

# Fetch key presses
mykeys = pi3d.Keyboard()
CAMERA = pi3d.Camera.instance()
CAMERA.was_moved = False #to save a tiny bit of work each loop


while DISPLAY.loop_running():
  crsl.update()
  crsl.draw()

  k = mykeys.read()
  #k = -1
  if k >-1:
    first = False
    d1, d2 = 2, 3
    if k==27: #ESC
      mykeys.close()
      DISPLAY.stop()
      break
    if k==115: #S go back a picture
      crsl.prev()
    #all other keys load next picture
    else:
      crsl.next()

DISPLAY.destroy()

