from itertools import chain
from numpy import array, dot
from math import radians, pi, sin, cos

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.context.TextureLoader import TextureLoader
from pi3d.util import Utility

from pi3d.util.Loadable import Loadable

class Shape(Loadable):
  def __init__(self, camera, light, name, x, y, z, rx, ry, rz, sx, sy, sz,
               cx, cy, cz):
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

    """
    self.tr1 = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [self.x - self.cx, self.y - self.cy, self.z - self.cz, 1]])
    s, c = sin(radians(self.rotx)), cos(radians(self.rotx))
    self.rox = array([[1.0, 0.0, 0.0, 0.0],[0.0, c, s, 0.0],[0.0, -s, c, 0.0],[0.0, 0.0, 0.0, 1.0]])
    s, c = sin(radians(self.roty)), cos(radians(self.roty))
    self.roy = array([[c, 0.0, -s, 0.0],[0.0, 1.0, 0.0, 0.0],[s, 0.0, c, 0.0],[0.0, 0.0, 0.0, 1.0]])
    s, c = sin(radians(self.rotz)), cos(radians(self.rotz))
    self.roz = array([[c, s, 0.0, 0.0],[-s, c, 0.0, 0.0],[0.0, 0.0, 1.0, 0.0],[0.0, 0.0, 0.0, 1.0]])
    self.scl = array([[self.sx, 0.0, 0.0, 0.0],[0.0, self.sy, 0.0, 0.0],[0.0, 0.0, self.sz, 0.0],[0.0, 0.0, 0.0, 1.0]])
    self.tr2 = array([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[self.cx, self.cy, self.cz, 1.0]])
    """
    
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
    # if called without parameters there has to have been a previous call to set_draw_details() for all the Buffers in buf[]
    shader = self.shader if shdr == None else shdr
    """
    # calculate rotation and translation matrix for this model
    # using numpy
    mtrx = dot(self.tr1, self.camera.mtrx)
    # rot z->x->y
    if not (self.rotz == 0.0):
      mtrx = dot(self.roz, mtrx)
    if not (self.rotx == 0.0):
      mtrx = dot(self.rox, mtrx)
    if not (self.roty == 0.0):
      mtrx = dot(self.roy, mtrx)
    if not (self.sx == 1.0 and self.sy == 1.0 and self.sz == 1.0):
      mtrx = dot(self.scl, mtrx)
    mtrx = dot(self.tr2, mtrx)

    # model matrix
    M = c_floats(list(chain(*mtrx)))
    opengles.glUniformMatrix4fv(shader.unif_modelviewmatrix, 1, c_int(0), ctypes.byref(M))
    """
    # camera matrix
    C = c_floats(list(chain(*self.camera.mtrx)))
    opengles.glUniformMatrix4fv(shader.unif_cameraviewmatrix, 1, c_int(0), ctypes.byref(C))
    opengles.glUniform3f(shader.unif_eye, c_float(self.camera.eye[0]), c_float(self.camera.eye[1]), c_float(self.camera.eye[2]))
    # light rotation
    """
    s = sin(radians(self.camera.rtn[1]));
    c = cos(radians(self.camera.rtn[1]));
    rotlight = dot([[s,0,c],[0,1,0],[c,0,-s]], self.light.lightpos)
    s = sin(radians(self.camera.rtn[0]));
    c = cos(radians(self.camera.rtn[0]));
    rotlight = dot([[1,0,0],[0,s,c],[0,c,-s]], rotlight)
    """
    # matrix variables
    opengles.glUniform3f(shader.unif_locn, c_float(self.x), c_float(self.y), c_float(self.z))
    opengles.glUniform3f(shader.unif_rotn, c_float(self.rotx), c_float(self.roty), c_float(self.rotz))
    opengles.glUniform3f(shader.unif_scle, c_float(self.sx),  c_float(self.sy), c_float(self.sz))
    opengles.glUniform3f(shader.unif_ofst, c_float(self.cx), c_float(self.cy), c_float(self.cz))

    ###########
    opengles.glUniform4f(shader.unif_fogshade, c_float(self.fogshade[0]), c_float(self.fogshade[1]), 
        c_float(self.fogshade[2]), c_float(self.fogshade[3])) 
    opengles.glUniform1f(shader.unif_fogdist, c_float(self.fogdist))
    opengles.glUniform3f(shader.unif_lightpos, c_float(self.light.lightpos[0]), c_float(self.light.lightpos[1]), c_float(self.light.lightpos[2]))
    opengles.glUniform3f(shader.unif_rtn, c_float(self.camera.rtn[0]), c_float(self.camera.rtn[1]), c_float(self.camera.rtn[2]))
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
      b.ntiles = ntiles
      if shinetex != None:
        while len(b.textures) < 3:
          b.textures.append(None)
        b.textures[2] = shinetex
        b.shiny = shiny

  def set_fog(self, fogshade, fogdist):
    # set fog for this Shape only it uses the shader smoothblend function from 1/3 fogdist to fogdist
    self.fogshade = fogshade
    self.fogdist = fogdist

  def scale(self, sx, sy, sz):
    self.sx = sx
    self.sy = sy
    self.sz = sz
    """
    self.scl[0, 0] = self.sx
    self.scl[1, 1] = self.sy
    self.scl[2, 2] = self.sz
    """

  def position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    """
    self.tr1[3, 0] = self.x - self.cx
    self.tr1[3, 1] = self.y - self.cy
    self.tr1[3, 2] = self.z - self.cz
    """

  def translate(self, dx, dy, dz):
    self.x = self.x + dx
    self.y = self.y + dy
    self.z = self.z + dz
    """
    self.tr1[3, 0] = self.x - self.cx
    self.tr1[3, 1] = self.y - self.cy
    self.tr1[3, 2] = self.z - self.cz
    """

  def rotateToX(self, v):
    self.rotx = v
    """
    s, c = sin(radians(self.rotx)), cos(radians(self.rotx))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    """

  def rotateToY(self, v):
    self.roty = v
    """
    s, c = sin(radians(self.roty)), cos(radians(self.roty))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    """

  def rotateToZ(self, v):
    self.rotz = v
    """
    s, c = sin(radians(self.rotz)), cos(radians(self.rotz))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    """

  def rotateIncX(self,v):
    self.rotx += v
    """
    s, c = sin(radians(self.rotx)), cos(radians(self.rotx))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    """

  def rotateIncY(self,v):
    self.roty += v
    """
    s, c = sin(radians(self.roty)), cos(radians(self.roty))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    """

  def rotateIncZ(self,v):
    self.rotz += v
    """
    s, c = sin(radians(self.rotz)), cos(radians(self.rotz))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    """

  def add_vertex(self, vert, norm, texc):
  # add vertex,normal and tex_coords ...
    self.verts.append(vert)
    self.norms.append(norm)
    self.texcoords.append(texc)


  def add_tri(self, indx):
  # add triangle refs.
    self.inds.append(indx)
  """
  # position, rotate and scale an object
  def transform(self):
    Utility.translatef(self.x - self.cx, self.y - self.cy, self.z - self.cz)

    # TODO: why the reverse order?
    Utility.rotatef(self.rotz, 0, 0, 1)
    Utility.rotatef(self.roty, 0, 1, 0)
    Utility.rotatef(self.rotx, 1, 0, 0)
    Utility.scalef(self.sx, self.sy, self.sz)
    Utility.translatef(self.cx, self.cy, self.cz)
  """
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

