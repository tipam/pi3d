import math
import Image
import PIL.ImageOps

from numpy import cross, dot, sqrt, array, arctan2, arcsin, degrees, subtract, multiply

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.shape.Shape import Shape
from pi3d.util import Utility

# a rectangular surface where elevation is defined by a greyscal image
class ElevationMap(Shape):
  """
  parameters:
  mapfile -- greyscale image path/file, string
  width -- of the map in world units, float (default 100.0)
  depth -- of the map in world units, float (default 100.0)
  height -- of the map in world units, float (default 10.0)
  divx -- number of divisions into which the map will be divided, int (default 0 will use 200)
  divy -- number of z division s(!!)
  ntiles -- number of repeats for tiling the texture image, int (default 1)
  name -- string (default "")
  x,y,z -- postion of centre of map, float (default 0,0,0)
  rx,ry,rz -- rotations of map degrees, float (default 0,0,0)
  sx,sy,sz -- scale factors, float (default 1,1,1)
  cx,cy,cz -- offset distances, float (default 0,0,0)
  smooth -- calculate normals with averaging rather than point straight up, bool (default True)
  """
  def __init__(self, mapfile, camera=None, light=None,
               width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0, smooth=True):
    super(ElevationMap, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                       sx, sy, sz, cx, cy, cz)
    if VERBOSE:
      print "Loading height map ...",mapfile

    if divx>200 or divy>200:
      print "... Map size can't be bigger than 200x200 divisions"
      divx = 200
      divy = 200

    im = Image.open(mapfile)
    im = PIL.ImageOps.invert(im)
    ix, iy = im.size
    if (ix>200 and divx==0) or (divx > 0):
      if divx == 0:
        divx = 200
        divy = 200
      im = im.resize((divx, divy), Image.ANTIALIAS)
      ix, iy = im.size
    if not im.mode == "P":
      im = im.convert('P', palette=Image.ADAPTIVE)

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    self.pixels = im.load()
    self.width = width
    self.depth = depth
    self.height = height
    self.ix=ix
    self.iy=iy
    self.ttype = GL_TRIANGLE_STRIP

    if VERBOSE:
      print "Creating Elevation Map ...", ix, iy

    wh = width * 0.5
    hh = depth * 0.5
    ws = width / ix
    hs = depth / iy
    ht = height / 255.0
    tx = 1.0*ntiles / ix
    ty = 1.0*ntiles / iy

    verts = []
    norms = []
    tex_coords = []
    idx = []

    for y in range(0,iy):
      for x in range(0,ix):
        hgt = (self.pixels[x,y])*ht
        verts.append((-wh+x*ws, hgt, -hh+y*hs))
        tex_coords.append(((ix-x) * tx,(iy-y) * ty))

    s=0
    #create one long triangle_strip by alternating X directions
    for y in range(0,iy-1):
      for x in range(0,ix-1):
        i = (y * ix)+x
        idx.append((i,i+ix,i+ix+1))
        idx.append((i+ix+1,i+1,i))
        s+=2

    self.buf = []
    self.buf.append(Buffer(self, verts, tex_coords, idx, None, smooth))

  # determines how high an object is when dropped on the map (providing it's inside the map area)
  def dropOn(self, px, pz):
    #adjust for map not set at origin
    px -= self.unif[0]
    pz -= self.unif[2]

    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / self.ix
    hs = self.depth / self.iy
    ht = self.height / 255.0

    if px > -wh and px < wh and pz > -hh and pz < hh:
      pixht = self.pixels[(wh + px) / ws,(hh + pz) / hs] * ht

    return pixht + self.unif[1]

  # accurately determines how high an object is when dropped on the map (providing it's inside the map area)
  def calcHeight(self, px, pz):
    """
    returns the hight of the map at the point specified

    parameters
    px, pz -- location of the point to calculate height
    """
    #adjust for map not set at origin
    px -= self.unif[0]
    pz -= self.unif[2]

    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / self.ix
    hs = self.depth / self.iy
    ht = self.height / 255.0
    #round off to nearest integer
    px = (wh + px) / ws
    pz = (hh + pz) / hs
    x = math.floor(px)
    z = math.floor(pz)
    if x < 0: x = 0
    if x > (self.ix-2): x = self.ix-2
    if z < 0: z = 0
    if z > (self.iy-2): z = self.iy-2
    # use actual vertex location rather than recreate it from pixel*ht
    p0 = int(z*self.ix + x) #offset 1 to get y values
    p1 = p0 + 1
    p2 = p0 + self.ix
    p3 = p0 + self.ix + 1

    if pz > (z + 1 - px + x): #i.e. this point is in the triangle on the opposite side of the diagonal so swap base corners
      x0, y0, z0 = x + 1, self.buf[0].vertices[p3][1], z + 1
    else:
      x0, y0, z0 = x, self.buf[0].vertices[p0][1], z
    return self.unif[1] + intersect_triangle((x0, y0, z0),
                            (x + 1, self.buf[0].vertices[p1][1], z),
                            (x, self.buf[0].vertices[p2][1], z + 1),
                            (px, 0, pz))


  # TODO these functions will be scrambled by any scaling, rotation or offset, either print warning or stop these operations applying
  # Works out if an object at a given location and radius will overlap with the map surface
  def clashTest(self, px, py, pz, rad):
    """
    returns four values:
    boolean whether there is a clash
    x, y, z components of the normal vector
    the amount of overlap at the x,z location

    parameters:
    px, py, pz -- location of object to test
    rad -- radius of object to test
    """
    # added Patrick Gaunt 2012-11-05
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
    minDist, minLoc = 1000000, (0,0)
    for i in xrange(x0+1, x1):
      for j in xrange(z0+1, z1):
        # use the locations stored in the one dimensional vertices matrix generated in __init__. 3 values for each location
        p = j*self.ix + i # pointer to the start of xyz for i,j in the vertices array
        p1 = j*self.ix + i - 1 # pointer to the start of xyz for i-1,j
        p2 = (j-1)*self.ix + i # pointer to the start of xyz for i, j-1
        vertp = self.buf[0].vertices[p]
        normp = self.buf[0].normals[p]
        # work out distance squared from this vertex to the point
        distSq = (px - vertp[0])**2 + (py - vertp[1])**2 + (pz - vertp[2])**2
        if distSq < minDist: # this vertex is nearest so keep a record
          minDist = distSq
          minLoc = (i,j)
        #TODO possibly use numpy for this kind of vector multiplication, though may take more effort to convert to array() than it saves
        # now find the distance between the point and the plane perpendicular to the normal at this vertex
        pDist = Utility.dotproduct((px - vertp[0]),(py - vertp[1]),(pz - vertp[2]),
                                  -normp[0], -normp[1], -normp[2])
        # and the position where the normal from point crosses the plane
        xIsect = px - normp[0]*pDist
        zIsect = pz - normp[2]*pDist

        # if the intersection point is in this rectangle then the x,z values will lie between edges
        if xIsect > self.buf[0].vertices[p1][0] and xIsect < self.buf[0].vertices[p][0] and zIsect > self.buf[0].vertices[p2][2] and zIsect < self.buf[0].vertices[p][2]:
          pDistSq = pDist**2
          # finally if the perpendicular distance is less than the nearest so far keep a record
          if pDistSq < minDist:
            minDist = pDistSq
            minLoc = (i,j)

        #if minDist < radSq:
        #  minDist = radSq

    gLevel = self.calcHeight(px, pz) #check it hasn't tunnelled through by going fast
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

  # works out the pitch (rx) and roll (rz) to apply to an object on the surface of the map at this point
  def pitch_roll(self, px, pz):
    """
    returns a tuple (pitch, roll) in degrees
    
    parameters
    px -- x location
    pz -- z location
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
    forwd = array([-normp[2]*normp[0], -normp[2]*normp[1], normp[0]*normp[0] + normp[1]*normp[1]])
    forwd = forwd / sqrt(forwd.dot(forwd))
    return (degrees(arcsin(-forwd[1])), degrees(arctan2(sidev[1], normp[1])))


#Function calculates the y intersection of a point on a triangle
def intersect_triangle(v1, v2, v3, pos):
  """
  returns the y value of the intersection of the line defined by x,z of pos through the triange defined by v1,v2,v3

  parameters
  v1,v2,v3 -- xyz tuples defining the corners of the triangle
  pos -- xyz tuple defining the x,z of the line
  """
  #calc normal from two edge vectors v2-v1 and v3-v1
  #nVec = Utility.crossproduct(v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2], v3[0]-v1[0],  v3[1]-v1[1], v3[2]-v1[2])
  nVec = cross(subtract(v2,v1), subtract(v3, v1))
  #equation of plane: Ax + By + Cz = kVal where A,B,C are components of normal. x,y,z for point v1 to find kVal
  kVal = dot(nVec,v1)
  #return y val i.e. y = (kVal - Ax - Cz)/B
  return (kVal - nVec[0]*pos[0] - nVec[2]*pos[2])/nVec[1]
