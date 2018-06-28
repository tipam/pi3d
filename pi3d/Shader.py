from __future__ import absolute_import, division, print_function, unicode_literals

import ctypes
import sys, os
import logging
from pkg_resources import resource_string

from pi3d.constants import opengles, GL_FRAGMENT_SHADER, GL_VERTEX_SHADER
from pi3d.util.Ctypes import c_chars
from pi3d.util import Loadable
from pi3d.util.DefaultInstance import DefaultInstance

# This class based on Peter de Rivaz's mandlebrot example + Tim Skillman's work on pi3d2
LOGGER = logging.getLogger(__name__)

MAX_LOG_SIZE = 1024

def _opengl_log(shader, function, caption):
  log = c_chars(MAX_LOG_SIZE)
  loglen = ctypes.c_int()
  function(shader, MAX_LOG_SIZE, ctypes.byref(loglen), log)
  LOGGER.info('%s: %s', caption, log.value)

class Shader(DefaultInstance):
  """This compiles and holds the shaders to be used to render the Shape Buffers
  using their draw() methods. Generally you will choose and load the Shader
  explicitly as part of the program, however some i.e. defocus are loaded
  automatically when you create an instance of the Defocus class. Shaders can
  be 're-used' to draw different objects and the same object can be drawn using
  different Shaders.

  The shaders included with the pi3d module fall into two categories:

  * Textured - generally defined using the **uv** prefix, where an image needs
    to be loaded via the Texture class which is then mapped to the surface
    of the object. The **2d_flat** shader is a special case of a textured shader
    which maps pixels in an image to pixels on the screen with an optional
    scaling and offset.

  * Material - generally defined using the **mat** prefix, where a material
    shade (rgb) has to be set for the object to be rendered

  Within these categories the shaders have been subdivided with a postfix to
  give full names like uv_flat, mat_bump etc:

  * flat - no lighting is used, the shade rendered is the rgb value of the
    texture or material

  * light - Light direction, shade and ambient shade are used give a 3D effect
    to the surface

  * bump - a normal map texture needs to be loaded as well and this will be
    used to give much finer 3D effect to the surface than can be defined by
    the resolution of the vertices. The effect of the normal map drops with
    distance to give a detailed foreground without tiling artifacts in the
    distance. The shader is passed a variable to use for tiling the normal
    map which may be different from the tiling of the general texture. If
    set to 0.0 then no normal mapping will occur.

  * reflect - in addition to a normal map an image needs to be supplied to
    act as a reflection. The shader is passed a value from 0.0 to 1.0 to
    determine the strength of the reflection.

  The reason for using a host of different shaders rather than one that can
  do everything is that 'if' statements within the shader language are **very**
  time consuming.
  """
  def __init__(self, shfile=None, vshader_source=None, fshader_source=None):
    """
    Arguments:
      *shfile*
        Pathname without vs or fs ending i.e. "shaders/uv_light"

      *vshader_source*
        String with the code for the vertex shader.

      *fshader_source*
        String with the code for the fragment shader.
    """
    try:
      assert Loadable.is_display_thread()
    except AssertionError as err:
      LOGGER.error('load_opengl must be called on main thread for %s', self)
      raise err

    # TODO: the rest of the constructor should be split into load_disk
    # and load_opengl so that we can delete that assert.

    self.program = opengles.glCreateProgram()
    self.shfile = shfile

    def make_shader(src, suffix, shader_type):
      src = src or self._load_shader(shfile + suffix)
      if type(src) != bytes: #if ..shader_source passed as a string to __init__
        src = src.encode()
      characters = ctypes.c_char_p(src)
      shader = opengles.glCreateShader(shader_type)
      src_len = ctypes.c_int(len(src))
      opengles.glShaderSource(shader, 1, characters, ctypes.byref(src_len))
      opengles.glCompileShader(shader)
      self.showshaderlog(shader, src)
      opengles.glAttachShader(self.program, shader)
      return shader, src

    self.vshader, self.vshader_source = make_shader(
      vshader_source, '.vs', GL_VERTEX_SHADER)

    self.fshader, self.fshader_source = make_shader(
      fshader_source, '.fs', GL_FRAGMENT_SHADER)

    opengles.glLinkProgram(self.program)
    self.showprogramlog(self.program)

    self.attr_vertex = opengles.glGetAttribLocation(self.program, b'vertex')
    self.attr_normal = opengles.glGetAttribLocation(self.program, b'normal')

    self.unif_modelviewmatrix = opengles.glGetUniformLocation(
      self.program, b'modelviewmatrix')

    self.unif_unif = opengles.glGetUniformLocation(self.program, b'unif')
    self.unif_unib = opengles.glGetUniformLocation(self.program, b'unib')

    self.attr_texcoord = opengles.glGetAttribLocation(self.program, b'texcoord')
    opengles.glEnableVertexAttribArray(self.attr_texcoord)
    self.unif_tex = []
    self.textures = []
    for i in range(8):
      s = 'tex{}'.format(i).encode() 
      self.unif_tex.append(opengles.glGetUniformLocation(self.program, s))
      self.textures.append(None)
      """
      *NB*
        for *uv* shaders tex0=texture tex1=normal map tex2=reflection

        for *mat* shaders tex0=normal map tex1=reflection
      """
    self.use()

  @staticmethod
  def _default_instance():
    return Shader('mat_light')

  def use(self):
    """Makes this shader active"""
    opengles.glUseProgram(self.program)

  def showshaderlog(self, shader, src):
    """Prints the compile log for a shader"""
    N = 1024
    log = (ctypes.c_char * N)()
    loglen = ctypes.c_int()
    opengles.glGetShaderInfoLog(
      shader, N, ctypes.byref(loglen), log)
    if len(log.value) > 0:
      LOGGER.info('shader(%s) %s, %s', shader, self.shfile, log.value)

  def showprogramlog(self, shader):
    """Prints the compile log for a program"""
    N = 1024
    log = (ctypes.c_char * N)()
    loglen = ctypes.c_int()
    opengles.glGetProgramInfoLog(
      shader, N, ctypes.byref(loglen), log)

  def _load_shader(self, sfile):
    ''' takes a file name as string, tries to find it then returns the
    contents as a bytes object swapping out the #include statements recursively. 
    This means that if you make your own shader with #includes, the names 
    of the include files must be different from the standard pi3d ones unless 
    you intend to use the standard ones.
    '''
    if type(sfile) == bytes: #annoyingly resource_string has string argument.
      sfile = sfile.decode()
    new_text = b'' #but then returns a bytes object so swap to bytes!
    try:
      st = resource_string('pi3d', 'shaders/' + sfile)
    except:
      LOGGER.info('no file shaders/' + sfile + ' in pkg_resources trying')
      st = open(sfile, 'rb').read() #assume it's a non-standard shader in a file
    for l in st.split(b'\n'):
      if b'#include' in l:
        inc_file = l.split()[1]
        new_text = new_text + self._load_shader(inc_file) + b'\n'
      else:
        new_text = new_text + l + b'\n'
    return new_text
