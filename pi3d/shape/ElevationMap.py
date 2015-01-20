from __future__ import absolute_import, division, print_function, unicode_literals

import math
import sys, os

from six.moves import xrange

from PIL import Image, ImageOps

from numpy import cross, dot, array, sum
from math import atan2, asin, degrees, sqrt

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
from pi3d.util import Utility

# a rectangular surface where elevation is defined by a greyscal image
class ElevationMap(Shape):
  """ 3d model inherits from Shape
  """
  def __init__(self, mapfile, camera=None, light=None,
               width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0, smooth=True, cubic=False):
    """uses standard constructor for Shape

    Arguments:
      *mapfile*
        Greyscale image path/file, string. If multiple bytes per pixel
        only the first one will be used for elevation. jpg files will
        create slight errors that will cause mis-matching of edges for
        tiled maps (i.e. use png for these) NB also see divx, divy below
        i.e. div=64x64 requires image 65x65 pixels 

    Keyword arguments:
      *width, depth, height*
        Of the map in world units.
      *divx, divy*
        Number of divisions into which the map will be divided.
        to create vertices (vertices += 1) NB if you want to create a map
        with 64x64 divisions there will be 65x65 vertices in each direction so
        the mapfile (above) needs to 65x65 pixels in order to specify
        elevations precisely and avoid resizing errors.
      *ntiles*
        Number of repeats for tiling the texture image.
      *smooth*
        Calculate normals with averaging rather than pointing
        straight up, slightly faster if false.
    """
    super(ElevationMap, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                       sx, sy, sz, cx, cy, cz)
    divx += 1 # one more vertex in each direction than number of divisions
    divy += 1
    if divx > 200 or divy > 200:
      print("... Map size can't be bigger than 199x199 divisions")
      divx = 200
      divy = 200
    #print(type(mapfile), type(""))
    
    try:
      if '' + mapfile == mapfile: #HORRIBLE. Only way to cope with python2v3
        if mapfile[0] != '/':
          for p in sys.path:
            if os.path.isfile(p + '/' + mapfile): # this could theoretically get different files with same name
              mapfile = p + '/' + mapfile
              break
        if VERBOSE:
          print("Loading height map ...", mapfile)

        im = Image.open(mapfile)
      else:
        im = mapfile #allow image files to be passed as mapfile
    except:
      im = mapfile
    ix, iy = im.size
    if (ix > 200 and divx == 0) or (ix != divx and iy != divy):
      if divx == 0:
        divx = 200
        divy = 200
      im = im.resize((divx, divy), Image.ANTIALIAS)
      ix, iy = im.size

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    self.pixels = im.load()
    self.width = width
    self.depth = depth
    self.height = height
    self.ix = ix
    self.iy = iy
    self.ttype = GL_TRIANGLE_STRIP

    if VERBOSE:
      print("Creating Elevation Map ...", ix, iy)

    wh = width * 0.5
    hh = depth * 0.5
    ws = width / (ix - 1.0)
    hs = depth / (iy - 1.0)
    ht = height / 255.0
    tx = 1.0 * ntiles / ix
    ty = 1.0 * ntiles / iy

    verts = []
    norms = []
    tex_coords = []
    idx = []

    for y in xrange(0, iy):
      for x in xrange(0, ix):
        pxl = self.pixels[x, y]
        hgt = pxl[0] if type(pxl) is tuple else pxl
        hgt *= ht
        this_x = -wh + x*ws
        this_z = -hh + y*hs
        if cubic:
          """ this is a bit experimental. It tries to make the map either zero
          or height high. Vertices are moved 'under' adjacent ones if there is
          a step to make vertical walls. Goes wrong in places - mainly because
          it doesn't check diagonals
          """
          if hgt > height / 2:
            hgt = height
          else:
            hgt = 0.0
          if hgt == 0 and y > 0 and y < iy-1 and x > 0 and x < ix-1:
            if self.pixels[x-1, y] > 127:
              this_x = -wh + (x-1)*ws
            elif self.pixels[x+1, y] > 127:
              this_x = -wh + (x+1)*ws
            elif self.pixels[x, y-1] > 127:
              this_z = -hh + (y-1)*hs
            elif self.pixels[x, y+1] > 127:
              this_z = -hh + (y+1)*hs
            elif self.pixels[x-1, y-1] > 127:
              this_x = -wh + (x-1)*ws
              this_z = -hh + (y-1)*hs
            elif self.pixels[x-1, y+1] > 127:
              this_x = -wh + (x-1)*ws
              this_z = -hh + (y+1)*hs
            elif self.pixels[x+1, y-1] > 127:
              this_x = -wh + (x+1)*ws
              this_z = -hh + (y-1)*hs
            elif self.pixels[x+1, y+1] > 127:
              this_x = -wh + (x+1)*ws
              this_z = -hh + (y+1)*hs
        verts.append((this_x, hgt, this_z))
        tex_coords.append(((ix-x) * tx,(iy-y) * ty))

    s = 0
    #create one long triangle_strip by alternating X directions
    for y in range(0, iy-1):
      for x in range(0, ix-1):
        i = (y * ix)+x
        idx.append((i, i+ix, i+ix+1))
        idx.append((i+ix+1, i+1, i))
        s += 2

    self.buf = []
    self.buf.append(Buffer(self, verts, tex_coords, idx, None, smooth))

  def dropOn(self, px, pz):
    """determines approximately how high an object is when dropped on the map
     (providing it's inside the map area)
    """
    #adjust for map not set at origin
    px -= self.unif[0]
    pz -= self.unif[2]

    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / (self.ix - 1.0)
    hs = self.depth / (self.iy - 1.0)
    ht = self.height / 255.0

    if px > -wh and px < wh and pz > -hh and pz < hh:
      pixht = self.pixels[(wh + px) / ws,(hh + pz) / hs] * ht

    return pixht + self.unif[1]

  def calcHeight(self, px, pz, inc_normal=False):
    """accurately return the height of the map at the point specified

    Arguments:
      *px, pz*
        Location of the point in world coordinates to calculate height.
      *inc_normal*
        optionall return a tuple with height and normal vector (h, (nx,ny,nz))
    """
    #adjust for map not set at origin
    px -= self.unif[0]
    pz -= self.unif[2]

    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / (self.ix - 1.0)
    hs = self.depth / (self.iy - 1.0)
    ht = self.height / 255.0
    #x, y integer index to vertices grid
    x = math.floor((wh + px) / ws)
    z = math.floor((hh + pz) / hs)
    if x < 0:
       x = 0
    if x > (self.ix - 2):
      x = self.ix - 2
    if z < 0:
      z = 0
    if z > (self.iy - 2):
      z = self.iy - 2
    # use actual vertex location rather than recreate it from pixel*ht
    p0 = int(z * self.ix + x) #offset 1 to get y values
    p1 = p0 + 1
    p2 = p0 + self.ix
    p3 = p0 + self.ix + 1
    v0 = self.buf[0].vertices[p0]
    v1 = self.buf[0].vertices[p1]
    v2 = self.buf[0].vertices[p2]
    v3 = self.buf[0].vertices[p3]

    if pz > (v0[2] + hs / ws * (px - v0[0])):
    #opposite side of the diagonal so swap base corners
      y, n = _intersect_triangle(v2, v3, v0, (px, 0, pz))
    else:
      y, n = _intersect_triangle(v1, v0, v3, (px, 0, pz))
    if inc_normal:
      n /= ((n * n).sum()) ** 0.5 # normalise to unit len
      return (self.unif[1] + y, n)
    return self.unif[1] + y

  def clashTest(self, px, py, pz, rad):
    """Works out if an object at a given location and radius will overlap
    with the map surface. Returns four values:

    * boolean whether there is a clash
    * x, y, z components of the normal vector
    * the amount of overlap at the x,z location

    Arguments:
      *px, py, pz*
        Location of object to test in world coordinates.
      *rad*
        Radius of object to test.
    """
    radSq = rad**2
    # adjust for map not set at origin
    px -= self.unif[0]
    py -= self.unif[1]
    pz -= self.unif[2]
    ht = self.height/255
    halfw = self.width/2.0
    halfd = self.depth/2.0
    dx = self.width/self.ix
    dz = self.depth/self.iy

    # work out x and z ranges to check, x0 etc correspond with vertex indices in grid
    x0 = int(math.floor((halfw + px - rad)/dx + 0.5)) - 1
    if x0 < 0: x0 = 0
    x1 = int(math.floor((halfw + px + rad)/dx + 0.5)) + 1
    if x1 > self.ix-1: x1 = self.ix-1
    z0 = int(math.floor((halfd + pz - rad)/dz + 0.5)) - 1
    if z0 < 0: z0 = 0
    z1 = int(math.floor((halfd + pz + rad)/dz + 0.5)) + 1
    if z1 > self.iy-1: z1 = self.iy-1
    # go through grid around px, pz
    minDist, minLoc = 1000000, (0, 0)
    for i in range(x0+1, x1):
      for j in range(z0+1, z1):
        # use the locations stored in the one dimensional vertices matrix
        #generated in __init__. 3 values for each location
        p = j*self.ix + i # pointer to the start of xyz for i,j in the vertices array
        p1 = j*self.ix + i - 1 # pointer to the start of xyz for i-1,j
        p2 = (j-1)*self.ix + i # pointer to the start of xyz for i, j-1
        vertp = self.buf[0].vertices[p]
        normp = self.buf[0].normals[p]
        # work out distance squared from this vertex to the point
        distSq = (px - vertp[0])**2 + (py - vertp[1])**2 + (pz - vertp[2])**2
        if distSq < minDist: # this vertex is nearest so keep a record
          minDist = distSq
          minLoc = (i, j)
        #now find the distance between the point and the plane perpendicular
        #to the normal at this vertex
        pDist = dot([px - vertp[0], py - vertp[1], pz - vertp[2]],
                    [-normp[0], -normp[1], -normp[2]])
        #and the position where the normal from point crosses the plane
        xIsect = px - normp[0]*pDist
        zIsect = pz - normp[2]*pDist

        #if the intersection point is in this rectangle then the x,z values
        #will lie between edges
        if xIsect > self.buf[0].vertices[p1][0] and \
           xIsect < self.buf[0].vertices[p][0] and \
           zIsect > self.buf[0].vertices[p2][2] and \
           zIsect < self.buf[0].vertices[p][2]:
          pDistSq = pDist**2
          # finally if the perpendicular distance is less than the nearest so far
          #keep a record
          if pDistSq < minDist:
            minDist = pDistSq
            minLoc = (i,j)

    gLevel = self.calcHeight(px + self.unif[0], pz + self.unif[1]) #check it hasn't tunnelled through by going fast
    if gLevel > (py-rad):
      minDist = py - gLevel
      minLoc = (int((x0+x1)/2), int((z0+z1)/2))

    if minDist <= radSq: #i.e. near enough to clash so return normal
      p = minLoc[1]*self.ix + minLoc[0]
      normp = self.buf[0].normals[p]
      if minDist < 0:
        jump = rad - minDist
      else:
        jump = 0
      return(True, normp[0], normp[1], normp[2],  jump)
    else:
      return (False, 0, 0, 0, 0)

  def pitch_roll(self, px, pz):
    """works out the pitch (rx) and roll (rz) to apply to an object
    on the surface of the map at this point

    * returns a tuple (pitch, roll) in degrees

    Arguments:
      *px*
        x location
      *pz*
        z location
    """
    px -= self.unif[0]
    pz -= self.unif[2]
    halfw = self.width/2.0
    halfd = self.depth/2.0
    dx = self.width/self.ix
    dz = self.depth/self.iy
    x0 = int(math.floor((halfw + px)/dx + 0.5))
    if x0 < 0: x0 = 0
    if x0 > self.ix-1: x0 = self.ix-1
    z0 = int(math.floor((halfd + pz)/dz + 0.5))
    if z0 < 0: z0 = 0
    if z0 > self.iy-1: z0 = self.iy-1
    normp = array(self.buf[0].normals[z0*self.ix + x0])
    # slight simplification to working out cross products as dirctn always 0,0,1
    #sidev = cross(normp, dirctn)
    sidev = array([normp[1], -normp[0], 0.0])
    sidev = sidev / sqrt(sidev.dot(sidev))
    #forwd = cross(sidev, normp)
    forwd = array([-normp[2]*normp[0], -normp[2]*normp[1],
                  normp[0]*normp[0] + normp[1]*normp[1]])
    forwd = forwd / sqrt(forwd.dot(forwd))
    return (degrees(asin(-forwd[1])), degrees(atan2(sidev[1], normp[1])))

  def __getstate__(self): # to allow pickling
    self.childModel = None
    state = super(ElevationMap, self).__getstate__()
    state['width'] = self.width
    state['height'] = self.height
    state['depth'] = self.depth
    state['ix'] = self.ix
    state['iy'] = self.iy
    return state
  
  def __setstate__(self, state):
    super(ElevationMap, self).__setstate__(state)
    self.width = state['width']
    self.height = state['height']
    self.depth = state['depth']
    self.ix = state['ix']
    self.iy = state['iy']

def _intersect_triangle(v1, v2, v3, pos):
  """calculates the y intersection of a point on a triangle and returns the y
  value of the intersection of the line defined by x,z of pos through the
  triange defined by v1,v2,v3

  Arguments:
    *v1,v2,v3*
      tuples (x1,y1,z1), (x2,y2,z2).. defining the corners of the triangle
    *pos*
      tuple (x,y,z) defining the x,z of the vertical line intersecting triangle
  """
  #calc normal from two edge vectors v2-v1 and v3-v1
  nVec = cross((v2 - v1), (v3 - v1))
  #equation of plane: Ax + By + Cz = kVal where A,B,C are components of normal. x,y,z for point v1 to find kVal
  kVal = dot(nVec, v1)
  #return y val i.e. y = (kVal - Ax - Cz)/B also the normal vector seeing as this has been calculated
  return (kVal - nVec[0]*pos[0] - nVec[2]*pos[2]) / nVec[1], nVec
