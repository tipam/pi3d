#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes
import numpy as np
import math

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.Camera import Camera
from pi3d.shape.Sprite import Sprite
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Display import Display
from pi3d import opengles

class StereoCam(object):
  """For creating an apparatus with two sprites to hold left and right
  eye views.

  This Class is used to hold the 3D Camera which should be used to draw
  the 3D objects. It also holds a 2D Camera for drawing the Sprites"""
  def __init__(self, shader="uv_flat", mipmap=False, separation=0.4, interlace=0):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer. Keyword Arguments:

      *shader*
        to use when drawing sprite, defaults to uv_flat.

      *mipmap*
        can be set to True with slight cost to speed, or use fxaa shader

      *separation*
        distance between the two camera positions - how wide apart the
        eye views are.

      *interlace*
        if interlace > 0 then the images are not taken with glScissor and
        must be drawn with a special interlacing shader.
    """
    # load shader
    if interlace <= 0: # i.e. default side by side behaviour
      self.shader = Shader(shader)
    else:
      self.shader = Shader(vshader_source = """
precision mediump float;
attribute vec3 vertex;
attribute vec2 texcoord;
uniform mat4 modelviewmatrix[2];
varying vec2 texcoordout;
void main(void) {
  texcoordout = texcoord;
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
    """, fshader_source = """
precision mediump float;
uniform sampler2D tex0;
uniform sampler2D tex1;
varying vec2 texcoordout;
void main(void) {{
  vec4 texc0 = texture2D(tex0, texcoordout);
  vec4 texc1 = texture2D(tex1, texcoordout);
  vec2 coord = vec2(gl_FragCoord);
  gl_FragColor = mix(texc0, texc1, step(0.5, fract(coord.x / {:f})));
}}
    """.format(interlace * 2.0))

    self.camera_3d = Camera() # create 3d cam first so it becomes default instance
    self.forMtrx = np.identity(4, dtype='float32') # initially not rotated
    self.position = [0.0, 0.0, 0.0]
    self.camera_2d = Camera(is_3d=False)
    self.offs = separation / 2.0
    self.interlace = interlace
    self.textures = []
    self.sprites = []
    self.tex_list = []
    for i in range(2):
      self.textures.append(OffScreenTexture(name="stereo"))
      ix, iy = self.textures[i].ix, self.textures[i].iy
      #two sprites full width but moved so that they are centred on the
      #left and right edges. The offset values then move the uv mapping
      #so the image is on the right of the left sprite and left of the
      #right sprite
      self.sprites.append(Sprite(z=20.0, w=ix, h=iy, flip=True))
      if interlace <= 0:
        self.sprites[i].positionX(-ix/2.0 + i*ix)
        self.sprites[i].set_offset((i * 0.5 - 0.25, 0.0))
      else:
        self.sprites[i].set_2d_size(w=ix, h=iy)
      self.textures[i].blend = True
      self.textures[i].mipmap = mipmap
      self.tex_list.append(self.textures[i])
    opengles.glColorMask(1, 1, 1, 1)

  def move_camera(self, position, rot, tilt, roll=0.0, absolute=True):
    ''' Arguments:
    
      *position*
        array [x,y,z]

      *rot, tilt, roll*
        rotations about y, x, z axis (yes it's not entirely logical for position
        to be an array and orientation three values but it's too late to change!)

      *absolute*
        if set to False then the rotations are treated as relative to the
        rotated frame of reference i.e. as if signals from VR headset 3
        axis gyro.
    '''
    self.camera_3d.rotate(tilt, rot, roll)
    self.camera_3d.position(position)
    self.camera_3d.absolute = absolute
    
  def start_capture(self, side):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display.

      *side*
        Either 0 or 1 to determine stereoscopic view
    """
    self.camera_3d.reset()
    offs = -self.offs if side == 0 else self.offs
    self.camera_3d.offset([offs, 0.0, 0.0])
    #self.camera_3d.mtrx = np.dot(self.forMtrx, self.camera_3d.mtrx)
    #self.camera_3d.position(self.position)
    tex = self.textures[side]
    tex._start()
    if self.interlace <= 0:
      xx = tex.ix / 4.0 # draw the middle only - half width
      yy = 0
      ww = tex.ix / 2.0
      hh = tex.iy
      opengles.glEnable(GL_SCISSOR_TEST)
      opengles.glScissor(ctypes.c_int(int(xx)), ctypes.c_int(int(yy)),
                    ctypes.c_int(int(ww)), ctypes.c_int(int(hh)))

  def end_capture(self, side):
    """ stop capturing to texture and resume normal rendering to default
    """
    self.textures[side]._end()
    if self.interlace <= 0:
      opengles.glDisable(GL_SCISSOR_TEST)

  def draw(self):
    """ draw the shape using the saved texture
    """
    if self.interlace <= 0:
      for i in range(2):
        self.sprites[i].draw(self.shader, [self.tex_list[i]], 0.0, 0.0, self.camera_2d)
    else:
      self.sprites[0].draw(self.shader, self.tex_list, 0.0, 0.0, self.camera_2d)
      
  def get_direction(self):
    return self.camera_3d.get_direction()

