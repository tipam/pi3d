#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example as the CollisionBalls demo but using 2d shader with the behaviour
included in the pi3d.sprites.Ball_2d class. The drawing is done repeatedly on
the Canvas but the Texture, location are held in Ball_2d and reset in repaint
To speed up rendering a scissor rectangle is set for each draw apart for the
last Ball which has to render the whole area to see the background! All a bit
complicated
"""

import random
import sys

import demo
import pi3d
from pi3d.sprite.Ball_2d import Ball_2d

MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100
MAX_BALL_VELOCITY = 10.0

KEYBOARD = pi3d.Keyboard()

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 0.0)
DISPLAY = pi3d.Display.create(background=BACKGROUND_COLOR)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height

SHADER = pi3d.Shader('2d_flat')
CANVAS = pi3d.Canvas()
CANVAS.set_shader(SHADER)

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']
TEXTURES = [pi3d.Texture(t) for t in TEXTURE_NAMES]

def random_ball():
  """Return a ball with a random color, position and velocity."""
  return Ball_2d(canvas=CANVAS, texture=random.choice(TEXTURES),
                   radius=random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE),
                   x=random.uniform(0.0, WIDTH ),
                   y=random.uniform(0.0, HEIGHT),
                   vx=random.uniform(-MAX_BALL_VELOCITY, MAX_BALL_VELOCITY),
                   vy=random.uniform(-MAX_BALL_VELOCITY, MAX_BALL_VELOCITY))

SPRITES = [random_ball() for b in range(MAX_BALLS)]

while DISPLAY.loop_running():
  for i, ball1 in enumerate(SPRITES):
    for ball2 in SPRITES[0:i]:
      ball1.bounce_collision(ball2)
    ball1.repaint(0 if i == (MAX_BALLS - 1) else 1)

  if KEYBOARD.read() == 27:
    DISPLAY.stop()
