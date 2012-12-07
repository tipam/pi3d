import random, math

from pi3d import *
from pi3d import Texture
from pi3d.Buffer import Buffer

from pi3d.context.TextureLoader import TextureLoader
from pi3d.shape.Shape import Shape
from pi3d.util.RotateVec import rotate_vec_x, rotate_vec_y, rotate_vec_z

class MergeShape(Shape):
  def __init__(self, camera, light, name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(MergeShape, self).__init__(camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz,
                                     cx, cy, cz)

    if VERBOSE:
      print "Creating Merge Shape ..."

    self.vertices=[]
    self.normals=[]
    self.tex_coords=[]
    self.indices=[]    #stores all indices for single render
    #self.shape=[]


  def merge(self, shape, x, y, z,
            rx=0.0, ry=0.0, rz=0.0,
            sx=1.0, sy=1.0, sz=1.0,
            cx=0.0, cy=0.0, cz=0.0):
    # merge Buffer really. i.e. shape is Shape.buf[n]
    #TODO cope with being sent a shape = a Shape with one Buffer object or a buffer from more complex object

    #assert shape.ttype == GL_TRIANGLES # this is always true of Buffer objects
    assert len(shape.vertices) == len(shape.normals)

    if VERBOSE:
      print "Merging", shape.name

    vertices = []
    normals = []
    original_vertex_count = len(self.vertices)

    for v in range(0, len(shape.vertices)):
      def rotate_slice(array):
        vec = array[v]
        if rz:
          vec = rotate_vec_z(rz, vec)
        if rx:
          vec = rotate_vec_x(rx, vec)
        if ry:
          vec = rotate_vec_y(ry, vec)
        return vec

      # Scale, offset and store vertices
      vx, vy, vz = rotate_slice(shape.vertices)
      self.vertices.append((vx * sx + x, vy * sy + y, vz * sz + z))

      # Rotate normals
      self.normals.append(rotate_slice(shape.normals))

    self.tex_coords.extend(shape.tex_coords)

    ctypes.restype = ctypes.c_short  # TODO: remove this side-effect.
    indices = [(i[0] + original_vertex_count, i[1] + original_vertex_count, i[2] + original_vertex_count) for i in shape.indices]
    self.indices.extend(indices)

    self.buf = []
    self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))
  
  def add(self, shape, x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
          sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    self.merge(shape, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz)

  def cluster(self, shape, elevmap, xpos, zpos, w, d, count, options, minscl, maxscl):
    #create a cluster of shapes on an elevation map
    for v in range(count):
      x = xpos + random.random() * w - w * 0.5 #mapwidth*.9-mapwidth*.5
      z = zpos + random.random() * d - d * 0.5 #mapdepth*.9-mapdepth*.5
      rh = random.random() * maxscl + minscl
      rt = random.random() * 360.0
      y = elevmap.calcHeight(x, z) + rh * 2
      #self.merge(shape, x, y, z, 0, rt, 0, rh, rh, rh)
      #self.merge(shape, x,y,z, shape.rotx, rt + shape.roty, shape.rotz, 
      #    rh * shape.sx, rh * shape.sy, rh * shape.sz)
      self.merge(shape, x,y,z, 0.0, rt, 0.0, rh, rh, rh)

  def radialCopy(self, shape, x=0, y=0, z=0, startRadius=2.0, endRadius=2.0,
                 startAngle=0.0, endAngle=360.0, step=12):
    st = (endAngle - startAngle) / step
    rst = (endRadius - startRadius) / int(st)
    rd = startRadius
    sta = startAngle

    for r in range(int(st)):
      print "merging ", r
      ca = math.cos(math.radians(sta))
      sa = math.sin(math.radians(sta))
      self.merge(shape, x + ca * rd, y ,z + sa * rd, 0, sta, 0)
      sta += step
      rd += rst

    print "merged all"
