from pi3d import *

from pi3d import Texture
from pi3d import loaderEgg
from pi3d.RotateVec import rotate_vec

from pi3d.shape.Shape import Shape
from pi3d.Matrix import Matrix

class Model(Shape):
  def __init__(self, fileString, texs, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    super(Model, self).__init__(name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    self.exf = fileString[-3:].lower()
    self.texs = texs
    if VERBOSE:
      print "Loading ",fileString

    if self.exf == 'egg':
      self.model = loaderEgg.loadFileEGG(self, fileString, texs)
      return self.model
    else:
      print self.exf, "file not supported"
      return None

  def draw(self, texID=None, n=None):
    # TODO: shadows Shape.draw.
    if self.exf != 'egg':
      return

    # From loaderEgg.draw, probably added by paddy gaunt 15 June 2012
    texToUse = None
    if texID != None:
      texToUse = texID
    elif n != None:
      n = n % (len(self.textureList))
      i = 0
      for t in self.textureList:
        if i == n:
          texToUse = self.textureList[t]["texID"]
          break
        i += 1

    mtrx = Matrix()
    mtrx.push()
    self.transform()
    for g in self.vGroup:
      opengles.glShadeModel(GL_SMOOTH)
      opengles.glVertexPointer( 3, GL_FLOAT, 0, self.vGroup[g]["vertices"]);
      opengles.glNormalPointer( GL_FLOAT, 0, self.vGroup[g]["normals"]);

      texture = texToUse or self.vGroup[g]["texID"]
      with Texture.Loader(texture, self.vGroup[g]["tex_coords"]):
        #TODO enable material colours as well as textures from images
        material = self.vGroup[g]["material"]
        if material:
          #opengles.glMaterialfv(GL_FRONT, GL_DIFFUSE, material);
          opengles.glEnableClientState(GL_COLOR_ARRAY)
          opengles.glColorPointer(4, GL_UNSIGNED_BYTE, 0, material);

        opengles.glDrawElements(GL_TRIANGLES, self.vGroup[g]["trianglesLen"],
                                GL_UNSIGNED_SHORT, self.vGroup[g]["triangles"])


        opengles.glShadeModel(GL_FLAT)
    mtrx.pop()

    for c in self.childModel:
      relx, rely, relz = c.x, c.y, c.z
      relrotx, relroty, relrotz = c.rotx, c.roty, c.rotz
      rval = rotate_vec(self.rotx, self.roty, self.rotz, (c.x, c.y, c.z))
      c.x, c.y, c.z = self.x + rval[0], self.y + rval[1], self.z + rval[2]
      c.rotx, c.roty, c.rotz = (self.rotx + c.rotx, self.roty + c.roty,
                                self.rotz + c.rotz)
      c.draw() #should texture override be passed down to children?
      c.x, c.y, c.z = relx, rely, relz
      c.rotx, c.roty, c.rotz = relrotx, relroty, relrotz

  def clone(self):
    newLM = loadModel("__clone__." + self.exf, self.texs)
    newLM.vGroup = self.vGroup
    return newLM

  def reparentTo(self, parent):
    if not(self in parent.childModel):
      parent.childModel.append(self)

  def texSwap(self, texID, filename):
    return loaderEgg.texSwap(self, texID, filename)

