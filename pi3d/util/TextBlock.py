from __future__ import absolute_import, division, print_function, unicode_literals

""" Text block used to update contents of buffers used to draw gl_point font characters.
"""
import numpy as np
import math
import colorsys
import logging

LOGGER = logging.getLogger(__name__)
WRAP_ON = [" ", "-", "_"]

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


class TextBlockColour(object):
  def __init__(self, colour=(1.0, 1.0, 1.0, 1.0), textBlock=None):
    self.colour = [colour[0], colour[1], colour[2], colour[3]]
    self.textBlock = textBlock

  def recolour(self):
    self.set_colour()

  def set_colour(self, colour=None, alpha=None):
    if colour is not None:
      self.colour[0:len(colour)] = colour[:] # could be 3 or 4, ambiguous

    if alpha is not None:
      self.colour[3] = alpha

    textBlock = self.textBlock
    manager = textBlock._text_manager
    st = textBlock._buffer_index
    mid = st + textBlock._string_length
    end = st + textBlock.char_count
    #Reset alpha to zero for all characters.  Prevents displaying old chars from longer strings
    manager.normals[st:end, 2] = 0

    #Fill an array with the colour to copy to the manager normals
    #rotation is included for efficiency
    normal = np.zeros((3), dtype=float)
    normal[0] = textBlock.rot + textBlock.char_rot
    normal[1] = (self.colour[1] * 0.999) + (math.floor(self.colour[0] * 999))
    normal[2] = (self.colour[3] * 0.999) + (math.floor(self.colour[2] * 999))

    #Only set colour alpha for string length. Zero for non displayed characters
    manager.normals[st:mid, :] = normal


class TextBlockColourGradient(TextBlockColour):
  def __init__(self, colour1, colour2, textBlock=None):
    self.colour1 = colour1
    self.colour2 = colour2
    self.textBlock = textBlock

  def set_colour(self, colour1=None, colour2=None):
    ''' Colour each character with a gradient from colour1 to colour2
    Interpolate hsv instead of rgb since it is a more natural change.
    '''
    if colour1 is not None:
      self.colour1 = colour1
    if colour2 is not None:
      self.colour2 = colour2

    if self.textBlock is None:
      return

    colour1 = self.colour1
    colour2 = self.colour2

    textBlock = self.textBlock    
    manager = textBlock._text_manager

    hsv1 = colorsys.rgb_to_hsv(colour1[0], colour1[1], colour1[2])
    hsv2 = colorsys.rgb_to_hsv(colour2[0], colour2[1], colour2[2])
      
    normal = np.zeros((3), dtype=float)
    normal[0] = textBlock.rot + textBlock.char_rot

    tlen = textBlock._string_length # alias for brevity below
    for i in range(tlen):
      h = hsv1[0] + (hsv2[0] - hsv1[0]) * i / tlen
      s = hsv1[1] + (hsv2[1] - hsv1[1]) * i / tlen
      v = hsv1[2] + (hsv2[2] - hsv1[2]) * i / tlen
      a = colour1[3] + (colour2[3] - colour1[3]) * i / tlen

      rgb = colorsys.hsv_to_rgb(h, s, v)
      normal[1] = (rgb[1] * 0.999) + math.floor((rgb[0] * 999))
      normal[2] = (a * 0.999) + math.floor((rgb[2] * 999))

      #Only set colour alpha for string length. Zero for non displayed characters
      manager.normals[textBlock._buffer_index + i, :] = normal


class TextBlock(object):
  def __init__(self, x, y, z, rot, char_count, data_obj=None, attr=None,
            text_format="{:s}", size=0.99, spacing="C", space=1.1,
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
      Justification position. 0.0=Left, 0.5=Center, 1.0=Right
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
    self.point_size = 48

    #If the colour is a tuple initialize it a plain colour
    #Otherwise use a TextBlockColour object and its textBlock reference to this TextBlock
    if isinstance(colour, tuple):
      self.colouring = TextBlockColour(colour, self)
    else:
      self.colouring = colour
      self.colouring.textBlock = self
    self.char_rot = math.radians(char_rot)
    self.justify = justify
    self.last_value = self # hack so that static None object get initialization
    self.rotation_changed = False
    self._buffer_index = 0
    self._text_manager = None
    self._string_length = 0
    self.char_offsets = np.zeros((char_count, 3)) # x, y, char width for wrapping alignment
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

    locations = np.zeros((self.char_count, 3), dtype=float)
    (c, s) = (np.cos(self.rot), np.sin(self.rot))
    matrix = np.array([[c, -s], [s, c]])
    locations[:,:2] = matrix.dot(self.char_offsets[:,:2].T).T
    locations += pos
    st = self._buffer_index
    mid = st + self._string_length
    end = st + self.char_count
    self._text_manager.locations[st:end, :] = locations
    self._text_manager.normals[st:mid, 0] = self.rot + self.char_rot

    self._text_manager.set_do_reinit()

  def recolour(self):
    self.colouring.recolour()

  def set_text(self, text_format=None, size=None, spacing=None, space=None,
              char_rot=None, set_pos=True, set_colour=True, wrap=None, line_space=1.0,
              wrap_pixels=None):
    """ Arguments:
      *text_format*:
        text to display or a format string for displaying value from data_obj
      *size*:
        size of text 0.0 to 0.9999
      *spacing*:
        'C', 'M' or 'F'
      *space*:
        additional space between character
      *char_rot*:
        character rotation in degrees
      *set_pos*:
        control whether set_position() is called - default True
      *set_colour*:
        control whether set_colour() is called - default True
      *wrap*:
        if set then line breaks insterted to wrap at this number of characters
      *line_space*:
        multiplier for line spacing if multiline TextBlock
      *wrap_pixels*
        if set to value then lines will be wrapped to new line at this distance
        TODO only aligns accurately with spacing type F
    """
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
    self._string_length = len(strval)
    if self._string_length > self.char_count:
      LOGGER.error("'%s' needs %s characters but only space for %s",
                      strval, self._string_length, self.char_count)
      return -1
    if wrap is not None:
      strval = self.split_lines(strval, wrap)
    pos = 0.0
    spacing = 0.0 #to stop crash if zero length string
    index = 0
    #Now the string is updated set the correct glyphs and calculate the
    #character offset positions. This is not the same as the final char positions.
    const_width = 64.0 * self.size * self.space
    vari_width = 0.0
    if self.spacing == "M":
      const_width = 0.0
      vari_width = self.size * self.space
    if self.spacing == "F":
      vari_width = self.size
    lines = [[0, 0]] # [start slice, end slice]
    line_n = 0
    """scale is needed if pointsize is different in Points from Font which is
    needed to avoid clipping or overlap of corners when rotation some truetype fonts"""
    g_scale = float(self._text_manager.point_size) / self._text_manager.font.height
    line_ht = None #need to use same line height for whole thing
    for glyph in self._text_manager.font.glyph_table.values():
      line_ht = glyph[1] * g_scale
      break

    last_space = None # index of last space on this line
    for char in strval:
      if char == '\n': ## new line
        lines.append([index, index])
        pos = 0.0
        line_n += 1

      if char in self._text_manager.font.glyph_table: # skip chars not in font
        glyph = self._text_manager.font.glyph_table[char]
        self._text_manager.uv[index+self._buffer_index] = glyph[4:]
        char_offset = pos
        char_width = glyph[0] * g_scale * vari_width
        if self.spacing == "F":
          #center character to the right 
          char_offset += char_width * 0.5
        self.char_offsets[index] = [char_offset, -line_space * line_n * line_ht, char_width]
        spacing = char_width + const_width
        index += 1
        lines[line_n][1] = index
        pos += spacing
        if wrap_pixels is not None and (char in WRAP_ON or index == len(strval)): # check if last word needs wrapping
          if last_space is not None and pos > wrap_pixels: # wrap to new line
            start_c = last_space
            offset = (self.char_offsets[start_c - 1, 0] - self.char_offsets[0, 0]
                    + 0.5 * (self.char_offsets[start_c - 1, 2] + self.char_offsets[0, 2]))
            self.char_offsets[start_c:index,:2] -= [offset, line_space * line_ht]
            lines[line_n][1] = last_space # revise end of line to before this space
            last_c = (index - 2) if char == " " else index
            lines.append([start_c, last_c])
            pos = self.char_offsets[index - 1, 0] + self.char_offsets[index - 1, 2]
            line_n += 1
            last_space = None
          else:
            last_space = index
    for i in range(index, self.char_count): # if text re-used with shorter string
      self._text_manager.uv[i + self._buffer_index] = [0.0, 0.0]

    #Justification
    if len(strval) > 0: # could be passed zero length string to blank previous contents of TextBlock
      for (i, line) in enumerate(lines):
        last_c = line[1] - (2 if strval[line[1] - 1] == " " else 1)
        last_offs = self.char_offsets[last_c]
        adjust_len = last_offs[0] + 0.5 * last_offs[2]
        self.char_offsets[line[0]:line[1], 0] += adjust_len * -self.justify

    if set_pos:
      self.set_position()
    if set_colour:
      self.recolour()
    self._text_manager.set_do_reinit()

  def split_lines(self, txt, width):
    new_txt = ""
    line_len = 0
    txt_words = txt.split()
    for w in txt_words:
      len_w = len(w)
      if line_len > 0:
        if (line_len + len_w) > width:
          new_txt += "\n"
          line_len = 0
        else:
          new_txt += " "
          line_len += 1
      new_txt += w
      line_len += len_w
    return new_txt
