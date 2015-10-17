from __future__ import absolute_import, division, print_function, unicode_literals

""" Text block used to update contents of buffers used to draw gl_point font characters.
"""
import numpy as np
import math
import colorsys

def getattra(obj, attr, default):
    if("[" in attr):
        splits = attr.split("[")
        index = int(splits[1].replace("]", ""))
        thearray = getattr(obj, splits[0], None)
        if(thearray is not None):
            return thearray[index]
        else:
            return default
    else:
        return getattr(obj, attr, default)


class TextBlock(object):
  def __init__(self, x, y, z, rot, char_count, data_obj=None, attr=None,
            text_format="{:s}", size=0.25, spacing="C", space=1.1,
            colour=(1.0,1.0,1.0,1.0) , char_rot=0.0, justify=0.0):
    """ Arguments:
    *x, y, z*:
      As usual
    *rot*:
      rotation in degrees
    *char_count*:
      number of characters for this block (capacity it can expand into)
    *data_obj*:
      Data object to use in text format
    *attr*:
      Attribute in data object to use in text format
    *text_format*:
      Thetext format to use including any data formattings
    *size*:
      Size of the text 0 to 0.9999
    *spacing*:
       Type of character spacing. C=Constant, M=Multiplier, F=Fixed space between chars
    *space*:
      Value to set the spacing to
    *colour*:
      drawn colour including alpha as format (0.99, 0.99, 0.99, 0.99)
    *char_rot*:
      character rotation in degrees
    *justify*:
      Justification position. 0.0=Right, 1.0=Left, 0.5=Center
    """
    self.x = x 
    self.y = y 
    self.z = z 
    self.rot = math.radians(rot) 
    self.char_count = char_count
    self.data_obj = data_obj
    self.attr = attr
    self.text_format = text_format
    self.size = size
    self.spacing = spacing
    self.space = space
    self.colour = [colour[0],colour[1],colour[2],colour[3]]
    self.char_rot = math.radians(char_rot)
    self.justify = justify
    self.last_value = self # hack so that static None object get initialization
    self.rotation_changed = False
    self._buffer_index = 0
    self._text_manager = None
    self._string_length = 0
    self.char_offsets = [0.0] * char_count
    self._string_length = len(self.get_string(self.get_value()))

  def set_text_manager(self, manager, buffer_index):
    self._text_manager = manager
    self._buffer_index = buffer_index

  def get_value(self):
    if (self.attr is not None) and (self.data_obj is not None):
      return getattra(self.data_obj, self.attr, None)
    return None

  def get_string(self, value):    
    if value is not None:
      strval = self.text_format.format(value)
      self._string_length = len(strval)
      return strval
    return self.text_format

  def set_position(self, x=None, y=None, z=None, rot=None):
    if x is not None:
      self.x = x
    if y is not None:
      self.y = y
    if z is not None:
      self.z = z
    if rot is not None:
      self.rot = math.radians(rot) 

    size_pos, __  = math.modf(self.size)
    size_pos += math.trunc(self.z * 10.0)   # depth has resolution of 0.1m and range of 25.5m
    pos = [self.x, self.y, size_pos]

    locations = np.zeros((self.char_count, 3), dtype=np.float)
    locations[:, 0] = np.multiply(self.char_offsets, math.cos(self.rot))
    locations[:, 1] = np.multiply(self.char_offsets, math.sin(self.rot))
    locations = np.add(locations, pos)
    self._text_manager.locations[self._buffer_index:self._buffer_index + self.char_count, :] = locations
    self._text_manager.normals[self._buffer_index:self._buffer_index + self._string_length, 0] = self.rot + self.char_rot
    self._text_manager.set_do_reinit()

  def set_colour(self, colour=None, alpha=None):
    if colour is not None:
      self.colour[0:2] = colour[0:2]
    if alpha is not None:
      self.colour[3] = alpha 
    #Reset alpha to zero for all characters.  Prevents displaying old chars from longer strings
    self._text_manager.normals[self._buffer_index:self._buffer_index + self.char_count, 1] = 0

    #Fill an array with the colour to copy to the manager normals
    #rotation is included for efficiency
    normal = np.zeros((3), dtype=np.float)
    normal[0] = self.rot + self.char_rot
    normal[1] = (self.colour[1] * 0.999) + (math.floor(self.colour[0] * 999))
    normal[2] = (self.colour[3] * 0.999) + (math.floor(self.colour[2] * 999))
    #Only set colour alpha for string length. Zero for non displayed characters
    self._text_manager.normals[self._buffer_index:self._buffer_index+self._string_length, :] = normal

  def set_colour_gradient(self, colour1, colour2, alpha1=None, alpha2=None):
    ''' Colour each character with a gradient from colour1 to colour2
    Interpolate hsv instead of rgb since it is a more natural change.
    This is quite processor intensive so not intended to be dynamic
    Only compatible with static text, reposition will result in default colour
    '''
    hsv1 = colorsys.rgb_to_hsv(colour1[0], colour1[1], colour1[2])
    hsv2 = colorsys.rgb_to_hsv(colour2[0], colour2[1], colour2[2])
    normal = np.zeros((3), dtype=np.float)
    normal[0] = self.rot + self.char_rot
    if alpha1 is None:
      alpha1 = self.colour[3]
    if alpha2 is None:
      alpha2 = alpha1 

    for index in range(0,self._string_length):
      h = np.interp(index, [0,self._string_length], [hsv1[0], hsv2[0]])
      s = np.interp(index, [0,self._string_length], [hsv1[1], hsv2[1]])
      v = np.interp(index, [0,self._string_length], [hsv1[2], hsv2[2]])
      a = np.interp(index, [0,self._string_length], [alpha1, alpha2])
      rgb = colorsys.hsv_to_rgb(h, s, v)
      normal[1] = (rgb[0] * 999) + (rgb[1] * 0.999)
      normal[2] = (rgb[2] * 999) + (a * 0.999)
      #Only set colour alpha for string length. Zero for non displayed characters
      self._text_manager.normals[self._buffer_index + index, :] = normal

  def set_text(self, text_format=None, size=None, spacing=None, space=None,
              char_rot=None, set_pos=True, set_colour=True):
    if text_format is not None:
      self.text_format = text_format
    if size is not None:
      self.size = size
    if spacing is not None:
      self.spacing = spacing
    if space is not None:
      self.space = space
    if char_rot is not None:
      self.char_rot = math.radians(char_rot)
    #If there is no data object then use the simple static string value
    if self.data_obj is not None:
      value = self.get_value()
      strval = self.get_string(value)
      self.last_value = value
    else:
      strval = self.text_format
    self._string_length =len(strval)

    pos = 0.0
    index = 0
    const_width = 0.0
    vari_width = 0.0
    if self.spacing == "C":
      const_width = 64.0 * self.size * self.space
    if self.spacing == "M":
      vari_width = self.size * self.space
    if self.spacing == "F":
      vari_width = self.size
      const_width =  (64.0 * self.space * self.size)    

    for char in strval:
      glyph = self._text_manager.font.glyph_table[char]
      self._text_manager.uv[index+self._buffer_index] = glyph[4:]
      char_offset = pos
      if self.spacing == "F":
        #center character to the right 
        char_offset += float(glyph[0]) * self.size * 0.5
      self.char_offsets[index] = char_offset
      spacing = (glyph[0] * vari_width) + const_width
      pos += spacing
      index += 1
    
    #Justification
    self.char_offsets = np.add(self.char_offsets, (pos - spacing) * -self.justify)     
    if set_pos:
      self.set_position()
    if set_colour:
      self.set_colour()
    self._text_manager.set_do_reinit()
