import random
import sys

from pi3d import Keyboard

from pi3d.Display import Display
from pi3d.DisplayLoop import DisplayLoop
from pi3d.Texture import Textures

from pi3d.sprite.Ball import Ball

# Setup display and initialise pi3d
display = Display()
scnx =  display.max_width
scny = display.max_height
display.create2D(0,0,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(0,0.2,0.6,0)

# Ball parameters
MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_RANDOMIZATION_TRIES = 20

texs = Textures()
balltex = []
balltex.append(texs.loadTexture("textures/red_ball.png"))
balltex.append(texs.loadTexture("textures/grn_ball.png"))
balltex.append(texs.loadTexture("textures/blu_ball.png"))

class RandomBall(Ball):
  def __init__(self, texture):
    super(RandomBall, self).__init__(texture, 1.0, 0, 0,
                                     random.uniform(-10.0, 10.0),
                                     random.uniform(-10.0, 10.0))
    self.texture = texture
    self.randomize()

  def randomize(self):
    self.radius = random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE)
    self.mass = self.radius * self.radius
    self.x = random.uniform(0.0, scnx)
    self.y = random.uniform(0.0, scny)

  def separate(self, balls, max_tries=MAX_RANDOMIZATION_TRIES):
    for i in range(max_tries):
      for b in balls:
        if b.hit(self):
          self.randomize()
          break
      else:
        return

  def update(self, display_loop, index, t):
    for ball in display_loop.sprites[0:index]:
      self.bounce_collision(ball)
    super(RandomBall, self).update(display_loop, index, t)

  def load(self):
    pass


# create balls and positions and make sure they don't touch to start with.
balls = [RandomBall(balltex[0]) for b in range(MAX_BALLS)]
for i, ball in enumerate(balls):
  if i:
    ball.separate(balls[0:i])

DisplayLoop(display,
            check_for_close=Keyboard.make_closer(),
            sprites=balls).loop()

