from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from pi3d.shape.Points import Points
from pi3d.Shader import Shader
from pi3d.util.TextBlock import TextBlock

import math
import colorsys


class PointText(object):
  def __init__(self, font, camera, max_chars=100, point_size=48):
    """ Arguments:
    *font*:
      A PointFont object.
    *camera*:
      camera to use for drawing the text.  Normally a fixed 2d camera.
    *max_chars*:
      maximum number of chars, which determines the number of points in the buffer
    *point_size*:
      size of "default" characters created using the Points class and the
      font. This is further scaled by the TextBlock.size
      This refinement is needed to allow pointsize to be different in Points from
      Font to avoid clipping or overlap of corners when rotation some truetype fonts
    """
    self.max_chars = max_chars
    self.font = font
    self.shader = Shader("uv_pointsprite")
    
    self.locations = np.zeros((max_chars, 3))
    # :,2 for size and z offset. 
    # size=fract(location[2] range 0.0 to 0.999)
    # zoffset = (location[2] - size)*0.1

    self.normals = np.zeros((max_chars, 3))
    # :,0 for rotation
    # :,1 for red and green, red=normal[1]/999, green=fract(normal[1])
    # :,2 for blue and alpha, blue=normal[2]/999, alpha=fract(normal[2])    
    self.normals[:,1] = 0.0
    self.normals[:,2] = 0.0
    self.uv = np.zeros((max_chars, 2)) # u picnum.u v

    self.text_blocks = []
    self._first_free_char = 0
    self._do_buffer_reinit = False

    self.point_size = point_size
    self.text = Points(camera=camera, vertices=self.locations, normals=self.normals,
                       tex_coords=self.uv, point_size=self.point_size)
    self.text.set_draw_details(self.shader, [self.font])
    self.text.unif[48] = 0.058  # used to hold "patch size" passed to shader
    #Reset all characters to space so there are no false character shadows
    try:
      glyph = self.font.glyph_table[' '] #u' ' doesn't work on python3.2!!
    except:
      glyph = list(self.font.glyph_table.values())[0] #in case ' ' isn't there
    self.uv[:] = glyph[0:2]

  def regen(self):
    ''' Regenerate all text blocks that are linked to data objects and have
    changed value '''
    for block in self.text_blocks:
      if block.data_obj is not None:
        value = block.get_value()
        if value != block.last_value:
          block.last_value = value
          block.set_text()

  def add_text_block(self, text_block):
    ''' Add a text block to the collection, setting the object link to this
    service and setting the buffer offset allocated to the text block.
    This is required for the text block to update the buffer allocated to
    it. Also tracks the next unallocated character in the buffer. '''
    if self._first_free_char + text_block.char_count >= self.max_chars:
      print("failed to allocate space in characers for " + text_block.char_count + " characters")
      return -1
    self.text_blocks.append(text_block)
    text_block.set_text_manager(self, self._first_free_char)
    text_block.set_text()
    self._first_free_char += text_block.char_count
    return 0

  def draw(self):
    ''' Draw all the text characters.  If the re_init flag is set then
    update the points shape buffer. '''
    if self._do_buffer_reinit:
        self.text.buf[0].re_init(pts=self.locations, normals=self.normals,
                              texcoords=self.uv) # reform opengles array_buffer

    self.text.draw()

  def set_do_reinit(self):
    self._do_buffer_reinit = True


