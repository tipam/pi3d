#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
''' 
'''
import pi3d
import numpy as np
import logging

LOGGER = logging.getLogger(__name__)

class Graph(object):
  '''Providing some basic functionality for a GPU accelerated x, y graph
  (i.e. for real-time display of instrumentation data etc)'''
  def __init__(self, x_values, y_values, width, height, font, title=None, 
              line_width=2, axes_desc=None, legend=None, xpos=0, ypos=0,
              xmin=None, xmax=None, ymin=None, ymax=None, camera=None,
              shader=None):
    '''
    Arguments:
        *x_values*
          1D numpy array
        *y_values*
          1 or 2D numpy array with size same as x_values in 2nd D draws
          a line graph
          or 3D numpy array with size same as x along axis=1 and last axis
          has 2 values. In this case the graph is drawn as vertical lines
        *width, height*
          as expected
        *font*
          pi3d.Font instance
        *title, line_width*
          as expected
        *axes_desc*
          tuple -> (x.axis.desc, y.axis.desc)
        *legend*
          tuple -> (y0.desc, y1.desc, y2.desc...)
        *xpos, ypos*
          offset relative to origin of display (centre)
        *xmin, xmax, ymin, ymax*
          override sampled values from init data
        *camera*
          if no other Shape to be drawn then a 2D Camera can be created here
        *shader*
          if no other Shape uses mat_flat shader then one will be created
    '''
    if len(y_values.shape) < 2:
      y_values.shape = (1,) + y_values.shape
    if x_values.shape[0] != y_values.shape[1]:
      LOGGER.error('mismatched array lengths')
      return
    if camera is None:
      camera = pi3d.Camera(is_3d=False)
    if shader is None:
      shader = pi3d.Shader('mat_flat')
    # title ##########
    point_size = max(min(48, int(height * 0.1)), 24)
    self.text = pi3d.PointText(font, camera, max_chars=400, point_size=point_size)
    if title is not None:
      title = pi3d.TextBlock(x=xpos, y=ypos+height/2-point_size+5, 
                    z=0.1, rot=0.0, char_count=len(title) + 2, spacing='F',
                    text_format=title, space=0.05, justify=0.5)
      self.text.add_text_block(title)
    # axes ###########
    axex, axey = width * 0.4, height * 0.4 # implies 10% margin all round
    self.axes = pi3d.Lines(vertices=[[axex, -axey-line_width, 0],
                                [-axex-line_width, -axey-line_width, 0],
                                [-axex-line_width, axey, 0]],
                                x=xpos, y=ypos, z=5.0, line_width=line_width)
    self.axes.set_shader(shader)
    # lines to represent data
    n = x_values.shape[-1]
    if xmin is None:
      xmin = x_values.min()
    if xmax is None:
      xmax = x_values.max()
    x_factor =  (2.0 * axex) / (xmax - xmin)
    x_offset = xmin
    if ymin is None:
      ymin = y_values.min()
    if ymax is None:
      ymax = y_values.max()
    y_factor =  (2.0 * axey) / (ymax - ymin)
    y_offset = ymin
    self.lines = []
    for i in range(y_values.shape[0]):
      data = np.zeros((n, 3))
      data[:,0] = (x_values - x_offset) * x_factor - axex + xpos
      if len(y_values[i].shape) == 1: # i.e. normal line graph
        data[:,1] = (y_values[i] - y_offset) * y_factor - axey + ypos
        strip = True
      else: # has to be pairs of values for separate line segments
        xx_vals = np.stack([data[:,0], data[:,0]], axis=1).flatten() # make x into pairs
        data = np.zeros((n * 2, 3))
        data[:,0] = xx_vals
        data[:,1] = (y_values[i].flatten() - y_offset) * y_factor - axey + ypos
        strip = False
      data[:,2] = 4.0 # z value
      line = pi3d.Lines(vertices=data, line_width=line_width, strip=strip)
      line.set_shader(shader)
      j = i + 1
      rgb_val = (0.913 * j % 1.0, 0.132 * j % 1.0, 0.484 * j % 1.0)
      line.set_material(rgb_val)
      self.lines.append(line)
    # axis values
    point_size *= 0.3
    # first add the max and min vals
    vals = [(-axex + xpos, -axey + ypos - point_size, '{:.3g}'.format(xmin), 0.0),
             (axex + xpos, -axey + ypos - point_size, '{:.3g}'.format(xmax), 0.0),
             (-axex + xpos - point_size, -axey + ypos, '{:.3g}'.format(ymin), 90.0),
             (-axex + xpos - point_size, axey + ypos, '{:.3g}'.format(ymax), 90.0)]
    data = [] # use this to hold vertex positions for grid lines (called ticks)
    for val in self.tick_pos(xmin, xmax):
      x = (val - x_offset) * x_factor - axex
      vals.append((x + xpos, -axey + ypos - point_size, '{:.3g}'.format(val), 0.0))
      data.extend([[x, -axey, 0],[x, axey, 0]]) 
      # NB points in pairs to use GL_LINES option with strip=False below.
    for val in self.tick_pos(ymin, ymax):
      y = (val - y_offset) * y_factor - axey
      vals.append((-axex + xpos - point_size, y + ypos, '{:.3g}'.format(val), 90.0))
      data.extend([[-axex, y, 0],[axex, y, 0]])
    for val in vals:
      self.text.add_text_block(pi3d.TextBlock(val[0], val[1], 4.0, val[3], 8, 
                          size=0.7, text_format=val[2], spacing='F', space=0.05, justify=0.5))
    self.ticks = pi3d.Lines(vertices=data, x=xpos, y=ypos, z=5.0, line_width=line_width,
                            material=(0.5, 0.5, 0.5), strip=False)
    self.ticks.set_shader(shader)
    # axes descritions
    if axes_desc is not None:
      self.text.add_text_block(pi3d.TextBlock(xpos, ypos - 1.15 * axey, 4.0, 0.0, len(axes_desc[0]) + 2, 
                          size=0.7, text_format=axes_desc[0], spacing='F', space=0.05, justify=0.5))
      self.text.add_text_block(pi3d.TextBlock(xpos - 1.15 * axex, ypos, 4.0, 90.0, len(axes_desc[1]) + 2, 
                          size=0.7, text_format=axes_desc[1], spacing='F', space=0.05, justify=0.5))
    # legend ##########
    if legend is not None:
      if not hasattr(legend, '__iter__'): # single string, make into list
        legend = [legend]
      for i, lgd in enumerate(legend):
        self.text.add_text_block(pi3d.TextBlock(axex + xpos, axey + ypos - (i + 1) * point_size * 2.0,
                    4.0, 0.0, len(lgd) + 2, size=0.8, text_format=lgd, spacing='F', space=0.05, 
                    justify=1.0, colour=tuple(self.lines[i].buf[0].unib[3:6]) + (1.0,)))
    # scale factors for use in update() so add to self
    self.y_offset = y_offset
    self.y_factor = y_factor
    self.axey = axey
    self.ypos = ypos

  def draw(self):
    self.text.draw()
    self.axes.draw()
    self.ticks.draw()
    for line in self.lines:
      line.draw()

  def update(self, y_values):
    ''' update all y_values
    '''
    if len(y_values.shape) < 2: # in case single line
      y_values.shape = (1,) + y_values.shape
    for i in range(y_values.shape[0]):
      self.lines[i].buf[0].array_buffer[:,1] = (y_values[i].flatten() - self.y_offset) * self.y_factor - self.axey + self.ypos
      self.lines[i].re_init()

  def tick_pos(self, minv, maxv, num=3):
    ''' work out nice looking grid line positions
    '''
    steps = np.array([1.0, 2.0, 2.5, 5.0, 10.0])
    span = maxv - minv
    d = span / (num + 1)
    d_exp = np.floor(np.log10(abs(d)))
    d_man = d / 10 ** d_exp
    diffs = np.abs((d_man - steps) / steps)
    st = steps[np.argmin(diffs)] * 10 ** d_exp
    val = np.floor((minv + st + span * 0.1) / st) * st
    vals = []
    while val < (maxv - span * 0.1):
      vals.append(val)
      val += st
    return vals
