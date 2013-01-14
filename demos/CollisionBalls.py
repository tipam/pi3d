import random
import sys

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Shader import Shader
from pi3d.Texture import Texture

from pi3d.sprite.Ball import Ball

MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_BALL_VELOCITY = 10.0

KEYBOARD = Keyboard()

BACKGROUND_COLOR = 1.0, 1.0, 1.0, 0.0
DISPLAY = Display.create(is_3d=False, background=BACKGROUND_COLOR)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height

SHADER = Shader('shaders/uv_flat')

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']
TEXTURES = [Texture(t) for t in TEXTURE_NAMES]

def random_ball():
  """Return a ball with a random color, position and velocity."""
  return Ball(shader=SHADER,
              texture=random.choice(TEXTURES),
              radius=random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE),
              x=random.uniform(-WIDTH / 2.0, WIDTH / 2.0),
              y=random.uniform(-HEIGHT / 2.0, HEIGHT / 2.0),
              vx=random.uniform(-MAX_BALL_VELOCITY, MAX_BALL_VELOCITY),
              vy=random.uniform(-MAX_BALL_VELOCITY, MAX_BALL_VELOCITY))


SPRITES = [random_ball() for b in range(MAX_BALLS)]
DISPLAY.add_sprites(*SPRITES)

while DISPLAY.loop_running():
  for i, ball1 in enumerate(SPRITES):
    for ball2 in SPRITES[0:i]:
      ball1.bounce_collision(ball2)

  if KEYBOARD.read() == 27:
    DISPLAY.stop()
