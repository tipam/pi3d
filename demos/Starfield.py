#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Use of points by using set_point_size() to a non-zero value. There is
no attempt to 'tile' the points to give continuous motion
"""
import random
import demo
import pi3d
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50)
DISPLAY.set_background(0,0,0,1)    	# r,g,b,alpha
shader = pi3d.Shader("shaders/uv_reflect")
flatsh = pi3d.Shader("shaders/uv_flat")
matsh = pi3d.Shader("shaders/mat_flat")

earthimg = pi3d.Texture("textures/world_map.jpg")
starsimg = pi3d.Texture("textures/stars.jpg")
# Load shapes
mysphere = pi3d.Sphere(radius=2, slices=24, sides=24,
                  name="earth", x=10, y=-5, z=180)
mysphere.set_draw_details(shader, [earthimg])
myplane = pi3d.Plane(w=500, h=500, name="stars", z=400)
myplane.set_draw_details(flatsh, [starsimg])

"""create the shape to hold the points. This could be encapsulated in its
own class to generate the required distribution and shield the user from
having to explicitly create the Buffer object and set the Shape.buf list
"""
mystars = Shape(None, None, "stars", 0, 0, 250,
               0, 0, 0, 100, 100, 500, 0, 0, 0)
verts, norms, texc, faces = [], [], [], []
for i in xrange(30000):
  verts.append((random.random() - 0.5, random.random() - 0.5, random.random() - 0.5))
  norms.append((0,0,0))
  texc.append((0,0))
for i in xrange(10000):
  faces.append((i*3, i*3 + 1, i*3 + 2))
mystars.buf = [Buffer(mystars, verts, texc, faces, norms)]
mystars.set_point_size(50)
mystars.set_material((0.9, 0.9, 1.0))
mystars.set_shader(matsh)

# Fetch key presses
mykeys = pi3d.Keyboard()
# Display scene
while DISPLAY.loop_running():
  mysphere.rotateIncY(-0.5)
  mysphere.positionZ(mysphere.z() - 0.5)
  mystars.positionZ(mystars.z() - 0.5)
  if mystars.z() < 75:
    mystars.positionZ(250)
    mysphere.positionZ(180)
  mystars.draw()
  mysphere.draw()
  myplane.draw()
  
  k = mykeys.read()
  if k >-1:
    if k==112:
      pi3d.screenshot("earth1.jpg")
    elif k==27:
      mykeys.close()
      DISPLAY.stop()
      break
  

