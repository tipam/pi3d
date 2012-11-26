import random
import sys

from pi3d import Keyboard

from pi3d.Display import Display
from pi3d.Display import DISPLAY
from pi3d.DisplayLoop import DisplayLoop
from pi3d.Texture import Texture

from pi3d.sprite.Ball import Ball

# Setup display and initialise pi3d
display = Display()
SCNX =  display.max_width
SCNY = display.max_height
display.create2D(0, 0, SCNX, SCNY, 0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.6,0)

# Ball parameters
MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
SPRITES = [] 
"""
 for clarity I am holding the list of things for the display to draw externally (also the textures)
 in the general case there might other objects around apart from balls. User controlled paddles, say, and
 the different objects need to be able to tell where each other is and act accordingly (in their respective
 repaint() methods
"""
TEXTURES = [Texture("textures/red_ball.png"),
            Texture("textures/grn_ball.png"),
            Texture("textures/blu_ball.png")]

class RandomBall(Ball):
  def __init__(self):
    super(RandomBall, self).__init__(random.choice(TEXTURES),
                                     1.0, 0, 0,
                                     random.uniform(-10.0, 10.0),
                                     random.uniform(-10.0, 10.0))
    self.randomize()
    self.index = len(SPRITES)
    # it is easier to understand if this instance of RandomBall gets added where the constructor is called (see below)
    # Of course this isn't as safe but in the general case the developer has to keep control of all the objects!
    
  def randomize(self):
    self.radius = random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE)
    self.mass = self.radius * self.radius
    self.x = random.uniform(0.0, SCNX)
    self.y = random.uniform(0.0, SCNY)

  # repaint is where the 'physics' can be done i.e.  every second or so you could check that the total energy of the system
  # was not increasing or decreasing and adjust all the velocities up or down accordingly. You could also add gravity or assign
  # charge according to self.texture and repel or attract etc.
  def repaint(self, t):
    for ball in SPRITES[0:self.index]:
      self.bounce_collision(ball)
    super(RandomBall, self).repaint(t)


# create balls and positions and colours.
for b in range(MAX_BALLS):
  SPRITES.append(RandomBall())

display.add_sprites(*SPRITES)
display.loop(Keyboard.make_closer())

