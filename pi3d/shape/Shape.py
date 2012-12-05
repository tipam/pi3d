import math, itertools

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.context.TextureLoader import TextureLoader
from pi3d.util import Utility

from pi3d.util.Loadable import Loadable

class Shape(Loadable):
  def __init__(self, camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz, cx, cy, cz):
    super(Shape, self).__init__()
    self.name = name
    self.x = x     #position
    self.y = y
    self.z = z
    self.rotx = rx #rotation
    self.roty = ry
    self.rotz = rz
    self.sx = sx   #scale
    self.sy = sy
    self.sz = sz
    self.cx = cx   #center
    self.cy = cy
    self.cz = cz
    
    self.camera = camera
    self.light = light
    self.shader = None
    self.textures = []
    self.ntiles = None
    self.shiny = None
    self.fogshade = (0.0, 0.0, 0.0, 0.0)
    self.fogdist = 0.0
    
    self.buf = []  #buffer for each part of this shape that needs rendering with a different Shader/Texture

        #this should all be done with matrices!! ... just for testing ...

  def draw(self, shdr=None, txtrs=None, ntl=None, shny=None):
    # if called without parameters there has to have been a previous call to setdrawdetails() for all the Buffers in buf[]
    shader = self.shader if shdr == None else shdr
    mtrx = Utility.transform(self.camera.mtrx, self.x, self.y, self.z, 
        self.rotx, self.roty, self.rotz, self.sx, self.sy, self.sz, self.cx, self.cy, self.cz)
    # model matrix
    M = c_floats(list(itertools.chain(*mtrx)))
    opengles.glUniformMatrix4fv(shader.unif_modelviewmatrix,16,c_int(0),ctypes.byref(M))

    C = c_floats(list(itertools.chain(*self.camera.mtrx)))
    opengles.glUniformMatrix4fv(shader.unif_cameraviewmatrix,16,c_int(0),ctypes.byref(C))
    opengles.glUniform3f(shader.unif_eye, c_float(self.camera.eye[0]), c_float(self.camera.eye[1]), c_float(self.camera.eye[2]))

    """
    # attemp to offload matrix work to shader see
    opengles.glUniform3f(shader.unif_locn, c_float(self.x), c_float(self.y), c_float(self.z))
    opengles.glUniform3f(shader.unif_rotn, c_float(self.rotx), c_float(self.roty), c_float(self.rotz))
    opengles.glUniform3f(shader.unif_scle, c_float(self.sx), c_float(self.sy), c_float(self.sz))
    opengles.glUniform3f(shader.unif_ofst, c_float(self.cx), c_float(self.cy), c_float(self.cz))
    """
  
    for b in self.buf:
      """
      Shape.draw has to be passed either parameter == None or values to pass on
      """
      b.draw(shdr, txtrs, ntl, shny) # relies on object inheriting from this creating Buffer called buf
    
  def set_shader(self, shader):
    self.shader = shader
    for b in self.buf:
      b.shader = shader    
      
  def set_normal_shine(self, normtex, ntiles = 1.0, shinetex = None, shiny = 0.0):
    for b in self.buf:
      if b.textures == None:
        b.textures = [normtex]
      while len(b.textures) < 2:
        b.textures.append(None)
      b.textures[1] = normtex
      b.ntiles = ntiles
      if shinetex != None:
        while len(b.textures) < 3:
          b.textures.append(None)
        b.textures[2] = shinetex
        b.shiny = shiny
  
  def setfog(self, fogshade, fogdist):
    # set fog for this Buffer only it uses the shader smoothblend function from 1/3 fogdist to fogdist
    self.fogshade = fogshade
    self.fogdist = fogdist
  
  def scale(self, sx, sy, sz):
    self.sx = sx
    self.sy = sy
    self.sz = sz

  def position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def translate(self, dx, dy, dz):
    self.x = self.x + dx
    self.y = self.y + dy
    self.z = self.z + dz

  def rotateToX(self, v):
    self.rotx = v

  def rotateToY(self, v):
    self.roty = v

  def rotateToZ(self, v):
    self.rotz = v

  def rotateIncX(self,v):
    self.rotx += v

  def rotateIncY(self,v):
    self.roty += v

  def rotateIncZ(self,v):
    self.rotz += v

  # TODO: should be a method on Shape.
  def add_vertex(self, vert, norm, texc):
  # add vertex,normal and tex_coords ...
    self.verts.append(vert)
    self.norms.append(norm)
    self.texcoords.append(texc)

  # TODO: should be a method on Shape.
  def add_tri(self, indx):
  # add triangle refs.
    self.inds.append(indx)

  # position, rotate and scale an object
  def transform(self):
    Utility.translatef(self.x - self.cx, self.y - self.cy, self.z - self.cz)

    # TODO: why the reverse order?
    Utility.rotatef(self.rotz, 0, 0, 1)
    Utility.rotatef(self.roty, 0, 1, 0)
    Utility.rotatef(self.rotx, 1, 0, 0)
    Utility.scalef(self.sx, self.sy, self.sz)
    Utility.translatef(self.cx, self.cy, self.cz)

  def lathe(self, path, rise=0.0, loops=1.0, tris=True):
    s = len(path)
    rl = int(self.sides * loops)
    ssize = rl * 6 * (s-1)
      
    pn = 0
    pp = 0
    tcx = 1.0 / self.sides
    pr = (math.pi / self.sides) * 2.0
    rdiv = rise / rl
    ss=0
    
    #find largest and smallest y of the path used for stretching the texture over
    miny = path[0][1]
    maxy = path[s-1][1]
    for p in range (0, s):
      if path[p][1] < miny: miny = path[p][1]
      if path[p][1] > maxy: maxy = path[p][1]
    
    verts=[]
    norms=[]
    idx=[]
    tex_coords=[]
    
    opx=path[0][0]
    opy=path[0][1]
    
    for p in range (0, s):
      
      px = path[p][0]*1.0
      py = path[p][1]*1.0
        
      tcy = 1.0 - ((py - miny)/(maxy - miny))

      #normalized 2D vector between path points
      dx, dy = Utility.vec_normal(Utility.vec_sub((px, py), (opx, opy)))

      for r in range (0, rl):
        sinr = math.sin(pr * r)
        cosr = math.cos(pr * r)
        verts.append((px * sinr,py,px * cosr))        
        norms.append((-sinr*dy,dx,-cosr*dy))
        tex_coords.append((1.0-tcx * r, tcy))
        py += rdiv
      #last path profile (tidies texture coords)
      verts.append((0,py,px))
      norms.append((0,dx,-dy))
      tex_coords.append((0,tcy))
      
      if p < s-1:      
        pn += (rl+1)
        for r in range (0, rl):
          idx.append((pp+r+1,pp+r,pn+r))
          idx.append((pn+r,pn+r+1,pp+r+1))
        pp += (rl+1)
          
      opx=px
      opy=py
      
      #print verts,norms,idx
    buf = Buffer(self, verts, tex_coords, idx, norms)
    return buf


def normalize_vector(begin, end):
  diff = [e - b for b, e in zip(begin, end)]
  mag = Utility.magnitude(*diff)
  mult = 1 / mag if mag > 0.0 else 0.0
  return [x * mult for x in diff]

