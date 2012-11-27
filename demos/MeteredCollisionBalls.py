import random
import sys

from pi3d import Keyboard

from pi3d import Display
from pi3d.Texture import Texture
from pi3d.Font import Font

from pi3d.sprite.Ball import Ball
from pi3d.util import String

# Ball parameters
MAX_BALLS = 1 #5
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100

BACKGROUND = 0.0, 0.0, 0.0, 0.0

FONT = Font("AR_CENA","#dd00aa")

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']


DISPLAY = Display.create(is_3d=False, background=BACKGROUND)

TEXTURES = [Texture(t) for t in TEXTURE_NAMES]

OFFSET = -10

class MeteredBall(Ball):
  def __init__(self, *args):
    super(MeteredBall, self).__init__(*args)


  def repaint(self, t):
    super(MeteredBall, self).repaint(t)
    if True:
      s = 'vel = %d, %d' % (self.vx, self.vy)
      # print(s)
      String.string(font=FONT,
                    string=s,
                    x=20, #OFFSET + self.x + self.radius / 2.0,
                    y=20, # OFFSET + self.y + self.radius / 2.0,
                    z=-5, rot=0,
                    sclx=0.02, scly=0.02)


def random_ball():
  """Return a ball with a random color, position and velocity."""
  return MeteredBall(random.choice(TEXTURES),
                     random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE),
                     random.uniform(0.0, DISPLAY.max_width),
                     random.uniform(0.0, DISPLAY.max_height),
                     random.uniform(-10.0, 10.0),
                     random.uniform(-10.0, 10.0))


SPRITES = [random_ball() for b in range(MAX_BALLS)]
DISPLAY.add_sprites(*SPRITES)

@Keyboard.screenshot('collision.jpg')
def my_loop():
  for i, ball1 in enumerate(SPRITES):
    for ball2 in SPRITES[0:i]:
      ball1.bounce_collision(ball2)

DISPLAY.loop(my_loop)

