import ctypes

from pi3d import *
from pi3d.util import Log

# This class based on Peter de Rivaz's mandlebrot example + Tim Skillman's work on pi3d2
LOGGER = Log.logger(__name__)

MAX_LOG_SIZE = 1024

def _opengl_log(shader, function, caption):
  log = c_chars(MAX_LOG_SIZE)
  loglen = ctypes.c_int()
  function(shader, MAX_LOG_SIZE, ctypes.byref(loglen), ctypes.byref(log))
  LOGGER.info('%s: %s', caption, log.value)

class Shader(object):
  def __init__(self, shfile):
    """
    shfile -- path/name without vs or fs ending i.e. "shaders/bumpShade"
    textures[] -- array of Texture() objects 0.texture map 1.normal map 2.reflection map
    scene -- Scene() object
    bumpTiles -- number to subdivide UV map by for normal texture map, 0.0 disables
    shiny -- proportion of shininess 0.0 to 1.0, 0.0 disables
    """

    #self.scene = scene
    self.shfile = shfile
    self.vshader_source = ctypes.c_char_p(self.loadShader(shfile + ".vs"))
    self.fshader_source = ctypes.c_char_p(self.loadShader(shfile + ".fs"))

    self.vshader = opengles.glCreateShader(GL_VERTEX_SHADER);
    opengles.glShaderSource(self.vshader, 1, ctypes.byref(self.vshader_source), 0)
    opengles.glCompileShader(self.vshader)
    self.showshaderlog(self.vshader)

    self.fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER);
    opengles.glShaderSource(self.fshader, 1, ctypes.byref(self.fshader_source), 0)
    opengles.glCompileShader(self.fshader)
    self.showshaderlog(self.fshader)

    self.program = opengles.glCreateProgram()
    opengles.glAttachShader(self.program, self.vshader)
    opengles.glAttachShader(self.program, self.fshader)
    opengles.glLinkProgram(self.program)
    self.showprogramlog(self.program)

    self.attr_vertex = opengles.glGetAttribLocation(self.program, "vertex")
    self.attr_normal = opengles.glGetAttribLocation(self.program, "normal")
    #self.unif_lightpos = opengles.glGetUniformLocation(self.program, "lightpos")
    self.unif_modelviewmatrix = opengles.glGetUniformLocation(self.program, "modelviewmatrix")
    self.unif_cameraviewmatrix = opengles.glGetUniformLocation(self.program, "cameraviewmatrix")
    #self.unif_ntiles = opengles.glGetUniformLocation(self.program, "ntiles")
    #self.unif_shiny = opengles.glGetUniformLocation(self.program, "shiny")
    #self.unif_fogshade = opengles.glGetUniformLocation(self.program, "fogshade")
    #self.unif_fogdist = opengles.glGetUniformLocation(self.program, "fogdist")
    #self.unif_eye = opengles.glGetUniformLocation(self.program, "eye")
    #self.unif_rtn = opengles.glGetUniformLocation(self.program, "rtn")
    #self.unif_blend = opengles.glGetUniformLocation(self.program, "blend")
    #self.unif_material = opengles.glGetUniformLocation(self.program, "material")
    # attemp to offload matrix work to shader
    #self.unif_locn = opengles.glGetUniformLocation(self.program, "locn")
    #self.unif_rotn = opengles.glGetUniformLocation(self.program, "rotn")
    #self.unif_scle = opengles.glGetUniformLocation(self.program, "scle")
    #self.unif_ofst = opengles.glGetUniformLocation(self.program, "ofst")
    self.unif_unif = opengles.glGetUniformLocation(self.program, "unif")
    self.unif_unib = opengles.glGetUniformLocation(self.program, "unib")

    self.attr_texcoord = opengles.glGetAttribLocation(self.program, "texcoord")
    opengles.glEnableVertexAttribArray(self.attr_texcoord)
    self.unif_tex = []
    self.texture = []
    for t in range(3):
      self.unif_tex.append(opengles.glGetUniformLocation(self.program, "tex"+str(t))) #tex0 texture tex1 bump tex2 reflection
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))
      opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, c_float(GL_LINEAR_MIPMAP_NEAREST))

    self.use()

  def use(self):
    """Makes this shader active"""
    opengles.glUseProgram(self.program)

  def showshaderlog(self,shader):
    """Prints the compile log for a shader"""
    N=1024
    log=(c_char*N)()
    loglen=c_int()
    opengles.glGetShaderInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
    print log.value

  def showprogramlog(self,shader):
    """Prints the compile log for a program"""
    N=1024
    log=(c_char*N)()
    loglen=c_int()
    opengles.glGetProgramInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
    print log.value

  def loadShader(self, sfile):
    return open(sfile,'r').read()
