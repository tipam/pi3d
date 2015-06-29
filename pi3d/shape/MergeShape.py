from __future__ import absolute_import, division, print_function, unicode_literals

#import ctypes
import math
import random
import numpy as np

from pi3d.constants import *
from pi3d.Buffer import Buffer

from pi3d.Shape import Shape
from pi3d.util.RotateVec import rotate_vec

class MergeShape(Shape):
  """ 3d model inherits from Shape. As there is quite a time penalty for
  doing the matrix recalculations and changing the variables being sent to
  the shader, each time an object is drawn, it is MUCH faster to use a MergeShape
  where several objects will always remain in the same positions relative to
  each other. i.e. trees in a forest.

  Where the objects have multiple Buffers, each needing a different texture
  (i.e. more complex Model objects) each must be combined into a different
  MergeShape
  """
  def __init__(self, camera=None, light=None, name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape"""
    super(MergeShape, self).__init__(camera, light, name, x, y, z,
                                   rx, ry, rz, sx, sy, sz, cx, cy, cz)

    if VERBOSE:
      print("Creating Merge Shape ...")

    self.vertices = []
    self.normals = []
    self.tex_coords = []
    self.indices = []    #stores all indices for single render

    self.buf = []
    self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))
    self.childModel = None #unused but asked for by pickle

  def merge(self, bufr, x=0.0, y=0.0, z=0.0,
            rx=0.0, ry=0.0, rz=0.0,
            sx=1.0, sy=1.0, sz=1.0):
    """merge the vertices, normals etc from this Buffer with those already there
    the position, rotation, scale, offset are set according to the origin of
    the MergeShape. If bufr is not a Buffer then it will be treated as if it
    is a Shape and its first Buffer object will be merged. Argument additional
    to standard Shape:

      *bufr*
        Buffer object or Shape with a member buf[0] that is a Buffer object.
        OR an array or tuple where each element is an array or tuple with
        the required arguments i.e. [[bufr1, x1, y1, z1, rx1, ry1....],
        [bufr2, x2, y2...],[bufr3, x3, y3...]] this latter is a more efficient
        way of building a MergeShape from lots of elements. If multiple
        Buffers are passed in this way then the subsequent arguments (x,y,z etc)
        will be ignored.
    """
    if not isinstance(bufr, list) and not isinstance(bufr, tuple):
      buflist = [[bufr, x, y, z, rx, ry, rz, sx, sy, sz]]
    else:
      buflist = bufr

    buf = self.buf[0].array_buffer # alias to tidy code
    vertices = buf[:,0:3] if len(buf) > 0 else buf
    normals = buf[:,3:6] if len(buf) > 0 else buf
    tex_coords = buf[:,6:8] if len(buf) > 0 else buf #TODO this will only cope with N_BYTES == 32
    indices = self.buf[0].element_array_buffer[:]

    for b in buflist:
      if not(type(b[0]) is Buffer):
        bufr = b[0].buf[0]
      else:
        bufr = b[0]

      n = len(bufr.array_buffer)

      if VERBOSE:
        print("Merging", bufr.name)

      original_vertex_count = len(vertices)

      vrot = rotate_vec(b[4], b[5], b[6], np.array(bufr.array_buffer[:,0:3]))
      vrot[:,0] = vrot[:,0] * b[7] + b[1]
      vrot[:,1] = vrot[:,1] * b[8] + b[2]
      vrot[:,2] = vrot[:,2] * b[9] + b[3]
      if bufr.array_buffer.shape[1] >= 6:
        nrot = rotate_vec(b[4], b[5], b[6], np.array(bufr.array_buffer[:,3:6]))
      else:
        nrot = np.zeros((n, 3))

      vertices = np.append(vertices, vrot)
      normals = np.append(normals, nrot)
      if bufr.array_buffer.shape[1] == 8:
        tex_coords = np.append(tex_coords, bufr.array_buffer[:,6:8])
      else:
        tex_coords = np.append(tex_coords, np.zeros((n, 2)))

      n = int(len(vertices) / 3)
      vertices.shape = (n, 3)
      normals.shape = (n, 3)
      tex_coords.shape = (n, 2)

      #ctypes.restype = ctypes.c_short  # TODO: remove this side-effect.
      faces = bufr.element_array_buffer + original_vertex_count
      indices = np.append(indices, faces)

      n = int(len(indices) / 3)
      indices.shape = (n, 3)

    self.buf = [Buffer(self, vertices, tex_coords, indices, normals)]
    # add some Buffer details from last one in list
    self.buf[0].shader = bufr.shader
    self.buf[0].material = bufr.material
    self.buf[0].textures = bufr.textures
    self.buf[0].draw_method = bufr.draw_method
    self.buf[0].unib = bufr.unib

  def add(self, bufr, x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
          sx=1.0, sy=1.0, sz=1.0):
    """wrapper to alias merge method"""
    self.merge(bufr, x, y, z, rx, ry, rz, sx, sy, sz)

  def cluster(self, bufr, elevmap, xpos, zpos, w, d, count, options, minscl, maxscl):
    """generates a random cluster on an ElevationMap.

    Arguments:
      *bufr*
        Buffer object to merge.
      *elevmap*
        ElevationMap object to merge onto.
      *xpos, zpos*
        x and z location of centre of cluster. These are locations RELATIVE
        to the origin of the MergeShape
      *w, d*
        x and z direction size of the cluster.
      *count*
        Number of objects to generate.
      *options*
        Deprecated.
      *minscl*
        The minimum scale value for random selection.
      *maxscl*
        The maximum scale value for random selection.
    """
    #create a cluster of shapes on an elevation map
    blist = []
    for v in range(count):
      x = xpos + random.random() * w - w * 0.5
      z = zpos + random.random() * d - d * 0.5
      rh = random.random() * (maxscl - minscl) + minscl
      rt = random.random() * 360.0
      y = elevmap.calcHeight(self.unif[0] + x, self.unif[2] + z) + rh * 2
      blist.append([bufr, x, y, z, 0.0, rt, 0.0, rh, rh, rh])
    self.merge(blist)

  def radialCopy(self, bufr, x=0, y=0, z=0, startRadius=2.0, endRadius=2.0,
                 startAngle=0.0, endAngle=360.0, step=12):
    """generates a radially copied cluster, axix is in the y direction.

    Arguments:
      *bufr*
        Buffer object to merge.

    Keyword arguments:
      *x,y,z*
        Location of centre of cluster relative to origin of MergeShape.
      *startRadius*
        Start radius.
      *endRadius*
        End radius.
      *startAngle*
        Start angle for merging 0 is in +ve x direction.
      *andAngle*
        End angle for merging, degrees. Rotation is clockwise
        looking up the y axis.
      *step*
        Angle between each copy, degrees NB *NOT* number of steps.
    """
    st = (endAngle - startAngle) / step
    rst = (endRadius - startRadius) / int(st)
    rd = startRadius
    sta = startAngle

    blist = []
    for r in range(int(st)):
      print("merging ", r)
      ca = math.cos(math.radians(sta))
      sa = math.sin(math.radians(sta))
      sta += step
      rd += rst
      blist.append([bufr, x + ca * rd, y, z + sa * rd,
                0, sta, 0, 1.0, 1.0, 1.0])

    self.merge(blist)
    print("merged all")
