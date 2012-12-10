import ctypes, itertools


from pi3d import *
from pi3d.util import Utility

class Buffer(object):
  """Hold a pair of Buffer Objects to draw a part of a model"""
  def __init__(self, shape, pts, texcoords, faces, normals=None, smooth=True):
    """Generate a vertex buffer to hold data and indices"""
    self.ntiles = 0.0
    self.shiny = 0.0
    self.shape = shape

    if normals == None:
      print "Calculating normals ..."
      
      normals=[[] for p in pts]

      #Calculate normals
      for f in faces:
        a,b,c=f[0:3]

        n=tuple(Utility.vec_normal(Utility.vec_cross(Utility.vec_sub(pts[a], pts[b]), Utility.vec_sub(pts[a], pts[c]))))
        for x in f[0:3]:
          normals[x].append(n)
          
      for i,N in enumerate(normals):
        if len(N)==0:
          normals[i]=(0,0,0.01)
          continue

        if smooth:
          normals[i] = tuple(Utility.vec_normal([sum(v[k] for v in N) for k in range(3)]))
        else: #this should be slightly faster for large shapes
          normals[i] = tuple(Utility.vec_normal([N[0][k] for k in range(3)]))

    # keep a copy for speeding up the collision testing of ElevationMap
    self.vertices = pts
    self.normals = normals
    self.tex_coords = texcoords
    self.indices = faces
    self.material = (0.0, 0.0, 0.0, 0.0) #needs to be overwritten by something i.e. model loader. If it is then img texture won't be used
      
    #pack points,normals and texcoords into tuples and convert to ctype floats
    P=[ p+n+t for p,n,t in zip(pts,normals,texcoords)]
    X=c_floats([x for x in itertools.chain(*P)])

    P=[f[0:3] for f in faces]
    E=c_shorts([x for x in itertools.chain(*P)])
    
    self.vbuf = c_int()
    opengles.glGenBuffers(1,ctypes.byref(self.vbuf))
    self.ebuf = c_int()
    opengles.glGenBuffers(1,ctypes.byref(self.ebuf))
    self.select()
    opengles.glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(X), ctypes.byref(X), GL_STATIC_DRAW);
    opengles.glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(E), ctypes.byref(E), GL_STATIC_DRAW);
    self.ntris = len(faces)
    
  def select(self):
    """Makes our buffers active"""
    opengles.glBindBuffer(GL_ARRAY_BUFFER, self.vbuf);
    opengles.glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebuf);
    
  def set_draw_details(self, shader, textures, ntiles, shiny):
    self.shader = shader
    self.shape.shader = shader # set shader for parent shape
    self.textures = textures # array of Textures
    self.ntiles = ntiles
    self.shiny = shiny
    
  def draw(self, shdr=None, txtrs=None, ntl=None, shny=None):
    """ -- """
    shader = self.shader if shdr == None else shdr
    textures = self.textures if txtrs == None else txtrs
    ntiles = self.ntiles if ntl == None else ntl
    shiny = self.shiny if shny == None else shny
    
    self.select()

    opengles.glUniform1f(shader.unif_ntiles, c_float(ntiles))
    opengles.glUniform1f(shader.unif_shiny, c_float(shiny))
    
    opengles.glVertexAttribPointer(shader.attr_vertex, 3, GL_FLOAT, 0, 32, 0)
    opengles.glVertexAttribPointer(shader.attr_normal, 3, GL_FLOAT, 0, 32, 12)
    opengles.glVertexAttribPointer(shader.attr_texcoord, 2, GL_FLOAT, 0, 32, 24)
    opengles.glEnableVertexAttribArray(shader.attr_normal)
    opengles.glEnableVertexAttribArray(shader.attr_vertex)
    opengles.glEnableVertexAttribArray(shader.attr_texcoord)
    
    opengles.glDisable(GL_BLEND)
    opengles.glUniform1f(shader.unif_blend, c_float(0.6))
    if len(textures)>0:
      for t in range(0,len(textures)):
        opengles.glActiveTexture(GL_TEXTURE0 + t)
        opengles.glBindTexture(GL_TEXTURE_2D, textures[t].tex)
        opengles.glUniform1i(shader.unif_tex[t], t)
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))
        if textures[t].blend: 
          opengles.glEnable(GL_BLEND) #i.e. if any of the textures set to blend then all will for this shader
          opengles.glUniform1f(shader.unif_blend, c_float(0.05))
          
    opengles.glUniform4f(shader.unif_material, c_float(self.material[0]), c_float(self.material[1]), 
        c_float(self.material[2]), c_float(self.material[3]))
          
    shader.use()
    opengles.glDrawElements(GL_TRIANGLES, self.ntris*3, GL_UNSIGNED_SHORT, 0)

