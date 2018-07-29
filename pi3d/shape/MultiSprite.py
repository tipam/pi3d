from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class MultiSprite(Shape):
  """ 3d model inherits from Shape, this is a series of Sprites
  edge to edge to allow larger images than the maximum size of 1920
  imposed by the Texture class
  """
  def __init__(self, textures, shader, camera=None, light=None, w=1.0, h=1.0, name="",
               x=0.0, y=0.0, z=20.0,
               rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """Uses standard constructor for Shape. Arguments:
      *textures*
        must be a two dimensional list of lists of textures or strings 
        (which must be the path/names of image files) The array runs left
        to right then down so six textures in spreadsheet notation would be
        
        [[R1C1, R1C2], [R2C1, R2C2], [R3C1, R3C2]]
        
      *shader*
        shader to use
        
      Extra keyword arguments:  
        
      *w*
        Width.
      *h*
        Height.
    """
    try:
      nh = len(textures)
      nw = len(textures[0])
      super(MultiSprite, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                   sx, sy, sz, cx, cy, cz)
      self.width = w
      self.height = h
      ww = w / 2.0 / nw
      hh = h / 2.0 / nh
      self.buf = []
      for i in range(nw):
        for j in range(nh):
          offw = w * ((1.0 - nw) / 2.0 + i) / nw
          offh = -h * ((1.0 - nh) / 2.0 + j) / nh
          verts = ((-ww + offw, hh + offh, 0.0), 
                        (ww + offw, hh + offh, 0.0), 
                        (ww + offw, -hh + offh, 0.0), 
                        (-ww + offw, -hh + offh, 0.0))
          norms = ((0, 0, -1), (0, 0, -1),  (0, 0, -1), (0, 0, -1))
          texcoords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0 , 1.0))

          inds = ((0, 1, 3), (1, 2, 3))

          thisbuf = Buffer(self, verts, texcoords, inds, norms)
          if not isinstance(textures[j][i], Texture): # i.e. can load from file name
            textures[j][i] = Texture(textures[j][i])
          thisbuf.textures = [textures[j][i]]
          self.buf.append(thisbuf)
      self.set_shader(shader)
      self.set_2d_size() # method in Shape, default full window size
    except IndexError:
      LOGGER.error('Must supply a list of lists of Textures or strings')
