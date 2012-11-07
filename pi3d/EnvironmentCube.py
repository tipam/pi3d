import os.path

from pi3d import *
from pi3d import Utility

CUBE_PARTS = ('top', 'left', 'front', 'right', 'back', 'bottom')

def loadECfiles(path, fname, textures):
  # Helper for loading environment cube faces.
  files = (os.path.join(path, '%s_%s.jpg' % (fname, p)) for p in CUBE_PARTS)
  return [textures.loadTexture(f) for f in files]

class EnvironmentCube(object):
  def __init__(self, size=500.0, maptype="HALFCROSS", name=""):
    if VERBOSE:
      print "Creating Environment Cube ..."

    self.scale = size
    self.ssize = 36
    self.ttype = GL_TRIANGLES
    self.maptype = maptype
    ww = self.scale / 2.0 # TODO: this seems wrong...!
    hh = self.scale / 2.0
    dd = self.scale / 2.0

    #cuboid data - faces are separated out for texturing..

    self.vertices = c_floats((-ww,hh,dd, ww,hh,dd, ww,-hh,dd, -ww,-hh,dd,
                               ww,hh,dd, ww,hh,-dd, ww,-hh,-dd, ww,-hh,dd,
                               -ww,hh,dd, -ww,hh,-dd, ww,hh,-dd, ww,hh,dd,
                               ww,-hh,dd, ww,-hh,-dd, -ww,-hh,-dd, -ww,-hh,dd,
                               -ww,-hh,dd, -ww,-hh,-dd, -ww,hh,-dd, -ww,hh,dd,
                               -ww,hh,-dd, ww,hh,-dd, ww,-hh,-dd, -ww,-hh,-dd))

    self.normals = c_floats((0,0,1, 0,0,1, 0,0,1, 0,0,1,
            1,0,0, 1,0,0, 1,0,0, 1,0,0,
            0,1,0, 0,1,0, 0,1,0, 0,1,0,
            0,-1,0, 0,-1,0, 0,-1,0, 0,-1,0,
            -1,0,0, -1,0,0, -1,0,0, -1,0,0,
            0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1))

    self.indices = c_shorts((3,0,1, 2,3,1, 7,4,5, 6,7,5, 11,8,9, 10,11,9, 15,12,13, 14,15,13, 19,16,17, 18,19,17, 23,22,21, 20,23,21));

    self.indfront = c_shorts((23,22,21, 20,23,21 )) #back
    self.indleft = c_shorts((19,16,17, 18,19,17)) #right
    self.indtop = c_shorts((11,8,9, 10,11,9))  #top
    self.indbot = c_shorts((15,12,13, 14,15,13))  #bottom
    self.indright = c_shorts((7,4,5, 6,7,5)) #left
    self.indback = c_shorts((3,0,1, 2,3,1)) #front

    if self.maptype == "HALFCROSS":
        self.tex_coords = c_floats((0.25,0.25, 0.25,0.75, -0.25,0.75, -0.25,0.25,
            0.25,0.75, 0.75,0.75, 0.75,1.25, 0.25,1.25,
            0.25,0.25, 0.75,0.25, 0.75,0.75, 0.25,0.75,  #top
            0,0, 1,0, 1,1, 0,1,    #bottom
            0.25,-0.25, 0.75,-0.25, 0.75,0.25, 0.25,0.25,
            0.75,0.25, 0.75,0.75, 1.25,0.75, 1.25,0.25))
    elif self.maptype == "CROSS":
        self.tex_coords = c_floats((1.0,0.34, 0.75,0.34, 0.75,0.661, 1.0,0.661, #back
            0.75,0.34, 0.5,0.34, 0.5,0.661, 0.75,0.661,  #right
            0.251,0.0, 0.251,0.34, 0.498,0.34, 0.498,0.0,  #top
            0.498,.998, 0.498,0.66, 0.251,0.66, 0.251,.998,    #bottom
            0.0,0.661, 0.25,0.661, 0.25,0.34, 0.0,0.34,    #left
            0.25,0.34, 0.5,0.34, 0.5,0.661, 0.25,0.661 )) #front
    else:
        self.tex_faces = c_floats((.998,0.002, 0.002,0.002, 0.002,.998, .998,.998,
            .998,0.002, 0.002,0.002, 0.002,.998, .998,.998,
            0.002,0.002, 0.002,.998, .998,.998, .998,0.002,
            .998,.998, .998,0.002, 0.002,0.002, 0.002,.998,
            0.002,.998, .998,.998, .998,0.002, 0.002,0.002,
            0.002,0.002, .998,0.002, .998,.998, 0.002,.998))


  def draw(self,tex, x, y, z):
    mtrx = (ctypes.c_float*16)()
    opengles.glGetFloatv(GL_MODELVIEW_MATRIX,ctypes.byref(mtrx))
    Utility.translatef(-x, -y, -z)
    Utility.texture_min_mag();
    opengles.glVertexPointer(3, GL_FLOAT, 0, self.vertices)
    opengles.glNormalPointer(GL_FLOAT, 0, self.normals)
    opengles.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    opengles.glDisable(GL_LIGHTING)
    opengles.glEnable(GL_TEXTURE_2D)

    if self.maptype=="FACES":
        opengles.glTexCoordPointer(2, GL_FLOAT, 0, self.tex_faces)
        opengles.glBindTexture(GL_TEXTURE_2D,tex[0].tex)
        opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indtop)

        Utility.texture_min_mag()
        opengles.glBindTexture(GL_TEXTURE_2D,tex[1].tex)
        opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indleft)

        Utility.texture_min_mag()
        opengles.glBindTexture(GL_TEXTURE_2D,tex[2].tex)
        opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indfront)

        Utility.texture_min_mag()
        opengles.glBindTexture(GL_TEXTURE_2D,tex[3].tex)
        opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indright)

        Utility.texture_min_mag()
        opengles.glBindTexture(GL_TEXTURE_2D,tex[4].tex)
        opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indback)
        if tex[5] >0:
          Utility.texture_min_mag()
          opengles.glBindTexture(GL_TEXTURE_2D,tex[5].tex)
          opengles.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT , self.indbot)
        else:
          #load view matrix
          opengles.glTexCoordPointer(2, GL_FLOAT, 0, self.tex_coords)
          opengles.glBindTexture(GL_TEXTURE_2D,tex.tex)
          opengles.glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT , self.indices)

    #opengles.glEnable(GL_LIGHTING)
    opengles.glDisable(GL_TEXTURE_2D)
    #restore to previous matrix
    opengles.glLoadMatrixf(mtrx)
