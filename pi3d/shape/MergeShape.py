import random

from pi3d.pi3dCommon import *
from pi3d import Constants
from pi3d.shape.Shape import Shape

class MergeShape(Shape):
  def __init__(self,name="",
               x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(MergeShape, self).__init__(name, x, y, z, rx, ry, rz, sx, sy, sz,
                                     cx, cy, cz)

    if Constants.VERBOSE:
      print "Creating Merge Shape ..."

    self.vertices=[]
    self.normals=[]
    self.tex_coords=[]
    self.indices=[]    #stores all indices for single render
    self.shape=[]

  # TODO: this should be part of MergeShape
  def merge(self, shape, x, y, z,
            rx=0.0, ry=0.0, rz=0.0,
            sx=1.0, sy=1.0, sz=1.0,
            cx=0.0, cy=0.0, cz=0.0):
    assert shape.ttype == GL_TRIANGLES
    assert len(shape.vertices) == len(shape.normals)

    if Constants.VERBOSE:
      print "Merging", shape.name

    vertices = []
    normals = []
    original_vertex_count = len(self.vertices)

    for v in range(0, len(shape.vertices), 3):
      def rotate(array):
        vec = shape.vertices[v:v + 3]
        if rz:
          vec = rotateVecZ(rz, *vec)
        if rx:
          vec = rotateVecX(rx, *vec)
        if ry:
          vec = rotateVecY(ry, *vec)
        return vec

      # Scale, offset and store vertices
      vx, vy, vz = rotate(shape.vertices)
      self.vertices.extend([vx * sx + x, vy * sy + y, vz * sz + z])

      # Rotate normals
      self.normals.extend(rotate(shape.normals))

    self.tex_coords.extend(shape.tex_coords)

    ctypes.restype = ctypes.c_short  # TODO: remove this side-effect.
    indices = [i + original_vertex_count / 3 for i in shape.indices]
    self.indices.extend(indices)

    self.totind = len(self.indices)
    self.verts = eglfloats(self.vertices)
    self.norms = eglfloats(self.normals)
    self.texcoords = eglfloats(self.tex_coords)
    self.inds = eglshorts(self.indices)
    self.ttype = GL_TRIANGLES
    self.shape.append((eglshorts(indices), len(indices), shape.ttype))

  def add(self, shape, x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
          sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    self.merge(shape, x + shape.x, y + shape.y, z + shape.z,
               rx + shape.rotx, ry + shape.roty, rz + shape.rotz,
               sx * shape.sx, sy * shape.sy, sz * shape.sz, cx, cy, cz)

  def cluster(self,shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl):
    #create a cluster of shapes on an elevation map
    for v in range(count):
      x = xpos + random.random() * w - w * 0.5 #mapwidth*.9-mapwidth*.5
      z = zpos + random.random() * d - d * 0.5 #mapdepth*.9-mapdepth*.5
      rh = random.random() * maxscl + minscl
      rt = random.random() * 360.0
      y=elevmap.calcHeight(-x, -z) + rh * 2
      self.merge(shape, x, y, z, 0, rt, 0, rh, rh, rh)

  def radialCopy(self, shape, x=0, y=0, z=0, startRadius=2.0, endRadius=2.0,
                 startAngle=0.0, endAngle=360.0, step=12):

    st = (endAngle - startAngle) / step
    rst = (endRadius - startRadius) / int(st)
    rd = startRadius
    sta = startAngle

    for r in range(int(st)):
      ca = math.cos(sta * rad)
      sa = math.sin(sta * rad)
      self.merge(shape, x + ca * rd, y ,z + sa * rd, 0, sta, 0)
      sta += st
      rd += rst

  def draw(self, shapeNo, tex=0):
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.verts);
    opengles.glNormalPointer(GL_FLOAT, 0, self.norms);
    if tex > 0:
      texture_on(tex, self.texcoords, GL_FLOAT)
    transform(self.x, self.y, self.z, self.rotx, self.roty, self.rotz,
              self.sx, self.sy, self.sz, self.cx, self.cy, self.cz)
    opengles.glDrawElements(self.shape[shapeNo][2],
                            self.shape[shapeNo][1],
                            GL_UNSIGNED_SHORT,
                            self.shape[shapeNo][0])
    if tex > 0:
      texture_off()

  def drawAll(self, tex=0):
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.verts);
    opengles.glNormalPointer(GL_FLOAT, 0, self.norms);
    if tex > 0:
      texture_on(tex,self.texcoords,GL_FLOAT)
    opengles.glDisable(GL_CULL_FACE)
    transform(self.x, self.y, self.z, self.rotx, self.roty, self.rotz,
              self.sx, self.sy, self.sz, self.cx, self.cy, self.cz)
    opengles.glDrawElements(self.shape[0][2], len(self.indices),
                            GL_UNSIGNED_SHORT, self.inds)
    opengles.glEnable(GL_CULL_FACE)
    if tex > 0:
      texture_off()
