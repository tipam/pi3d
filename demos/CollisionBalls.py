import random
import sys

from pi3d import Keyboard

from pi3d.Display import Display
from pi3d.DisplayLoop import DisplayLoop
from pi3d.Texture import Textures

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
MAX_RANDOMIZATION_TRIES = 20

TEXS = Textures()

class RandomBall(Ball):
  BALLS = []
  TEXTURES = [TEXS.loadTexture("textures/red_ball.png"),
              TEXS.loadTexture("textures/grn_ball.png"),
              TEXS.loadTexture("textures/blu_ball.png")]

  def __init__(self):
    super(RandomBall, self).__init__(random.choice(RandomBall.TEXTURES),
                                     1.0, 0, 0,
                                     random.uniform(-10.0, 10.0),
                                     random.uniform(-10.0, 10.0))
    self.randomize()
    self.index = len(RandomBall.BALLS)
    RandomBall.BALLS.append(self)

  def randomize(self):
    self.radius = random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE)
    self.mass = self.radius * self.radius
    self.x = random.uniform(0.0, SCNX)
    self.y = random.uniform(0.0, SCNY)

  def repaint(self, t):
    for ball in RandomBall.BALLS[0:self.index]:
      self.bounce_collision(ball)
    super(RandomBall, self).repaint(t)

# create balls and positions and colours.
for b in range(MAX_BALLS):
  RandomBall()

DisplayLoop(display,
            check_if_close_requested=Keyboard.make_closer(),
            sprites=RandomBall.BALLS).loop()

