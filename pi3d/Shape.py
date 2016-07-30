from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes

from numpy import array, dot, savez, load, zeros
from math import radians, pi, sin, cos

from pi3d.constants import *
from pi3d.Buffer import Buffer
from pi3d.Light import Light
from pi3d.Camera import Camera
from pi3d.util import Utility
from pi3d.util.Ctypes import c_floats

from pi3d.util.Loadable import Loadable

class Shape(Loadable):
  """inherited by all shape objects, including simple 2D sprite types"""
  def __init__(self, camera, light, name, x, y, z,
               rx, ry, rz, sx, sy, sz, cx, cy, cz):
    """
    Arguments:
      *light*
        Light instance: if None then Light.instance() will be used.
      *name*
        Name string for identification.
      *x, y, z*
        Location of the origin of the shape, stored in a uniform array.
      *rx, ry, rz*
        Rotation of shape in degrees about each axis.
      *sx, sy, sz*
        Scale in each direction.
      *cx, cy, cz*
        Offset vertices from origin in each direction.
    """
    super(Shape, self).__init__()
    self.name = name
    light = light if light is not None else Light.instance()
    # uniform variables all in one array (for Shape and one for Buffer)
    self.unif =  (ctypes.c_float * 60)(
      x, y, z, rx, ry, rz,
      sx, sy, sz, cx, cy, cz,
      0.5, 0.5, 0.5, 5000.0, 0.8, 1.0,
      0.0, 0.0, 0.0, light.is_point, 0.0, 0.0,
      light.lightpos[0], light.lightpos[1], light.lightpos[2],
      light.lightcol[0], light.lightcol[1], light.lightcol[2],
      light.lightamb[0], light.lightamb[1], light.lightamb[2],
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    """ pass to shader array of vec3 uniform variables:

    ===== ========================================== ==== ==
    vec3  description                                python
    ----- ------------------------------------------ -------
    index                                            from to
    ===== ========================================== ==== ==
       0  location                                     0   2
       1  rotation                                     3   5
       2  scale                                        6   8
       3  offset                                       9  11
       4  fog shade                                   12  14
       5  fog distance, fog alpha, shape alpha        15  17
       6  camera position                             18  20
       7  point light if 1: light0, light1, unused    21  23
       8  light0 position, direction vector           24  26
       9  light0 strength per shade                   27  29
      10  light0 ambient values                       30  32
      11  light1 position, direction vector           33  35
      12  light1 strength per shade                   36  38
      13  light1 ambient values                       39  41
      14  defocus dist_from, dist_to, amount          42  43 # also 2D x, y
      15  defocus frame width, height (only 2 used)   45  46 # also 2D w, h, tot_ht
      16  custom data space                           48  50
      17  custom data space                           51  53
      18  custom data space                           54  56
      19  custom data space                           57  59
    ===== ========================================== ==== ==
    """
    self.shader = None
    self.textures = []

    self.buf = []
    """self.buf contains a buffer for each part of this shape that needs
    rendering with a different Shader/Texture. self.draw() relies on objects
    inheriting from this filling buf with at least one element.
    """
    
    self.children = []
    self._camera = camera
    
    self.__init_matrices()

  def __init_matrices(self):
    """
    Shape holds matrices that are updated each time it is moved or rotated
    this saves time recalculating them each frame as the Shape is drawn
    """
    self.tr1 = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [self.unif[0] - self.unif[9], self.unif[1] - self.unif[10], self.unif[2] - self.unif[11], 1.0]])
    """translate to position - offset"""

    s, c = sin(radians(self.unif[3])), cos(radians(self.unif[3]))
    self.rox = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, c, s, 0.0],
                      [0.0, -s, c, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    self.roxflg = True if self.unif[3] != 0.0 else False
    """rotate about x axis"""

    s, c = sin(radians(self.unif[4])), cos(radians(self.unif[4]))
    self.roy = array([[c, 0.0, -s, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [s, 0.0, c, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    self.royflg = True if self.unif[4] != 0.0 else False
    """rotate about y axis"""

    s, c = sin(radians(self.unif[5])), cos(radians(self.unif[5]))
    self.roz = array([[c, s, 0.0, 0.0],
                      [-s, c, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    self.rozflg = True if self.unif[5] != 0.0 else False
    """rotate about z axis"""

    self.scl = array([[self.unif[6], 0.0, 0.0, 0.0],
                      [0.0, self.unif[7], 0.0, 0.0],
                      [0.0, 0.0, self.unif[8], 0.0],
                      [0.0, 0.0, 0.0, 1.0]])
    if self.unif[6] != 1.0 or self.unif[7] != 1.0 or self.unif[8] != 1.0:
      self.sclflg = True 
    else:
      self.sclflg = False
    """scale"""

    self.tr2 = array([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [self.unif[9], self.unif[10], self.unif[11], 1.0]])
    if self.unif[9] != 0.0 or self.unif[10] != 0.0 or self.unif[11] != 0.0:
      self.tr2flg = True 
    else:
      self.tr2flg = False
    """translate to offset"""

    self.MFlg = True
    #self.M = zeros(32, dtype="float32").reshape(2,4,4)
    self.M = zeros(48, dtype="float32").reshape(3,4,4) # 3rd matrix added for casting shadows v2.7


  def draw(self, shader=None, txtrs=None, ntl=None, shny=None, camera=None, mlist=[], light_camera=None):
    """If called without parameters, there has to have been a previous call to
    set_draw_details() for each Buffer in buf[].
    NB there is no facility for setting umult and vmult with draw: they must be
    set using set_draw_details or Buffer.set_draw_details.
    """
    self.load_opengl() # really just to set the flag so _unload_opengl runs

    camera = camera or self._camera or Camera.instance()
    
    if not camera.mtrx_made:
      camera.make_mtrx()
    if light_camera and not light_camera.mtrx_made:
      light_camera.make_mtrx()

    if self.MFlg or len(mlist) > 0 or len(self.children) > 0:
      # Calculate rotation and translation matrix for this model using numpy.
      self.MRaw = self.tr1
      if self.rozflg:
        self.MRaw = dot(self.roz, self.MRaw)
      if self.roxflg:
        self.MRaw = dot(self.rox, self.MRaw)
      if self.royflg:
        self.MRaw = dot(self.roy, self.MRaw)
      if self.sclflg:
        self.MRaw = dot(self.scl, self.MRaw)
      if self.tr2flg:
        self.MRaw = dot(self.tr2, self.MRaw)

      # child drawing addition #############
      newmlist = [m for m in mlist]
      newmlist.append(self.MRaw)
      if len(self.children) > 0:
        for c in self.children:
          c.draw(shader, txtrs, ntl, shny, camera, newmlist, light_camera) # TODO issues where child doesn't use same shader 
      for m in mlist[-1::-1]:
        self.MRaw = dot(self.MRaw, m)
      ######################################
      self.M[0,:,:] = self.MRaw[:,:]
      #self.M[0:16] = c_floats(self.MRaw.reshape(-1).tolist()) #pypy version
      self.M[1,:,:] = dot(self.MRaw, camera.mtrx)[:,:]
      #self.M[16:32] = c_floats(dot(self.MRaw, camera.mtrx).reshape(-1).tolist()) #pypy
      if light_camera is not None:
        self.M[2,:,:] = dot(self.MRaw, light_camera.mtrx)[:,:]
      self.MFlg = False

    elif camera.was_moved:
      # Only do this if it's not done because model moved.
      self.M[1,:,:] = dot(self.MRaw, camera.mtrx)[:,:]
      if light_camera is not None:
        self.M[2,:,:] = dot(self.MRaw, light_camera.mtrx)[:,:]

    if camera.was_moved:
      self.unif[18:21] = camera.eye[0:3]

    for b in self.buf:
      # Shape.draw has to be passed either parameter == None or values to pass
      # on.
      b.draw(self, self.M, self.unif, shader, txtrs, ntl, shny)

  def set_shader(self, shader):
    """Wrapper method to set just the Shader for all the Buffer objects of
    this Shape. Used, for instance, in a Model where the Textures have been
    defined in the obj & mtl files, so you can't use set_draw_details.

    Arguments:

      *shader*
        Shader to use

    """

    self.shader = shader
    for b in self.buf:
      b.shader = shader

  def set_normal_shine(self, normtex, ntiles=1.0, shinetex=None,
                       shiny=0.0, is_uv=True, bump_factor=1.0):
    """Used to set some of the draw details for all Buffers in Shape.
    This is useful where a Model object has been loaded from an obj file and
    the textures assigned automatically.

    Arguments:
      *normtex*
        Normal map Texture to use.

    Keyword arguments:
      *ntiles*
        Multiplier for the tiling of the normal map.
      *shinetex*
        Reflection Texture to use.
      *shiny*
        Strength of reflection (ranging from 0.0 to 1.0).
      *is_uv*
        If True then the normtex will be textures[1] and shinetex will be
        textures[2] i.e. if using a 'uv' type Shader. However, for 'mat' type
        Shaders they are moved down one, as the basic shade is defined by
        material rgb rather than from a Texture.
      *bump_factor*
        multiplier for the normal map surface distortion effect
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
      b.unib[11] = bump_factor
      if shinetex is not None:
        while len(b.textures) < (3 + ofst):
          b.textures.append(None)
        b.textures[2 + ofst] = shinetex
        b.unib[1] = shiny

  def set_draw_details(self, shader, textures, ntiles = 0.0, shiny = 0.0,
                      umult=1.0, vmult=1.0, bump_factor=1.0):
    """Wrapper to call set_draw_details() for each Buffer object.

    Arguments:
      *shader*
        Shader object
      *textures*
        array of Texture objects
    """
    self.shader = shader
    for b in self.buf:
      b.set_draw_details(shader, textures, ntiles, shiny, umult, vmult, bump_factor)

  def set_material(self, material):
    """Wrapper for setting material shade in each Buffer object.

    Arguments:
      *material*
        tuple (rgb)
    """
    for b in self.buf:
      b.set_material(material)

  def set_textures(self, textures):
    """Wrapper for setting textures in each Buffer object.

    Arguments:
      *textures*
        list of Texture objects
    """
    for b in self.buf:
      b.set_textures(textures)

  def set_offset(self, offset):
    """Wrapper for setting uv texture offset in each Buffer object.

    Arguments:
      *offset*
        tuple (u_off, v_off) values between 0.0 and 1.0 to offset the texture
        sampler by
    """
    for b in self.buf:
      b.set_offset(offset)

  def offset(self):
    """Get offset as (u, v) tuple of (first) buf uv. Doesnt check that buf array
    exists and has at least one value and only returns offset for that value"""
    return self.buf[0].unib[9:11]


  def set_fog(self, fogshade, fogdist):
    """Set fog for this Shape only, it uses the shader smoothblend function from
    1/3 fogdist to fogdist.

    Arguments:
      *fogshade*
        tuple (rgba)
      *fogdist*
        distance from Camera at which Shape is 100% fogshade
    """
    self.unif[12:15] = fogshade[0:3]
    self.unif[15] = fogdist
    self.unif[16] = fogshade[3]

  def set_alpha(self, alpha=1.0):
    """Set alpha for this Shape only

    Arguments:
      *alpha*
        alpha value between 0.0 and 1.0 (default)
    """
    self.unif[17] = alpha

  def alpha(self):
    """Get value of alpha"""
    return self.unif[17]

  def set_light(self, light, num=0):
    """Set the values of the lights.

    Arguments:
      *light*
        Light object to use
      *num*
        number of the light to set
    """
    #TODO (pg) need MAXLIGHTS global variable, room for two now but shader
    # only uses 1.
    if num > 1 or num < 0:
      num = 0
    stn = 24 + num * 9
    self.unif[stn:(stn + 3)] = light.lightpos[0:3]
    self.unif[(stn + 3):(stn + 6)] = light.lightcol[0:3]
    self.unif[(stn + 6):(stn + 9)] = light.lightamb[0:3]
    self.unif[21 + num] = light.is_point

  def set_2d_size(self, w=None, h=None, x=0, y=0):
    """saves size to be drawn and location in pixels for use by 2d shader

    Keyword arguments:

      *w*
        Width, pixels.
      *h*
        Height, pixels.
      *x*
        Left edge of image from left edge of display, pixels.
      *y*
        Top of image from top of display, pixels

    """
    from pi3d.Display import Display
    if w is None:
      w = Display.INSTANCE.width
    if h is None:
      h = Display.INSTANCE.height
    self.unif[42:44] = [x, y]
    self.unif[45:48] = [w, h, Display.INSTANCE.height]

  def set_2d_location(self, x, y):
    """saves location in pixels for use by 2d shader

    Arguments:

      *x*
        Left edge of image from left edge of display, pixels.
      *y*
        Top of image from top of display, pixels

    """
    self.unif[42:44] = [x, y]

  def set_custom_data(self, index_from, data):
    """save general purpose custom data for use by any shader **NB it is up
    to the user to provide data in the form of a suitable array of values
    that will fit into the space available in the unif array**

    Arguments:

      *index_from*
        start index in unif array for filling data should be 48 to 59
        42 to 47 could be used if they do not conflict with existing shaders
        i.e. 2d_flat, defocus etc
      *data*
        2D array of values to put in [[a,b,c],[d,e,f]]
    """
    self.unif[index_from:(index_from + len(data))] = data

  def set_point_size(self, point_size=1.0):
    """This will set the draw_method in all Buffers of this Shape"""
    for b in self.buf:
      b.unib[8] = point_size
      b.draw_method = GL_POINTS if point_size > 0.0 else GL_TRIANGLES

  def set_line_width(self, line_width=1.0, strip=True, closed=False):
    """This will set the draw_method in all Buffers of this Shape

      *line-width*
        line width default 1

      *closed*
        if set to True then the last leg will be filled in. ie polygon
    
    NB it differs from point size in that glLineWidth() is called here
    and that line width will be used for all subsequent draw() operations
    so if you want to draw shapes with different thickness lines you will
    have to call this method repeatedly just before each draw()
    
    Also, there doens't seem to be an equivalent of gl_PointSize as used
    in the shader language to make lines shrink with distance.

    If you are drawing lines with high contrast they will look better
    anti aliased which is done by Display.create(samples=4) """
    for b in self.buf:
      b.unib[11] = line_width
      opengles.glLineWidth(ctypes.c_float(line_width))
      if strip:
        draw_method = GL_LINE_LOOP if closed else GL_LINE_STRIP
      else:
        draw_method = GL_LINES
      b.draw_method = draw_method if line_width > 0.0 else GL_TRIANGLES

  def re_init(self, pts=None, texcoords=None, normals=None, offset=0):
    """ wrapper for Buffer.re_init()
    """
    self.buf[0].re_init(pts, texcoords, normals, offset)
    
  def add_child(self, child):
    """puts a Shape into the children list"""
    self.children.append(child)

  def x(self):
    """get value of x"""
    return self.unif[0]

  def y(self):
    """get value of y"""
    return self.unif[1]

  def z(self):
    """get value of z"""
    return self.unif[2]

  def get_bounds(self):
    """Find the limits of vertices in three dimensions. Returns a tuple
    (left, bottom, front, right, top, back)
    """
    left, bottom, front  = 10000.0, 10000.0, 10000.0
    right, top, back = -10000.0, -10000.0, -10000.0
    for b in self.buf:
      v = b.array_buffer # alias to simplify code. vertices are array_buffer[:,0:3]
      left = min(left, v[:,0].min())
      bottom = min(bottom, v[:,1].min())
      front = min(front, v[:,2].min())
      right = max(right, v[:,0].max())
      top = max(top, v[:,1].max())
      back = max(back, v[:,2].max())

    return (left, bottom, front, right, top, back)

  def scale(self, sx, sy, sz):
    """Arguments:

      *sx*
        x scale
      *sy*
        y scale
      *sz*
        z scale
    """
    self.scl[0, 0] = sx
    self.scl[1, 1] = sy
    self.scl[2, 2] = sz
    self.unif[6] = sx
    self.unif[7] = sy
    self.unif[8] = sz
    self.MFlg = True
    self.sclflg = True

  def position(self, x, y, z):
    """Arguments:

      *x*
        x position
      *y*
        y position
      *z*
        z position
    """
    self.tr1[3, 0] = x - self.unif[9]
    self.tr1[3, 1] = y - self.unif[10]
    self.tr1[3, 2] = z - self.unif[11]
    self.unif[0] = x
    self.unif[1] = y
    self.unif[2] = z
    self.MFlg = True

  def positionX(self, v):
    """Arguments:

      *v*
        x position
    """
    self.tr1[3, 0] = v - self.unif[9]
    self.unif[0] = v
    self.MFlg = True

  def positionY(self, v):
    """Arguments:

      *v*
        y position
    """
    self.tr1[3, 1] = v - self.unif[10]
    self.unif[1] = v
    self.MFlg = True

  def positionZ(self, v):
    """Arguments:

      *v*
        z position
    """
    self.tr1[3, 2] = v - self.unif[11]
    self.unif[2] = v
    self.MFlg = True

  def translate(self, dx, dy, dz):
    """Arguments:

      *dx*
        x translation
      *dy*
        y translation
      *dz*
        z translation
    """
    self.tr1[3, 0] += dx
    self.tr1[3, 1] += dy
    self.tr1[3, 2] += dz
    self.MFlg = True
    self.unif[0] += dx
    self.unif[1] += dy
    self.unif[2] += dz

  def translateX(self, v):
    """Arguments:

      *v*
        x translation
    """
    self.tr1[3, 0] += v
    self.unif[0] += v
    self.MFlg = True

  def translateY(self, v):
    """Arguments:

      *v*
        y translation
    """
    self.tr1[3, 1] += v
    self.unif[1] += v
    self.MFlg = True

  def translateZ(self, v):
    """Arguments:

      *v*
        z translation
    """
    self.tr1[3, 2] += v
    self.unif[2] += v
    self.MFlg = True

  def rotateToX(self, v):
    """Arguments:

      *v*
        x rotation
    """
    s, c = sin(radians(v)), cos(radians(v))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    self.unif[3] = v
    self.MFlg = True
    self.roxflg = True

  def rotateToY(self, v):
    """Arguments:

      *v*
        y rotation
    """
    s, c = sin(radians(v)), cos(radians(v))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    self.unif[4] = v
    self.MFlg = True
    self.royflg = True

  def rotateToZ(self, v):
    """Arguments:

      *v*
        z rotation
    """
    s, c = sin(radians(v)), cos(radians(v))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    self.unif[5] = v
    self.MFlg = True
    self.rozflg = True

  def rotateIncX(self, v):
    """Arguments:

      *v*
        x rotational increment
    """
    self.unif[3] += v
    s, c = sin(radians(self.unif[3])), cos(radians(self.unif[3]))
    self.rox[1, 1] = self.rox[2, 2] = c
    self.rox[1, 2] = s
    self.rox[2, 1] = -s
    self.MFlg = True
    self.roxflg = True

  def rotateIncY(self, v):
    """Arguments:

      *v*
        y rotational increment
    """
    self.unif[4] += v
    s, c = sin(radians(self.unif[4])), cos(radians(self.unif[4]))
    self.roy[0, 0] = self.roy[2, 2] = c
    self.roy[0, 2] = -s
    self.roy[2, 0] = s
    self.MFlg = True
    self.royflg = True

  def rotateIncZ(self, v):
    """Arguments:

      *v*
        z rotational increment
    """
    self.unif[5] += v
    s, c = sin(radians(self.unif[5])), cos(radians(self.unif[5]))
    self.roz[0, 0] = self.roz[1, 1] = c
    self.roz[0, 1] = s
    self.roz[1, 0] = -s
    self.MFlg = True
    self.rozflg = True

  def _lathe(self, path, sides=12, rise=0.0, loops=1.0):
    """Returns a Buffer object by rotating the points defined in path.

    Arguments:
      *path*
        An array of points [(x0, y0), (x1, y1) ...] to rotate around
        the y axis.

    Keyword arguments:
      *sides*
        Number of sides to divide each rotation into.
      *rise*
        Amount to increment the path y values for each rotation (ie helix)
      *loops*
        Number of times to rotate the path by 360 (ie helix).

    """
    self.sides = sides

    s = len(path)
    rl = int(self.sides * loops)

    pn = 0
    pp = 0
    tcx = 1.0 / self.sides
    pr = (pi / self.sides) * 2.0
    rdiv = rise / rl

    # Find length of the path
    path_len = 0.0
    for p in range(1, s):
      path_len += ((path[p][0] - path[p-1][0])**2 +
                   (path[p][1] - path[p-1][1])**2)**0.5

    verts = []
    norms = []
    idx = []
    tex_coords = []

    opx = path[0][0]
    opy = path[0][1]

    tcy = 0.0
    for p in range(s):

      px = path[p][0] * 1.0
      py = path[p][1] * 1.0

      if p > 0:
        tcy += ((path[p][0] - path[p-1][0])**2 +
                (path[p][1] - path[p-1][1])**2)**0.5 / path_len

      # Normalized 2D vector between path points
      if p == 0:
        ipx, ipy = path[1][0] * 1.0, path[1][1] * 1.0
      else:
        ipx, ipy = px, py
      dx, dy = Utility.vec_normal(Utility.vec_sub((ipx, ipy), (opx, opy)))

      for r in range (0, rl + 1):
        sinr = sin(pr * r)
        cosr = cos(pr * r)
        verts.append((px * sinr, py, px * cosr))
        norms.append((-sinr * dy, dx, -cosr * dy))
        tex_coords.append((1.0 - tcx * r, tcy))
        py += rdiv

      if p < s - 1:
        pn += (rl + 1)
        for r in range(rl):
          idx.append((pp + r + 1, pp + r, pn + r))
          idx.append((pn + r, pn + r + 1, pp + r + 1))
        pp += (rl + 1)

      opx = px
      opy = py

    return Buffer(self, verts, tex_coords, idx, norms)
  
  def __getstate__(self):
    return {
      'unif': list(self.unif),
      #'childModel': self.childModel,
      'children': self.children,
      'name': self.name,
      'buf': self.buf,
      'textures': self.textures,
      'shader': self.shader

      }
  
  def __setstate__(self, state):
    unif_tuple = tuple(state['unif'])
    self.unif = (ctypes.c_float * 60)(*unif_tuple)
    #self.childModel = state['childModel']
    self.name = state['name']
    self.children = state['children']
    self.buf = state['buf']
    self.textures = state['textures']
    self.shader = state['shader']
    self.opengl_loaded = False
    self.disk_loaded = True
    self._camera = None
    self.__init_matrices()


