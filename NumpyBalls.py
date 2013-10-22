#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of using the loop control in the Display class with the behaviour
included in the pi3d.sprites.Ball class
"""

import random
import sys
import numpy as np

import demo
import pi3d

MAX_BALLS = 50
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_BALL_VELOCITY = 10.0

KEYBOARD = pi3d.Keyboard()
LOGGER = pi3d.Log.logger(__name__)

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 0.0)
DISPLAY = pi3d.Display.create(background=BACKGROUND_COLOR)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height
CAMERA = pi3d.Camera(is_3d=False)
SHADER = pi3d.Shader('uv_flat')

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

VERT = np.array([[s.radius for s in SPRITES] for i in SPRITES])
HORIZ = np.array([[s.radius for i in SPRITES] for s in SPRITES])

DISPLAY.add_sprites(*SPRITES)

LOGGER.info('Starting CollisionBalls')

while DISPLAY.loop_running():
  a = np.array([b.unif[0:3] for b in SPRITES])
  b = np.copy(a)
  d0 = np.subtract.outer(a[:,0], b[:,0])
  d1 = np.subtract.outer(a[:,1], b[:,1])
  d3 = np.hypot(d0, d1) - VERT - HORIZ
  
  for i in range(0, MAX_BALLS):
    for j in range(i + 1, MAX_BALLS):
      if d3[i][j] < 0:
        SPRITES[i].bounce_collision(SPRITES[j])

  if KEYBOARD.read() == 27:
    DISPLAY.stop()
