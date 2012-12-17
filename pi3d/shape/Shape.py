from itertools import chain
from numpy import array, dot
from math import radians, pi, sin, cos

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.context.TextureLoader import TextureLoader
from pi3d.util import Utility

from pi3d.util.Loadable import Loadable

class Shape(Loadable):
  def __init__(self, camera, light, name, x, y, z,   rx, ry, rz,   sx, sy, sz,   cx, cy, cz):
    super(Shape, self).__init__()
    self.name = name
    # uniform variables all in one array!
    self.unif = (c_float * 33)(x,y,z, rx,ry,rz, sx,sy,sz, cx,cy,cz, 0.5,0.5,0.5, 200.0,0.8,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0,
      light.lightpos[0], light.lightpos[1], light.lightpos[2], 1.0,1.0,1.0, 0.1,0.1,0.1)
    """ in shader array of vec3 uniform variables:
    0  location 0-2
    1  rotation 3-5
    2  scale 6-8
    3  offset 9-11
    4  fog shade 12-14
    5  fog distance and alph (only first two values used at moment) 15, 16
    6  camera position  18-20
    7  camera rotation 21-23
    8  light position, direction vector (if capacity for more lights is added these would go on the end of this list) 24-26
    9  light strength per shade 27-29
    10 light ambient values 30-32
    """

    self.camera = camera
    self.light = light
    self.shader = None
    self.textures = []

    self.buf = []  #buffer for each part of this shape that needs rendering with a different Shader/Texture

        #this should all be done with matrices!! ... just for testing ...

  def draw(self, shdr=None, txtrs=None, ntl=None, shny=None):
    # if called without parameters there has to have been a previous call to set_draw_details() for all the Buffers in buf[]
    shader = self.shader if shdr == None else shdr

    # camera matrix
    if self.camera.movedFlag:
      if self.camera.C == None:
        self.camera.C = c_floats(list(chain(*self.camera.mtrx)))
      opengles.glUniformMatrix4fv(shader.unif_cameraviewmatrix, 1, c_int(0), ctypes.byref(self.camera.C))
      self.unif[18], self.unif[19], self.unif[20] = c_float(self.camera.eye[0]), c_float(self.camera.eye[1]), c_float(self.camera.eye[2])
      self.unif[21], self.unif[22], self.unif[23] = c_float(self.camera.rtn[0]), c_float(self.camera.rtn[1]), c_float(self.camera.rtn[2])

    # variables for movement of this object
    opengles.glUniform3fv(shader.unif_unif, 11, ctypes.byref(self.unif))

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
      if b.textures == None or len(b.textures) == 0:
        b.textures = [normtex]
      while len(b.textures) < 2:
        b.textures.append(None)
      b.textures[1] = normtex
      b.unib[0] = ntiles
      if shinetex != None:
        while len(b.textures) < 3:
          b.textures.append(None)
        b.textures[2] = shinetex
        b.unib[1] = shiny

  def set_fog(self, fogshade, fogdist):
    # set fog for this Shape only it uses the shader smoothblend function from 1/3 fogdist to fogdist
    self.unif[12], self.unif[13], self.unif[14] = fogshade[0], fogshade[1], fogshade[2]
    self.unif[15] = fogdist

  def scale(self, sx, sy, sz):
    self.unif[6], self.unif[7], self.unif[8] = sx, sy, sz
    
  def position(self, x, y, z):
    self.unif[0], self.unif[1], self.unif[2] = x, y, z

  def positionX(self, v):
    self.unif[0] = v

  def positionY(self, v):
    self.unif[1] = v

  def positionZ(self, v):
    self.unif[2] = v

  def translate(self, dx, dy, dz):
    self.unif[0] += dx
    self.unif[1] += dy
    self.unif[2] += dz

  def translateX(self, v):
    self.unif[0] += v

  def translateY(self, v):
    self.unif[1] += v

  def translateZ(self, v):
    self.unif[2] += v

  def rotateToX(self, v):
    self.unif[3] = v

  def rotateToY(self, v):
    self.unif[4] = v

  def rotateToZ(self, v):
    self.unif[5] = v

  def rotateIncX(self,v):
    self.unif[3] += v

  def rotateIncY(self,v):
    self.unif[4] += v

  def rotateIncZ(self,v):
    self.unif[5] += v

  def add_vertex(self, vert, norm, texc):
  # add vertex,normal and tex_coords ...
    self.verts.append(vert)
    self.norms.append(norm)
    self.texcoords.append(texc)


  def add_tri(self, indx):
  # add triangle refs.
    self.inds.append(indx)

  def lathe(self, path, rise=0.0, loops=1.0, tris=True):
    s = len(path)
    rl = int(self.sides * loops)
    ssize = rl * 6 * (s-1)

    pn = 0
    pp = 0
    tcx = 1.0 / self.sides
    pr = (pi / self.sides) * 2.0
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
        sinr = sin(pr * r)
        cosr = cos(pr * r)
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

