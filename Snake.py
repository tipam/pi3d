#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" based on code Written by Simpliplant, this just happened to be the
first result for a google search for 'python snake code'
"""

from random import randrange
from math import sin, cos, radians

import demo
import pi3d
 
NORTH, SOUTH = (0.0, 0.0, 1.0), (0.0, 0.0, -1.0) # (dx, dy, dz)
EAST, WEST =  (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0) # (dx, dy, dz)
UP, DOWN =  (0.0, 1.0, 0.0), (0.0, -1.0, 0.0) # (dx, dy, dz)
TURN_LEFT = {NORTH:WEST, WEST:SOUTH, SOUTH:EAST, EAST:NORTH}
TURN_RIGHT = {NORTH:EAST, EAST:SOUTH, SOUTH:WEST, WEST:NORTH}

SIZE = 100.0
BLOCK_SIZE = 4.0

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=200, y=200, frames_per_second=10)
DISPLAY.set_background(0.4,0.8,0.8,1)      # r,g,b,alpha
#========================================
CAMERA = pi3d.Camera()
LIGHT = pi3d.Light(lightamb=(0.6, 0.6, 0.8))
# load shader
shader = pi3d.Shader("uv_light")
flatsh = pi3d.Shader("uv_flat")
foodTex = pi3d.Texture("textures/Raspi256x256.png")
partTex = pi3d.Texture("textures/stripwood.jpg")

ectex = pi3d.loadECfiles("textures/ecubes","skybox_hall")
myecube = pi3d.EnvironmentCube(size=2.0 * SIZE, maptype="FACES", name="cube")
myecube.set_draw_details(shader, ectex)

class Food:
  def __init__(self, snake):
    self.snake = snake
    plane = pi3d.Plane(w=BLOCK_SIZE * 2.0, h=BLOCK_SIZE * 2.0)
    self.shape = pi3d.MergeShape()
    self.shape.add(plane, 0,0,0)
    self.shape.add(plane, 0,0,0, 0,90,0)
    self.shape.set_draw_details(shader, [foodTex])
    self.spawn()
 
  def spawn(self):
    collision = True
 
    while collision:
      random_x = randrange(-SIZE, SIZE, BLOCK_SIZE) + BLOCK_SIZE / 2.0
      random_y = randrange(-SIZE, SIZE, BLOCK_SIZE) + BLOCK_SIZE / 2.0
      random_z = randrange(-SIZE, SIZE, BLOCK_SIZE) + BLOCK_SIZE / 2.0
 
      collision = False
 
      for each in snake.parts:
        if each.shape.x() == random_x and each.shape.y() == random_y and each.shape.z() == random_z:
          collision = True
          break
 
    self.shape.position(random_x, random_y, random_z)

  def draw(self):
    self.shape.draw()
 
class Part:
  def __init__(self, x=0, y=0, z=0, direction=NORTH):
    self.direction = direction
    #self.shape = pi3d.Cuboid(w=BLOCK_SIZE, h=BLOCK_SIZE, d=BLOCK_SIZE)
    self.shape = pi3d.Sphere(radius=BLOCK_SIZE / 2.0)
    self.shape.set_draw_details(shader, [partTex])
    self.shape.position(x, y, z)
    self.speed = BLOCK_SIZE
 
  def change_direction(self, direction):
    d_sum = 0
    for i in (0,1,2):
      d_sum += abs(self.direction[i] + direction[i])
    if d_sum == 0: #going back on self
      return
 
    self.direction = direction
 
  def move(self):
    if self.shape.x() >= SIZE - BLOCK_SIZE / 2.0 and self.direction == EAST:
      return False
    if self.shape.x() <= -SIZE + BLOCK_SIZE / 2.0 and self.direction == WEST:
      return False
    if self.shape.y() >= SIZE - BLOCK_SIZE / 2.0 and self.direction == UP:
      return False
    if self.shape.y() <= -SIZE + BLOCK_SIZE / 2.0 and self.direction == DOWN:
      return False
    if self.shape.z() >= SIZE - BLOCK_SIZE / 2.0 and self.direction == NORTH:
      return False
    if self.shape.z() <= -SIZE + BLOCK_SIZE / 2.0 and self.direction == SOUTH:
      return False
 
    self.shape.translate(self.direction[0] * self.speed,
                           self.direction[1] * self.speed,
                           self.direction[2] * self.speed)
 
    return True
 
class Snake:
  def __init__(self, x=0, y=0, z=0):
    self.head = Part(x, y, z)
    self.direction = NORTH
    self.length = 1
    self.parts = []
    self.parts.append(self.head)
    self.extend_flag = False
 
  def change_direction(self, direction):
    self.direction = direction
 
  def move(self, food):
    new_direction = self.direction
    old_direction = None
    new_part = None
 
    if self.extend_flag:
      last_part = self.parts[-1]
      new_part = Part(last_part.shape.x(), last_part.shape.y(),
              last_part.shape.z(), last_part.direction)
 
    for each in self.parts:
      old_direction = each.direction
      each.change_direction(new_direction)
 
      if not each.move():
        return False
 
      new_direction = old_direction
 
    if self.extend_flag:
      self.extend(new_part)
 
    for each in self.parts[1:]:
      if (each.shape.x() == self.head.shape.x() and
        each.shape.y() == self.head.shape.y() and
        each.shape.z() == self.head.shape.z()):
        return False
 
    if pi3d.Utility.distance([food.shape.x(), food.shape.y(), food.shape.z()],
          [self.head.shape.x(), self.head.shape.y(), self.head.shape.z()]) < BLOCK_SIZE:
      food.spawn()
      self.extend_flag = True
 
    return True
 
  def extend(self, part):
    self.parts.append(part)
    self.length += 1
    self.extend_flag = False

  def draw(self):
    for part in self.parts:
      part.shape.draw()

# Fetch key presses
mykeys = pi3d.Keyboard()

snake = Snake()
food = Food(snake)
CAMERA.direction = snake.direction
tilt = -15.0
rot = 0.0
rot_target = 0.0
rad = 45.0

while DISPLAY.loop_running():
  rot = 0.75 * rot + 0.25 * rot_target
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((snake.head.shape.x() + sin(radians(rot - 10)) * rad,
                   snake.head.shape.y() - sin(radians(tilt)) * rad,
                   snake.head.shape.z() - cos(radians(rot - 10))* rad))
  snake.draw()
  food.draw()
  myecube.draw()
  
  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if (k == 27): #esc
      break
    elif (k == 137): # rgt
      CAMERA.direction = TURN_RIGHT[CAMERA.direction]
      rot_target = rot_target - 90
      snake.change_direction(CAMERA.direction)
    elif (k == 136): # lft
      CAMERA.direction = TURN_LEFT[CAMERA.direction]
      rot_target = rot_target + 90
      snake.change_direction(CAMERA.direction)
    elif (k == 134): # up
      if snake.direction == DOWN or snake.direction == UP:
        snake.change_direction(CAMERA.direction)
      else:
        snake.change_direction(UP)
    elif (k == 135): # dwn
      if snake.direction == DOWN or snake.direction == UP:
        snake.change_direction(CAMERA.direction)
      else:
        snake.change_direction(DOWN)
    elif (k == 32): # sp
      snake.extend_flag = True
 
  if not snake.move(food):
    break

mykeys.close()
DISPLAY.stop()
 

