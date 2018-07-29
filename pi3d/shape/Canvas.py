from pi3d.Buffer import Buffer
from pi3d.Shape import Shape

class Canvas(Shape):
  """ 3d model inherits from Shape. The simplest possible shape: a single
  triangle designed to fill the screen completely
  """
  def __init__(self, camera=None, light=None, name="", z=0.1):
    """Uses standard constructor for Shape but only one position variable is
    available as Keyword argument:

      *z*
        The depth that the shape will be constructed as an actual z offset
        distance in the vertices. As the Canvas is intended for use with
        2d shaders there is no way to change its location as no matrix
        multiplication will happen in the vertex shader.
    """
    super(Canvas, self).__init__(camera, light, name, x=0.0, y=0.0, z=0.0,
                                rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
                                cx=0.0, cy=0.0, cz=0.0)

    ww = 20.0
    hh = 20.0

    verts = ((-ww, -hh, z), (0.0, hh, z), (ww, -hh, z))
    norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1))
    texcoords = ((0.0, 0.0), (0.5, 1.0), (1.0, 0.0))

    inds = ((0, 1, 2), ) #python quirk: comma for tuple with only one val

    self.buf = [Buffer(self, verts, texcoords, inds, norms)]

  def set_texture(self, tex):
    self.buf[0].textures = [tex]

  def repaint(self, t):
    self.draw()

  def _load_opengl(self):
    self.buf[0].textures[0].load_opengl()

  def _unload_opengl(self):
    self.buf[0].textures[0].unload_opengl()
