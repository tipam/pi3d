import random
import sys

from pi3d import Keyboard

from pi3d import Display
from pi3d.Texture import Texture

from pi3d.sprite.Ball import Ball

# Setup display and initialise pi3d
DISPLAY = Display.create(is_3d=False)

# Set last value (alpha) to zero for a transparent background!
DISPLAY.setBackColour(0, 0.2, 0.6, 0)

# Ball parameters
MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100

TEXTURES = [Texture("textures/red_ball.png"),
            Texture("textures/grn_ball.png"),
            Texture("textures/blu_ball.png")]

def random_ball():
  return Ball(random.choice(TEXTURES),
              random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE),
              random.uniform(0.0, DISPLAY.max_width),
              random.uniform(0.0, DISPLAY.max_height),
              random.uniform(-10.0, 10.0),
              random.uniform(-10.0, 10.0))

SPRITES = []

# create balls and positions and colours.
for b in range(MAX_BALLS):
  SPRITES.append(random_ball())

DISPLAY.add_sprites(*SPRITES)

@Keyboard.screenshot('collision.jpg')
def my_loop():
  for i, ball1 in enumerate(SPRITES):
    for ball2 in SPRITES[0:i]:
      ball1.bounce_collision(ball2)

DISPLAY.loop(my_loop)

