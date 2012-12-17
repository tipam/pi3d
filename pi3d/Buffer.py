import ctypes, itertools


from pi3d import *
from pi3d.util import Utility

class Buffer(object):
  """Hold a pair of Buffer Objects to draw a part of a model"""
  def __init__(self, shape, pts, texcoords, faces, normals=None, smooth=True):
    """Generate a vertex buffer to hold data and indices"""
    # uniform variables all in one array!
    self.unib = (c_float * 6)(0.0,0.0,0.0, 0.0,0.0,0.0)
    """ in shader array of vec3 uniform variables:
    0  ntile, shiny, blend 0-2
    1  material 3-5 if any of material is non zero then the UV texture will not be used and the material shade used instead
    """
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
    
  def set_draw_details(self, shader, textures, ntiles = 0.0, shiny = 0.0):
    self.shader = shader
    self.shape.shader = shader # set shader for parent shape
    self.textures = textures # array of Textures
    self.unib[0] = ntiles
    self.unib[1] = shiny
  
  def set_material(self, mtrl):
    self.unib[3], self.unib[4], self.unib[5] = mtrl[0], mtrl[1], mtrl[2]
    
  def draw(self, shdr=None, txtrs=None, ntl=None, shny=None, fullset=True):
    """ -- """
    shader = self.shader if shdr == None else shdr
    textures = self.textures if txtrs == None else txtrs
    if ntl != None: self.unib[0] = ntl
    if shny != None: self.unib[1] = shny
    self.select()
    shader.use()
    
    opengles.glVertexAttribPointer(shader.attr_vertex, 3, GL_FLOAT, 0, 32, 0)
    opengles.glVertexAttribPointer(shader.attr_normal, 3, GL_FLOAT, 0, 32, 12)
    opengles.glVertexAttribPointer(shader.attr_texcoord, 2, GL_FLOAT, 0, 32, 24)
    opengles.glEnableVertexAttribArray(shader.attr_normal)
    opengles.glEnableVertexAttribArray(shader.attr_vertex)
    opengles.glEnableVertexAttribArray(shader.attr_texcoord)
    
    opengles.glDisable(GL_BLEND)
    self.unib[2] = 0.6
    if len(textures)>0:
      for t in range(0,len(textures)):
        opengles.glActiveTexture(GL_TEXTURE0 + t)
        opengles.glBindTexture(GL_TEXTURE_2D, textures[t].tex)
        opengles.glUniform1i(shader.unif_tex[t], t)
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))
        if textures[t].blend: 
          opengles.glEnable(GL_BLEND) #i.e. if any of the textures set to blend then all will for this shader
          self.unib[2] = 0.05
          
    opengles.glUniform3fv(shader.unif_unib, 2, ctypes.byref(self.unib)) # have to do this after checking textures for blend set in unib[0][2]
    
    #opengles.glDrawElements(GL_TRIANGLES, self.ntris*3, GL_UNSIGNED_SHORT, 0)
    self.glDraw()

  def glDraw(self):
    opengles.glDrawElements(GL_TRIANGLES, self.ntris*3, GL_UNSIGNED_SHORT, 0)
