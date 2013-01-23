import ctypes

from itertools import chain
from numpy import array, dot, ravel
from math import radians, pi, sin, cos

from pi3d.constants import *
from pi3d.Buffer import Buffer
from pi3d.context.Light import Light
from pi3d.util import Utility

from pi3d.util.Loadable import Loadable

class Shape(Loadable):
  """inherited by all shape objects, including simple 2D sprite types"""
  def __init__(self, camera, light, name, x, y, z,
               rx, ry, rz, sx, sy, sz, cx, cy, cz):
    """
    Arguments:
    camera -- Camera instance if None then a default instance will be created
    light -- Light instance if None then default instance will be created
    name -- handy string
    x, y, z, -- location of the origin of the shape, stored in unif array
    rx, ry, rz -- rotation of shape in degrees about each axis
    sx, sy, sz -- scale in each direction
    cx, cy, cz -- offset vertices from origin in each direction
    """
    super(Shape, self).__init__()
    self.name = name
    light = light or Light.instance()
    # uniform variables all in one array (for Shape and one for Buffer)
    self.unif = (ctypes.c_float * 48)(
      x, y, z, rx, ry, rz,
      sx, sy, sz, cx, cy, cz,
      0.5, 0.5, 0.5, 5000.0, 0.8, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      light.lightpos[0], light.lightpos[1], light.lightpos[2],
      light.lightcol[0], light.lightcol[1], light.lightcol[2],
      light.lightamb[0], light.lightamb[1], light.lightamb[2])
    """ in shader array of vec3 uniform variables:
    0  location 0-2
    1  rotation 3-5
    2  scale 6-8
    3  offset 9-11
    4  fog shade 12-14
    5  fog distance and alph (only first two values used at moment) 15, 16
    6  camera position  18-20
    7  animation offets x, y, delta 21-23
    8  light0 position, direction vector 24-26
    9  light0 strength per shade 27-29
    10 light0 ambient values 30-32
    11 light1 position, direction vector 33-35
    12 light1 strength per shade 36-38
    13 light1 ambient values 39-41
    14 defocus dist, amount 42,43
    15 defocus frame width, height 45,46
    """
    """Shape holds matrices which are updated each time it is moved or rotated
    this saves time recalculating them each frame as the Shape is drawn
    """
    """translate to position - offset"""
    self.tr1 = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [self.unif[0] - self.unif[9], self.unif[1] - self.unif[10], self.unif[2] - self.unif[11], 1.0]])
    """rotate about x axis"""
    s, c = sin(radians(self.unif[3])), cos(radians(self.unif[3]))
    self.rox = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, c, s, 0.0],
                      [0.0, -s, c, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    """rotate about y axis"""
    s, c = sin(radians(self.unif[4])), cos(radians(self.unif[4]))
    self.roy = array([[c, 0.0, -s, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [s, 0.0, c, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    """rotate about z axis"""
    s, c = sin(radians(self.unif[5])), cos(radians(self.unif[5]))
    self.roz = array([[c, s, 0.0, 0.0],
                      [-s, c, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    """scale"""
    self.scl = array([[self.unif[6], 0.0, 0.0, 0.0],
                      [0.0, self.unif[7], 0.0, 0.0],
                      [0.0, 0.0, self.unif[8], 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    """translate to offset"""
    self.tr2 = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [self.unif[9], self.unif[10], self.unif[11], 1.0]])
    self.MFlg = True
    self.M = (ctypes.c_float * 32)(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    self._camera = camera
    self.shader = None
    self.textures = []

    self.buf = []
    """self.buf contains a buffer for each part of this shape that needs
    rendering with a different Shader/Texture. self.draw() relies on objects
    inheriting from this filling buf with at least one element.
    """
  def draw(self, shader=None, txtrs=None, ntl=None, shny=None, camera=None):
    """If called without parameters, there has to have been a previous call to
    set_draw_details() for each Buffer in buf[].
    NB there is no facility for setting umult and vmult with draw they must be
    set using set_draw_details or Buffer.set_draw_details
    """
    from pi3d.Camera import Camera

    camera = camera or self._camera or Camera.instance()
    shader = shader or self.shader
    shader.use()

    if self.MFlg == True:
      # Calculate rotation and translation matrix for this model using numpy.
      self.MRaw = dot(self.tr2,
        dot(self.scl,
        dot(self.roy,
        dot(self.rox,
        dot(self.roz, self.tr1)))))
      self.M[0:16] = self.MRaw.ravel()
      self.M[16:32] = dot(self.MRaw, camera.mtrx).ravel()
      self.MFlg = False

    elif camera.was_moved:
      # Only do this if it's not done because model moved.
      self.M[16:32] = dot(self.MRaw, camera.mtrx).ravel()

    if camera.was_moved:
      self.unif[18:21] = camera.eye[0:3]

    opengles.glUniformMatrix4fv(shader.unif_modelviewmatrix, 2,
                                ctypes.c_int(0),
                                ctypes.byref(self.M))

    opengles.glUniform3fv(shader.unif_unif, 16, ctypes.byref(self.unif))
    for b in self.buf:
      # Shape.draw has to be passed either parameter == None or values to pass
      # on.
      b.draw(shader, txtrs, ntl, shny)

  def set_shader(self, shader):
    self.shader = shader
    for b in self.buf:
      b.shader = shader

  def set_normal_shine(self, normtex, ntiles=1.0, shinetex=None,
                       shiny=0.0, is_uv=True):
    """used to set some of the draw details for all Buffers in Shape
    this is useful where a Model object has been loaded from an obj file and
    the textures assigned automatically

    Arguments:
    normtex -- normal map Texture to use

    Keyword arguments:
    ntiles -- multiplier for the tiling of the normal map
    shinetex -- reflection Texture to use
    shiny -- 0.0 to 1.0 strength of reflection
    is_uv -- if True then the normtex will be textures[1] and shinetex will be
          textures[2] i.e. for using a uv_ type Shader. However for mat_ type
          Shaders they are moved down one as the basic shade is defined by
          material rgb rather than from a Texture
    """
    ofst = 0 if is_uv else -1
    for b in self.buf:
      b.textures = b.textures or []
      if is_uv and not b.textures:
        b.textures = [normtex]
      while len(b.textures) < (2 + ofst):
        b.textures.append(None)
      b.textures[1 + ofst] = normtex
      b.unib[0] = ntiles
      if shinetex:
        while len(b.textures) < (3 + ofst):
          b.textures.append(None)
        b.textures[2 + ofst] = shinetex
        b.unib[1] = shiny

  def set_draw_details(self, shader, textures, ntiles = 0.0, shiny = 0.0, 
                      umult=1.0, vmult=1.0):
    """wrapper to call set_draw_details() in each Buffer object
    Arguments:
    shader -- Shader object
    textures -- array of Texture objects
    """
    self.shader = shader
    for b in self.buf:
      b.set_draw_details(shader, textures, ntiles, shiny, umult, vmult)

  def set_material(self, mtrl):
    """ wrapper for setting material shade in each Buffer object
    Arguments:
    mtrl -- tuple (rgb)
    """
    for b in self.buf:
      b.set_material(mtrl)

  def set_fog(self, fogshade, fogdist):
    """Set fog for this Shape only, it uses the shader smoothblend function from
    1/3 fogdist to fogdist.
    Arguments:
    fogshade -- tuple (rgba)
    fogdist -- distance from Camera at which Shape is 100% fogshade
    """
    self.unif[12:15] = fogshade[0:3]
    self.unif[15] = fogdist
    self.unif[16] = fogshade[3]

  def set_light(self, light, num=0):
    """Set the values of the lights
    Arguments:
    light -- Light object to use
    num -- number of the light to set
    """
    #TODO (pg) need MAXLIGHTS global variable, room for two now but shader
    # only uses 1. Also shader doesn't use light colour or ambient colour
    if num > 1 or num < 0:
      num = 0
    stn = 24 + num * 9
    self.unif[stn:(stn + 3)] = light.lightpos[0:3]
    self.unif[(stn + 3):(stn + 6)] = light.lightcol[0:3]
    self.unif[(stn + 6):(stn + 9)] = light.lightamb[0:3]
    
  def set_2d_size(self, w=None, h=None, x=0, y=0):
    from pi3d.Display import DISPLAY
    if w == None:
      w = DISPLAY.width
    if h == None:
      h = DISPLAY.height
    self.unif[42:44] = [x, y]
    self.unif[45:48] = [w, h, DISPLAY.height]
    
  def set_2d_location(self, x, y):
    self.unif[42:44] = [x, y]

  def x(self):
    """get value of x"""
    return self.unif[0]

  def y(self):
    """get value of y"""
    return self.unif[1]

  def z(self):
    """get value of z"""
    return self.unif[2]

  def scale(self, sx, sy, sz):
    self.scl[0, 0] = sx
    self.scl[1, 1] = sy
    self.scl[2, 2] = sz
    self.unif[6:9] = sx, sy, sz
    self.MFlg = True

  def position(self, x, y, z):
    self.tr1[3, 0] = x - self.unif[9]
    self.tr1[3, 1] = y - self.unif[10]
    self.tr1[3, 2] = z - self.unif[11]
    self.unif[0:3] = x, y, z
    self.MFlg = True

  def positionX(self, v):
    self.tr1[3, 0] = v - self.unif[9]
    self.unif[0] = v
    self.MFlg = True

  def positionY(self, v):
    self.tr1[3, 1] = v - self.unif[10]
    self.unif[1] = v
    self.MFlg = True

  def positionZ(self, v):
    self.tr1[3, 2] = v - self.unif[11]
    self.unif[2] = v
    self.MFlg = True

  def translate(self, dx, dy, dz):
    self.tr1[3, 0] += dx
    self.tr1[3, 1] += dy
    self.tr1[3, 2] += dz
    self.MFlg = True
    self.unif[0] += dx
    self.unif[1] += dy
    self.unif[2] += dz

  def translateX(self, v):
    self.tr1[3, 0] += v
    self.unif[0] += v
    self.MFlg = True

  def translateY(self, v):
    self.tr1[3, 1] += v
    self.unif[1] += v
    self.MFlg = True

  def translateZ(self, v):
    self.tr1[3, 2] += v
    self.unif[2] += v
    self.MFlg = True

  def rotateToX(self, v):
    s, c = sin(radians(v)), cos(radians(v))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    self.unif[3] = v
    self.MFlg = True

  def rotateToY(self, v):
    s, c = sin(radians(v)), cos(radians(v))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    self.unif[4] = v
    self.MFlg = True

  def rotateToZ(self, v):
    s, c = sin(radians(v)), cos(radians(v))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    self.unif[5] = v
    self.MFlg = True

  def rotateIncX(self,v):
    self.unif[3] += v
    s, c = sin(radians(self.unif[3])), cos(radians(self.unif[3]))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    self.MFlg = True

  def rotateIncY(self,v):
    self.unif[4] += v
    s, c = sin(radians(self.unif[4])), cos(radians(self.unif[4]))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    self.MFlg = True

  def rotateIncZ(self,v):
    self.unif[5] += v
    s, c = sin(radians(self.unif[5])), cos(radians(self.unif[5]))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    self.MFlg = True

  def add_vertex(self, vert, norm, texc):
    """add vertex,normal and tex_coords ..."""
    self.verts.append(vert)
    self.norms.append(norm)
    self.texcoords.append(texc)


  def add_tri(self, indx):
    """add triangle refs."""
    self.inds.append(indx)

  def lathe(self, path, rise=0.0, loops=1.0):
    """returns a Buffer object by rotating the points defined in path

    Arguments:
    path -- an array of points [(x0,y0),(x1,y1)..] to rotate around
        the y axis
    NB TODO self.sides is not passed as an argument but is required to be
    set by anything calling this method
    [self.sides -- number of sides to divide each rotation into]

    Keyword arguments:
    rise -- amout to increment the path y values for each rotation (ie helix)
    loops -- numbe of times to rotate the path by 360 (ie helix)
    """
    s = len(path)
    rl = int(self.sides * loops)
    ssize = rl * 6 * (s - 1)

    pn = 0
    pp = 0
    tcx = 1.0 / self.sides
    pr = (pi / self.sides) * 2.0
    rdiv = rise / rl
    ss = 0

    # Find largest and smallest y of the path used for stretching the texture
    miny = path[0][1]
    maxy = path[s-1][1]
    for p in range(s):
      if path[p][1] < miny:
        miny = path[p][1]
      if path[p][1] > maxy:
        maxy = path[p][1]

    verts = []
    norms = []
    idx = []
    tex_coords = []

    opx = path[0][0]
    opy = path[0][1]

    for p in range(s):

      px = path[p][0] * 1.0
      py = path[p][1] * 1.0

      tcy = 1.0 - ((py - miny) / (maxy - miny))

      # Normalized 2D vector between path points
      dx, dy = Utility.vec_normal(Utility.vec_sub((px, py), (opx, opy)))

      for r in range (0, rl):
        sinr = sin(pr * r)
        cosr = cos(pr * r)
        verts.append((px * sinr, py, px * cosr))
        norms.append((-sinr * dy, dx, -cosr * dy))
        tex_coords.append((1.0 - tcx * r, tcy))
        py += rdiv

      # Last path profile (tidies texture coords).
      verts.append((0, py, px))
      norms.append((0, dx, -dy))
      tex_coords.append((0, tcy))

      if p < s - 1:
        pn += (rl + 1)
        for r in range(rl):
          idx.append((pp + r + 1, pp + r, pn + r))
          idx.append((pn + r, pn + r + 1, pp + r + 1))
        pp += (rl + 1)

      opx = px
      opy = py

    return Buffer(self, verts, tex_coords, idx, norms)
