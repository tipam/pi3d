import ctypes, itertools

from pi3d import *
from pi3d.util import Log
from pi3d.util import Utility

LOGGER = Log.logger(__name__)

class Buffer(object):
  """Hold a pair of Buffer Objects to draw a part of a model"""
  def __init__(self, shape, pts, texcoords, faces, normals=None, smooth=True):
    """Generate a vertex buffer to hold data and indices"""
    # Uniform variables all in one array!
    self.unib = (c_float * 6)(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    """ in shader array of vec3 uniform variables:
    0  ntile, shiny, blend 0-2.
    1  material 3-5 if any of material is non zero then the UV texture will not
       be used and the material shade used instead.
    """
    self.shape = shape

    if not normals:
      LOGGER.debug("Calculating normals ...")

      normals = [[] for p in pts]
      # Calculate normals.
      for f in faces:
        a, b, c = f[0:3]

        ab = Utility.vec_sub(pts[a], pts[b])
        bc = Utility.vec_sub(pts[a], pts[c])
        n = tuple(Utility.vec_normal(Utility.vec_cross(ab, bc)))
        for x in f[0:3]:
          normals[x].append(n)

      for i, n in enumerate(normals):
        if n:
          if smooth:
            norms = [sum(v[k] for v in n) for k in range(3)]
          else:  # This should be slightly faster for large shapes
            norms = [n[0][k] for k in range(3)]
          normals[i] = tuple(Utility.vec_normal(norms))
        else:
          normals[i] = 0, 0, 0.01

    # keep a copy for speeding up the collision testing of ElevationMap
    self.vertices = pts
    self.normals = normals
    self.tex_coords = texcoords
    self.indices = faces
    self.material = (0.0, 0.0, 0.0, 0.0)
    # Needs to be overwritten by something i.e. model loader. If it is then img
    # texture won't be used.

    # Pack points,normals and texcoords into tuples and convert to ctype floats.
    points = [p + n + t for p, n, t in zip(pts, normals, texcoords)]
    array_buffer = c_floats(list(itertools.chain(*points)))

    points = [f[0:3] for f in faces]
    element_array_buffer = c_shorts(list(itertools.chain(*points)))

    self.vbuf = c_int()
    opengles.glGenBuffers(1, ctypes.byref(self.vbuf))
    self.ebuf = c_int()
    opengles.glGenBuffers(1, ctypes.byref(self.ebuf))
    self.select()
    opengles.glBufferData(GL_ARRAY_BUFFER,
                          ctypes.sizeof(array_buffer),
                          ctypes.byref(array_buffer),
                          GL_STATIC_DRAW);
    opengles.glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                          ctypes.sizeof(element_array_buffer),
                          ctypes.byref(element_array_buffer),
                          GL_STATIC_DRAW);
    self.ntris = len(faces)

  def select(self):
    """Makes our buffers active"""
    opengles.glBindBuffer(GL_ARRAY_BUFFER, self.vbuf);
    opengles.glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebuf);

  def set_draw_details(self, shader, textures, ntiles = 0.0, shiny = 0.0):
    self.shader = shader
    self.shape.shader = shader # set shader for parent shape
    self.textures = textures # array of Textures
    self.unib[0] = ntiles
    self.unib[1] = shiny

  def set_material(self, mtrl):
    self.unib[3:6] = mtrl[0:3]

  def draw(self, shader=None, textures=None, ntl=None, shny=None, fullset=True):
    """ -- """
    shader = shader or self.shader
    textures = textures or self.textures
    if ntl:
      self.unib[0] = ntl
    if shny:
      self.unib[1] = shny
    self.select()

    opengles.glVertexAttribPointer(shader.attr_vertex, 3, GL_FLOAT, 0, 32, 0)
    opengles.glVertexAttribPointer(shader.attr_normal, 3, GL_FLOAT, 0, 32, 12)
    opengles.glVertexAttribPointer(shader.attr_texcoord, 2, GL_FLOAT, 0, 32, 24)
    opengles.glEnableVertexAttribArray(shader.attr_normal)
    opengles.glEnableVertexAttribArray(shader.attr_vertex)
    opengles.glEnableVertexAttribArray(shader.attr_texcoord)

    opengles.glDisable(GL_BLEND)

    self.unib[2] = 0.6
    for t, texture in enumerate(textures):
      opengles.glActiveTexture(GL_TEXTURE0 + t)
      opengles.glBindTexture(GL_TEXTURE_2D, texture.tex())
      opengles.glUniform1i(shader.unif_tex[t], t)
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               c_float(GL_LINEAR_MIPMAP_NEAREST))
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               c_float(GL_LINEAR_MIPMAP_NEAREST))
      if texture.blend:
        opengles.glEnable(GL_BLEND)
        # i.e. if any of the textures set to blend then all will for this shader.
        self.unib[2] = 0.05

    opengles.glUniform3fv(shader.unif_unib, 2, ctypes.byref(self.unib))
    opengles.glDrawElements(GL_TRIANGLES, self.ntris * 3, GL_UNSIGNED_SHORT, 0)
