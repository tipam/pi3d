from pi3d import *

# This class based on Peter de Rivaz's mandlebrot example

class Shader(object):
  def showlog(self,shader):
    """Prints the compile log for a shader"""
    N = 1024
    log = (ctypes.c_char * N)()
    loglen=ctypes.c_int()
    opengles.glGetShaderInfoLog(shader, N,
                                ctypes.byref(loglen), ctypes.byref(log))
    print "Shader log:",log.value

  def showprogramlog(self,shader):
    """Prints the compile log for a shader"""
    N = 1024
    log = (ctypes.c_char * N)()
    loglen = ctypes.c_int()
    opengles.glGetProgramInfoLog(shader, N,
                                 ctypes.byref(loglen), ctypes.byref(log))
    print log.value


  def __init__(self, vshader_source, fshader_source,
               tex1=None, tex2=None, param1=None, param2=None, param3=None):
    #Pi3D can only accept shaders with limited parameters as specific parameters
    #would require a lot more coding unless there's a way of passing these back.
    #Shaders should have their parameters defined in the shader source.
    #The only parameters Pi3D can pass (for now) is textures.

    self.vshader_source = ctypes.c_char_p(
      "attribute vec4 vertex;"
      "varying vec2 tcoord;"
      "void main(void) {"
      "  vec4 pos = vertex;"
      "  pos.xy*=0.9;"
      "  gl_Position = pos;"
      "  tcoord = vertex.xy*0.5+0.5;"
      "}")

    self.tex1 = tex1
    self.tex2 = tex2

    vshads = ctypes.c_char_p(vshader_source)
    fshads = ctypes.c_char_p(fshader_source)

    vshader = opengles.glCreateShader(GL_VERTEX_SHADER)
    opengles.glShaderSource(vshader, 1, ctypes.byref(self.vshader_source), 0)
    opengles.glCompileShader(vshader)
    if VERBOSE:
      self.showlog(vshader)

    fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER)
    opengles.glShaderSource(fshader, 1, ctypes.byref(fshads), 0)
    opengles.glCompileShader(fshader)
    if VERBOSE:
      self.showlog(fshader)

    self.program = opengles.glCreateProgram()
    opengles.glAttachShader(self.program, vshader)
    opengles.glAttachShader(self.program, fshader)
    opengles.glLinkProgram(self.program)
    if VERBOSE:
      self.showprogramlog(self.program)

  def use(self):
    if self.tex1 is not None:
      unif_tex1 = opengles.glGetUniformLocation(self.program, "tex1")
      # frag shader must have a uniform 'tex1'

    if self.tex2 is not None:
      unif_tex2 = opengles.glGetUniformLocation(self.program, "tex2")
      # frag shader must have a uniform 'tex2'
    opengles.glUseProgram( self.program );

  #self.program = program
  #self.unif_color = opengles.glGetUniformLocation(program, "color");
  #self.attr_vertex = opengles.glGetAttribLocation(program, "vertex");
  #self.unif_scale = opengles.glGetUniformLocation(program, "scale");
  #self.unif_offset = opengles.glGetUniformLocation(program, "offset");
  #self.unif_tex = opengles.glGetUniformLocation(program, "tex");
