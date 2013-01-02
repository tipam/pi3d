import random
import sys

from pi3d import Display
from pi3d.Camera import Camera
from pi3d.Keyboard import Keyboard
from pi3d.Shader import Shader
from pi3d.Texture import Texture

from pi3d.context.Light import Light

from pi3d.sprite.Ball import Ball

MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_BALL_VELOCITY = 10.0

KEYBOARD = Keyboard()

BACKGROUND = 1.0, 1.0, 1.0, 0.0
DISPLAY = Display.create(is_3d=False, background=BACKGROUND)
WIDTH, HEIGHT = DISPLAY.win_width, DISPLAY.win_height

CAMERA_LENS = (1, 1000, WIDTH / 1000.0, HEIGHT / 1000.0)
CAMERA = Camera((0, 0, 0), (0, 0, -0.1), CAMERA_LENS)

LIGHT = Light((10, 10, -20))

SHADER = Shader('shaders/uv_flat')

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']
TEXTURES = [Texture(t) for t in TEXTURE_NAMES]

def random_ball():
  """Return a ball with a random color, position and velocity."""
  return Ball(CAMERA, LIGHT, SHADER,
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
