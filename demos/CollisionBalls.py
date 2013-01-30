#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of using the loop control in the Display class with the behaviour
included in the pi3d.sprites.Ball class
"""

import random
import sys

import demo
import pi3d

MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_BALL_VELOCITY = 10.0

KEYBOARD = pi3d.Keyboard()

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 0.0)
DISPLAY = pi3d.Display.create(is_3d=False, background=BACKGROUND_COLOR)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height

SHADER = pi3d.Shader('shaders/uv_flat')

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']
TEXTURES = [pi3d.Texture(t) for t in TEXTURE_NAMES]

def random_ball():
  """Return a ball with a random color, position and velocity."""
  return pi3d.Ball(shader=SHADER,
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

  k = KEYBOARD.read()
  if k == 27:
    DISPLAY.stop()
  elif k == 112: 
    pi3d.screenshot("collision1.jpg")
