from __future__ import absolute_import, division, print_function, unicode_literals

# Silo project using pi3d module
# =====================================
# Copyright (c) 2012-2013 Richard Urwin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The above license is the 2-clause BSD license, which is compatible with both
# version 2 and 3 of the GPL. (Unlike versions 2 and 3 of the GPL ;-)
# http://www.gnu.org/licenses/license-list.html
#
# I aim to make all infrastructure of the Silo project open and free, although the
# finished game may contain none-free or otherwise restricted elements such as level maps.
#
# Based on code in the Forest Walk example
# Copyright (c) 2012 - Tim Skillman
# Version 0.04 - 20Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
import os.path

import math, random, sys
from six_mod.moves import filter

# NB PIL must be available to use Building
from PIL import ImageOps, ImageDraw, Image

from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Cuboid import Cuboid
from pi3d.shape.Plane import Plane
from pi3d.Shape import Shape
from pi3d.Buffer import Buffer
from pi3d.Texture import Texture
import logging

LOGGER = logging.getLogger(__name__)

rads = 0.017453292512 # degrees to radians

class xyz(object):
  """
  Encapsulates a 3D point-type triple.
  """
  def __init__(self, x,y=None,z=None):
    """
    Constructor
    Can be initialised either with one of these or by with three things that can be cast to floats.
    """
    if isinstance(x, xyz):
      self.x = x.x
      self.y = x.y
      self.x = x.z
    else:
      self.x = float(x)
      self.y = float(y)
      self.z = float(z)

def __str__(self):
      return "({0}, {1}, {2})".format(self.x, self.y, self.z)


class Size(xyz):
  """
  Encapsulates a 3D size.
  Works together with Position to provide intelligent typing. A position plus a
  size is a position, whereas a position minus a position is a size.
  """
  def __init__(self, x,y=None,z=None):
    super(Size,self).__init__(x, y, z)

  def __add__(self, a):
    if isinstance(a, Position):
      return Position(self.x + a.x, self.y + a.y, self.z + a.z)
    if isinstance(a, Size):
      return Size(self.x + a.x, self.y + a.y, self.z + a.z)
    else:
      raise TypeException

  def __sub__(self,a):
    if isinstance(a, Position):
      return Position(self.x - a.x, self.y - a.y, self.z - a.z)
    if isinstance(a, Size):
      return Size(self.x - a.x, self.y - a.y, self.z - a.z)
    else:
      raise TypeError

  def __div__(self, a):
    return Size(self.x / a, self.y / a, self.z / a)

  def __truediv__(self, a):
    return self.__div__(a)


class Position(xyz):
  """
  Encapsulates a 3D position.
  Works together with Size to provide intelligent typing. A position plus a
  size is a position, whereas a position minus a position is a size.
  """
  def __init__(self, x,y=None,z=None):
    super(Position,self).__init__(x,y,z)

  def __add__(self, a):
    if isinstance(a, Size):
      return Position(self.x + a.x, self.y + a.y, self.z + a.z)
    if isinstance(a, Position):
      return Size(self.x + a.x, self.y + a.y, self.z + a.z)
    else:
      raise TypeException

  def __sub__(self,a):
    if isinstance(a, Size):
      return Position(self.x - a.x, self.y - a.y, self.z - a.z)
    if isinstance(a, Position):
      return Size(self.x - a.x, self.y - a.y, self.z - a.z)
    else:
      raise TypeError

  def setvalue(self,p):
    if not isinstance(p, Position): raise TypeError
    self.x = p.x
    self.y = p.y
    self.z = p.z

def _overlap(x1, w1, x2, w2):
  """
  A utility function for testing for overlap on a single axis. Returns true
  if a line w1 above and below point x1 overlaps a line w2 above and below point x2.
  """
  if x1+w1 < x2-w2: return False
  if x1-w1 > x2+w2: return False

  return True

class ObjectCuboid(object):
  """
  An ObjectCuboid has a size and position (of its centre) and a bulk.
  The size is its extent beyond the centre on the three axes, the position is the position of its centre.
  Note that this is different from the size of an ObjectCuboid. The bulk
  is an aura around it that the auras of other objects can not enter. The bulk can be zero.
  """
  def __init__(self, name, s, p, bulk):
    """
    Constructor
    """
    if not isinstance(s, Size): raise TypeError
    if not isinstance(p, Position): raise TypeError
    self.name = name
    self.size = s
    self.position = p
    self.bulk = bulk

  def x(self):
    """
    Returns the x coordinate of the centre of this object
    """
    return self.position.x

  def y(self):
    """
    Returns the x coordinate of the centre of this object
    """
    return self.position.y

  def top_y(self):
      """
      Returns the y coordinate of the top of this object
      """
      return self.position.y + self.size.y + self.bulk

  def bottom_y(self):
      """
      Returns the y coordinate of the top of this object
      """
      return self.position.y - self.size.y - self.bulk

  def z(self):
    """
    Returns the x coordinate of the centre of this object
    """
    return self.position.z

  def w(self):
    """
    Returns size of this object along the x axis -- its width
    """
    return self.size.x

  def h(self):
    """
    Returns size of this object along the y axis -- its height
    """
    return self.size.y

  def d(self):
    """
    Returns size of this object along the z axis -- its depth
    """
    return self.size.z

  def move(self, p):
    """
    Moves this object to the given position.
    """
    self.position.setvalue(p)

  def Overlaps(self, o, pos=None):
    """
    Returns true if the current ObjectCuboid overlaps the given ObjectCuboid.
    If the pos argument is specified then it is used as the position of the
    given ObjectCuboid instead of its actual position.

    Clear as mud?

    Without a pos argument: "does object o overlap me?"
    With a pos argument: "would object o overlap me if it was at position 'pos'?"
    """
    if pos is None:
      pos = o.position
    return _overlap(self.position.x-self.bulk, self.size.x+2*self.bulk, pos.x-o.bulk, o.size.x+o.bulk*2) and \
      _overlap(self.position.y-self.bulk, self.size.y+2*self.bulk, pos.y-o.bulk, o.size.y+o.bulk*2) and \
      _overlap(self.position.z-self.bulk, self.size.z+2*self.bulk, pos.z-o.bulk, o.size.z+o.bulk*2)


class SolidObject(ObjectCuboid):
  """
  A solid object is one that the avatar can not walk through. It has a size, a position and a bulk.
  The size is its total size on the three axes, the position is the position of its centre.
  The bulk is the aura around it into which the avatar's aura is not allowed to enter. A zero bulk works fine.

  Each solid object can have an optional model associated with it. Each SolidObject created is added to a
  list of SolidObjects. All the models of all the objects in the list can be drawn with a single method call (drawall).
  If a solid object does not have an associated model then drawall() does not attempt to draw it. That
  applies to the avatar and to any objects that are part of merged shapes for example.
  """
  objectlist = []

  def __init__(self,name,s,p, bulk):
    """
    Constructor
    """
    super(SolidObject, self).__init__(name, s / 2, p, bulk)
    type(self).objectlist.append(self)
    self.model = None
    self.details = None

  def remove(self):
    try:
      type(self).objectlist.remove(self)
    except:
      LOGGER.error('Tried to remove %s twice.', self)

  def CollisionList(self, p):
    """
    Returns a list of the objects that would overlap with the current oject,
    if the current object was at the given position. (With the exception of the current
    oject of course.)
    This can be used for any moving object to ensure that its proposed new position is available,
    or maybe to determine when a missile should explode and what it should destroy.
    """
    if not isinstance(p, Position): raise TypeError
    r = list(filter(lambda x: x.Overlaps(self,p), type(self).objectlist))
    try:
        r.remove(self)
    except ValueError:
        pass
    return r

  def setmodel(self, model, details):
    """
    Sets the associated model and the details with which to draw it. If the model is set
    then drawall() will draw this object. If it isn't, it wont.
    """
    self.model = model
    self.details = details
    self.model.set_draw_details(details[0], details[1], details[2], details[3], details[4], details[5])

  @classmethod
  def drawall(self):
    """
    Draw all solid objects to which models (and detailss) have been associated.
    """
    for x in self.objectlist:
      if x.model:
        x.model.draw()

class createMyCuboid(Cuboid):
    """
    A bodge because my cuboids appear to be out of position with respect to my collision
    system. Fortunately it does not seem to happen with planes. Probably my fault.
    """
    def __init__(self,w,h,d, name="", x=0.0,y=0.0,z=0.0, rx=0.0,ry=0.0,rz=0.0, cx=0.0,cy=0.0,cz=0.0):
      fact = 0
      if w > fact:
        fact = w
      if h > fact:
        fact = h
      if d > fact:
        fact = d
      super(createMyCuboid,self).__init__(w=w, h=h, d=d, name=name, x=x+0.125, y=y, z=z-1.125,
        rx=rx, ry=ry, rz=rz, cx=cx, cy=cy, cz=cz, tw=w / fact, th=h / fact, td=d / fact)

wallnum=0
def corridor(x,z, emap, width=10, length=10, height=10, details=None, walls="ns", name="wall", mergeshape=None):
  """
  Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
  The north and south walls are parallel with the x axis, with north being more positive. The east and
  west walls are parallel with the z axis, with east being more positive.
  The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
  "length" along the x axis, and "height" high. All walls and ceiling is a cuboid, 1 unit thick. There is no floor.

  Use this function when having the walls as planes is a problem, such as when their zero thinkness is visible.
  Otherwise corridor_planes() is more efficient.

  Which walls to create are specified by the string argument "walls". This should contain the letters n,e,s,w to draw the
  corresponding wall, or "o" (for open) if no ceiling is required.
  For example a N-S corridor section would use "ew", and a simple corner in the SE with no roof would be "seo"

  If mergeshape is None then the resulting objects are drawn with SolidObject.drawall(), if mergeshape is set then the
  objects are added to it and SolidObject.drawall() will not draw it.

  The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
  """
  global wallnum
  n = z + width / 2
  s = z - width / 2
  e = x + length / 2
  w = x - length / 2

  solid_objects = []

  if "n" in walls:
    # TODO: abstract out the mostly-duplicate code in these cases...
    nwall = SolidObject(name+str(wallnum),
                        Size(length, height, 1),
                        Position(x, emap.calcHeight(x, z) + height / 2, n-0.5), 0)
    solid_objects.append(nwall)
    nwallmodel = createMyCuboid(nwall.w() * 2, nwall.h() * 2, nwall.d() * 2,
          name=name+str(wallnum),
          x=nwall.x(),y=nwall.y(),z=nwall.z(),
          rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0)
    if mergeshape:
      mergeshape.add(nwallmodel)
    else:
      nwall.setmodel(nwallmodel, details)


    wallnum += 1

  if "s" in walls:
    swall = SolidObject(name+str(wallnum), Size(length, height, 1), Position(x, emap.calcHeight(x, z)+height / 2, s+0.5), 0)
    solid_objects.append(swall)
    swallmodel = createMyCuboid(swall.w()*2, swall.h()*2, swall.d()*2,
                                name=name+str(wallnum),
                                x=swall.x(), y=swall.y(), z=swall.z(),
                                rx=0.0, ry=0.0, rz=0.0, cx=0.0,cy=0.0, cz=0.0)
    if mergeshape:
      mergeshape.add(swallmodel)
    else:
      swall.setmodel(swallmodel, details)

    wallnum += 1

  if "e" in walls:
    ewall = SolidObject(name+str(wallnum), Size(1, height, width), Position(e-0.5, emap.calcHeight(x, z)+height / 2, z), 0)
    solid_objects.append(ewall)
    ewallmodel = createMyCuboid(ewall.w()*2, ewall.h()*2, ewall.d()*2,
          name=name+str(wallnum),
          x=ewall.x(), y=ewall.y(), z=ewall.z(),
          rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0)
    if mergeshape:
      mergeshape.add(ewallmodel)
    else:
      ewall.setmodel(ewallmodel, details)

    wallnum += 1

  if "w" in walls:
    wwall = SolidObject(name+str(wallnum), Size(1, height, width), Position(w+0.5, emap.calcHeight(x, z)+height / 2, z), 0)
    solid_objects.append(wwall)
    wwallmodel = createMyCuboid(wwall.w()*2, wwall.h()*2, wwall.d()*2,
          name=name+str(wallnum),
          x=wwall.x(), y=wwall.y(), z=wwall.z(),
          rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0)
    if mergeshape:
      mergeshape.add(wwallmodel)
    else:
      wwall.setmodel(wwallmodel, details)
    wallnum += 1

  if "o" not in walls:
    ceiling = SolidObject(name+str(wallnum), Size(length, 1, width), Position(x, emap.calcHeight(x, z)+height+0.5, z), 0)
    solid_objects.append(ceiling)
    ceilingmodel = createMyCuboid(ceiling.w()*2, ceiling.h()*2, ceiling.d()*2,
          name=name+str(wallnum),
          x=ceiling.x(), y=ceiling.y(), z=ceiling.z(),
          rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0)
    if mergeshape:
      mergeshape.add(ceilingmodel)
    else:
      ceiling.setmodel(ceilingmodel, details)

    wallnum += 1

  return solid_objects


class Building (object):

  # baseScheme : black is wall, white is corridor or room, there is one model
  baseScheme = {"#models": 1,
          (0,None): [["R",0]],
          (1,None): [["R",0], ["C",0]],
          (0,0,"edge"): [["W",0], ["CE", 0]],
          (1,0,"edge"): [["W",0], ["CE", 0]],
          (1,0):[["W",0], ["CE", 0]]}

  # openSectionScheme: black is wall, white is corridor or room, grey has no ceiling, there is one model
  openSectionScheme = {"#models": 1,
              (0,None) : [["R",0]],           # black cell has a roof
              (2,None):[["C", 0], ["R", 0]],      # white cell has a ceiling and roof
              (0,0,"edge"):[["W",0], ["CE", 0]],    # black cell on the edge next to a black cell has a wall and ceiling edge
              (1,0,"edge"):[["W",0], ["CE", 0]],    # grey cell on the edge next to a black cell has a wall and ceiling edge
              (2,0,"edge"):[["W",0], ["CE", 0]],    # white cell on the edge next to a black cell has a wall and ceiling edge
              (2,2,"edge"):[["CE", 0]],         # white cell on the edge next to a white cell a ceiling edge
              (2,0):[["W", 0]],             # white cell next to a black cell has a wall
              (1,0):[["W", 0], ["CE", 0]],       # grey cell next to a black cell has a wall and ceiling edge
              (1,2):[["CE", 0]] }            # grey cell next to a white cell has a ceiling edge

  def __init__(self, mapfile, xpos, zpos, emap, width=10.0, depth=10.0, height=10.0, name="building", draw_details=None, yoff=0.0, scheme=None):
    """
    Creates a building at the given location. Each pixel of the image is one cell of the building
    If the cell is white then the cell is open, if it is black then it is wall. If it is grey
    then it is open and has no ceiling.
    The building is centred at xpos, zpos (which gets renamed herin to x,y to match the image coords)
    Each cell is width on the x axis and depth on the z axis, and the walls are height high on the y axis.

    The function returns a merged shape with the entire building in it.
    """
    self.xpos = xpos
    self.zpos = zpos
    self.width = width
    self.depth = depth
    self.height = height
    self.name = name
    self.ceilingthickness = 1.0
    self.walls = []

    if scheme is None:
      self.scheme = Building.baseScheme
    else:
      self.scheme = scheme

    # We don't have to be rigorous here, this should only be a draw_details or an iterable of draw_details.
    if hasattr(draw_details, "__getitem__") or hasattr(draw_details, "__iter__"):
      assert (len(draw_details) == self.scheme["#models"])
      self.details = draw_details
    else:
      self.details = [draw_details for x in range(self.scheme["#models"])]
    # having a method like this allows draw details to be set later

    self.yoff = yoff

    self.model = [MergeShape(name=name+"."+str(x)) for x in range(self.scheme["#models"])]

    if mapfile[0] != '/':
      import os
      for p in sys.path:
        if os.path.isfile(p + '/' + mapfile): # this could theoretically get different files with same name
          mapfile = p + '/' + mapfile
          break
    LOGGER.info("Loading building map ...%s", mapfile)

    im = Image.open(mapfile)
    im = ImageOps.invert(im)
    ix,iy = im.size

    LOGGER.info("image size %d, %d", ix, iy)

    startx = xpos - ix / 2 * width
    starty = zpos - ix / 2 * depth

    yoff += emap.calcHeight(-xpos,-zpos)

    if not im.mode == "P":
        im = im.convert('P', palette=Image.ADAPTIVE)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    pixels = im.load()

    for y in range(1,iy-1):
      for x in range(1,ix-1):
          colour = pixels[x,y]

          if x == 1:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x-1,y], "edge"), wallfunc=self.west_wall, ceilingedgefunc=self.west_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)
          else:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x-1,y]), wallfunc=self.west_wall, ceilingedgefunc=self.west_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)

          if x == ix-2:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x+1,y], "edge"), wallfunc=self.east_wall, ceilingedgefunc=self.east_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)
          else:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x+1,y]), wallfunc=self.east_wall, ceilingedgefunc=self.east_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)

          if y == 1:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x,y-1], "edge"), wallfunc=self.south_wall, ceilingedgefunc=self.south_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)
          else:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x,y-1]), wallfunc=self.south_wall, ceilingedgefunc=self.south_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)

          if y == iy-2:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x, y+1], "edge"), wallfunc=self.north_wall, ceilingedgefunc=self.north_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)
          else:
            self._executeScheme(x, y, startx, starty, (colour, pixels[x,y+1]), wallfunc=self.north_wall, ceilingedgefunc=self.north_edge, ceilingfunc=self.ceiling, rooffunc=self.roof)

          self._executeScheme(x, y, startx, starty, (colour, None), wallfunc=None, ceilingedgefunc=None, ceilingfunc=self.ceiling, rooffunc=self.roof)

    self.set_draw_details(self.details) # after models created otherwise
                                        # details lost by merging


  def remove_walls(self):
    for w in self.walls:
      w.remove()
    self.walls = []

  def drawAll(self):
    """
    Draws all the models that comprise the building
    """
    for x in range(len(self.model)):
      self.model[x].draw()

  def set_draw_details(self, details):
    """
    Set the shader, textures, ntiles and reflection strength
    """
    for x in range(len(self.model)):
      self.model[x].set_draw_details(details[x][0], details[x][1], details[x][2], details[x][3], details[x][4], details[x][5])

  def _executeScheme (self, x, y, startx, starty, key, wallfunc=None, ceilingedgefunc=None, ceilingfunc=None, rooffunc=None):
    """
    Calls the functions defined for the given key in the scheme.
    Each operation consists of a string and a model index. If the string is W then a wall is created and added to the indexed model.
    If the string is CE then a ceiling edge is created and added to the indexed model.
    If the string is R then a roof is created and if C then a ceiling is created.
    The key has one of three forms:
    (n1, n2) The first number is the colour of the current cell.
      The second number is the colour of the adjacent cell (on the other side of the prospective wall.)
      This is used once per direction to create upto four walls (and ceiling edges).
    (n1, n2, "edge") As (n1,n2), but the cell is on the edge of the building.
    (n, None) The number is the colour of the current cell. This is used once per cell to create the ceiling and roof.
    """

    if key in self.scheme:
      for op in self.scheme[key]:
        if op[0] == "W" and wallfunc:
          wallfunc(x*self.width + startx, self.yoff, y*self.depth + starty,
               self.width, self.depth, self.height,
               self.details[op[1]], mergeshape=self.model[op[1]])
        elif op[0] == "C" and ceilingfunc:
          ceilingfunc(x*self.width + startx, self.yoff, y*self.depth + starty,
               self.width, self.depth, self.height,
               self.details[op[1]], mergeshape=self.model[op[1]])
        elif op[0] == "R" and rooffunc:
          rooffunc(x*self.width + startx, self.yoff, y*self.depth + starty,
               self.width, self.depth, self.height,
               self.details[op[1]], mergeshape=self.model[op[1]])
        elif op[0] == "CE" and ceilingedgefunc:
          ceilingedgefunc(x*self.width + startx, self.yoff, y*self.depth + starty,
               self.width, self.depth, self.height,
               self.details[op[1]], mergeshape=self.model[op[1]])

  def north_wall(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    nwall = SolidObject(name+str(wallnum), Size(length, height, 1), Position(x, y + height / 2, n), 0)
    self.walls.append(nwall)
    model = Plane(w=nwall.w()*2, h=nwall.h()*2, name=name+str(wallnum))
    mergeshape.add(model, nwall.x(), nwall.y(), nwall.z())


    wallnum += 1

  def north_edge(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    model = Plane(w=length, h=self.ceilingthickness, name=name+str(wallnum))
    mergeshape.add(model, x, y+height+self.ceilingthickness / 2, n)

    wallnum += 1

  def south_wall(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    swall = SolidObject(name+str(wallnum), Size(length, height, 1), Position(x, y+height / 2, s), 0)
    self.walls.append(swall)
    model = Plane(w=swall.w()*2, h=swall.h()*2, name=name+str(wallnum))
    mergeshape.add(model, swall.x(),swall.y(),swall.z(), rx=0.0,ry=0.0,rz=0.0)

    wallnum += 1

  def south_edge(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    model = Plane(w=length, h=self.ceilingthickness, name=name+str(wallnum))
    mergeshape.add(model, x,y+height+self.ceilingthickness / 2,s, rx=0.0,ry=0.0,rz=0.0)

    wallnum += 1

  def east_wall(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    ewall = SolidObject(name+str(wallnum), Size(1, height, width), Position(e, y+height / 2, z), 0)
    self.walls.append(ewall)
    model = Plane(w=ewall.d()*2, h=ewall.h()*2, name=name+str(wallnum))
    mergeshape.add(model, ewall.x(),ewall.y(),ewall.z(), rx=0.0,ry=90.0,rz=0.0)

    wallnum += 1

  def east_edge(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    model = Plane(w=width, h=self.ceilingthickness, name=name+str(wallnum))
    mergeshape.add(model, e,y+height+self.ceilingthickness / 2,z, rx=0.0,ry=90.0,rz=0.0)

    wallnum += 1

  def west_wall(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    wwall = SolidObject(name+str(wallnum), Size(1, height, width), Position(w, y+height / 2, z), 0)
    self.walls.append(wwall)
    model = Plane(w=wwall.d()*2, h=wwall.h()*2, name=name+str(wallnum))
    mergeshape.add(model, wwall.x(),wwall.y(),wwall.z(),rx=0.0,ry=90.0,rz=0.0)

    wallnum += 1

  def west_edge(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    model = Plane(w=width, h=self.ceilingthickness, name=name+str(wallnum))
    mergeshape.add(model, w,y+height+self.ceilingthickness / 2,z,rx=0.0,ry=90.0,rz=0.0)

    wallnum += 1

  def ceiling(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None, makeroof=True, makeceiling=True):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The resulting object is added to the given mergeshape

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.
    """
    global wallnum
    n = z + width / 2
    s = z - width / 2
    e = x + length / 2
    w = x - length / 2

    ceilingmodel = Plane(w=length, h=width, name=name+str(wallnum))
    mergeshape.add(ceilingmodel,x,y+height,z,rx=90.0,ry=0.0,rz=0.0)

    wallnum += 1

  def roof(self, x, y, z, width=10, length=10, height=10, details=None, name="wall", mergeshape=None, makeroof=True, makeceiling=True):
    """
    Creates a cell consisting of optional north, south, east and west walls and an optional ceiling.
    The north and south walls are parallel with the x axis, with north being more positive. The east and
    west walls are parallel with the z axis, with east being more positive.
    The cell is centred at (x,y,z). The cell is "width" along the z axis, (so north and south walls are that far apart,)
    "length" along the x axis, and "height" high. Each wall is a plane, but the ceiling is a cuboid, 1 unit high. There is no floor.

    The objects are named with the given name argument as a prefix and a globally incrementing number as the suffix.

    The resulting objects are added to the given mergeshape
    """
    global wallnum

    roof = SolidObject(name+str(wallnum), Size(length, 1, width), Position(x, y+height+self.ceilingthickness / 2, z), 0)
    self.walls.append(roof)
    roofmodel = Plane(w=length, h=width, name=name+str(wallnum))
    mergeshape.add(roofmodel,x,y+height+self.ceilingthickness,z,rx=90.0,ry=0.0,rz=0.0)

    wallnum += 1
