import math
import Image
import PIL.ImageOps

from pi3d import *
from pi3d.shape.Shape import Shape

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
  def __init__(self, mapfile, width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0, smooth=True):
    super(ElevationMap,self).__init__(name, x, y, z, rx, ry, rz,
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

    for y in range(iy):
      for x in range(ix):
        hgt = (self.pixels[x, y]) * ht
        verts.append(-wh + x * ws)
        verts.append(hgt)
        verts.append(-hh + y * hs)
        if (smooth and y > 0 and y < (iy-1) and x > 0 and x < (ix-1)):
          nVec = Utility.crossproduct(-ws, self.pixels[x-1, y]*ht - hgt, 0, 0, hgt - self.pixels[x, y-1]*ht ,hs)
          norms.append(nVec[0])
          norms.append(nVec[1])
          norms.append(nVec[2])
        else:
          norms.append(0.0)
          norms.append(1.0)
          norms.append(0.0)
        tex_coords.append((ix - x) * tx)
        tex_coords.append((iy - y) * ty)
    #smooth normals
    if smooth:
      for y in range(0,iy):
        for x in range(0,ix):
          p = 3*(y*ix+x)
          if (y > 0 and y < (iy-1) and x > 0 and x < (ix-1)):
            norms[p] = (norms[p-3] + norms[p+3] + norms[p-ix*3] + norms[p+ix*3] + norms[p])/5
            norms[p+1] = (norms[p-2] + norms[p+4] + norms[p-ix*3+1] + norms[p+ix*3+1])/5
            norms[p+2] = (norms[p-1] + norms[p+5] + norms[p-ix*3+2] + norms[p+ix*3+2])/5
            # now normalize them to save time with clashTest
            nFact = math.sqrt(norms[p]**2 + norms[p+1]**2 +norms[p+2]**2)
            norms[p] = norms[p]/nFact
            norms[p+1] = norms[p+1]/nFact
            norms[p+2] = norms[p+2]/nFact
    s = 0
    #create one long triangle_strip by alternating X directions
    for y in range(0, iy - 2, 2):
      for x in range(0, ix - 1):
        i = (y * ix) + x
        idx.append(i)
        idx.append(i + ix)
        s+=2
      for x in range(ix - 1, 0, -1):
        i = ((y + 1) * ix) + x
        idx.append(i + ix)
        idx.append(i)
        s += 2

    self.vertices = c_floats(verts)
    self.normals = c_floats(norms)
    self.indices = c_shorts(idx)
    self.tex_coords = c_floats(tex_coords)
    self.ssize = s  #ix * iy * 2
    print s, ix * iy * 2

  # determines how high an object is when dropped on the map (providing it's inside the map area)
  def dropOn(self,x,z):
    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / self.ix
    hs = self.depth / self.iy
    ht = self.height / 255.0

    if x > -wh and x < wh and z > -hh and z < hh:
      pixht = self.pixels[(wh - x) / ws,(hh - z) / hs] * ht

    return pixht

  # accurately determines how high an object is when dropped on the map (providing it's inside the map area)
  def calcHeight(self, px, pz):
    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / self.ix
    hs = self.depth / self.iy
    ht = self.height / 255.0
    #round off to nearest integer
    px = (wh - px) / ws
    pz = (hh - pz) / hs
    x = math.floor(px)
    z = math.floor(pz)
    if x < 0: x = 0
    if x > (self.ix-2): x = self.ix-2
    if z < 0: z = 0
    if z > (self.iy-2): z = self.iy-2
    # use actual vertex location rather than recreate it from pixel*ht
    p0 = int((z*self.ix + x)*3 + 1) #offset 1 to get y values
    p1 = p0 + 3
    p2 = p0 + 3*self.ix
    p3 = p0 + 3*self.ix + 3
    ih = intersect_triangle((x, self.vertices[p0], z),
                            (x + 1, self.vertices[p1], z),
                            (x, self.vertices[p2], z + 1),
                            (px, 0, pz))
    if ih == -100000:  # TODO: magic number
      ih = intersect_triangle((x + 1, self.vertices[p3], z + 1),
                              (x + 1, self.vertices[p1], z),
                              (x, self.vertices[p2], z + 1),
                              (px, 0, pz))
    if ih == -100000:  # TODO: magic number
      ih = 0

    return ih

  # Works out if an object at a given location and radius will overlap with the map surface
  def clashTest(self, px, py, pz, rad):
    """
    it does not interpolate between points so objects can 'sink' into steep sections with no
    intermediate points. Also the height calculation is the equivalent of passing -px, -pz
    to calcHeight() which was designed around 'reverse' positioning for the viewing matrix
    
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
    ht = self.height/255
    halfw = self.width/2.0
    halfd = self.depth/2.0
    dx = self.width/self.ix
    dz = self.depth/self.iy
    
    # work out x and z ranges to check
    x0 = int(math.floor((halfw + px - rad)/dx + 0.5)) - 1
    if x0 < 0: x0 = 0
    x1 = int(math.floor((halfw + px + rad)/dx + 0.5)) + 1
    if x1 > self.ix-1: x1 = self.ix-1
    z0 = int(math.floor((halfd + pz - rad)/dz + 0.5)) - 1
    if z0 < 0: z0 = 0
    z1 = int(math.floor((halfd + pz + rad)/dz + 0.5)) + 1
    if z1 > self.iy-1: z1 = self.iy-1
    
    minDist, minLoc = 1000000, (0,0)
    for i in xrange(x0+1, x1):
      for j in xrange(z0+1, z1):
        # use the locations stored in the one dimensional vertices matrix generated in __init__. 3 values for each location
        p = (j*self.ix + i)*3 # pointer to the start of xyz for i,j in the vertices array
        p1 = (j*self.ix + i - 1)*3 # pointer to the start of xyz for i-1,j
        p2 = ((j-1)*self.ix + i)*3 # pointer to the start of xyz for i, j-1
        # work out distance squared from this vertex to the point
        distSq = (px - self.vertices[p])**2 + (py - self.vertices[p+1])**2 + (pz - self.vertices[p+2])**2
        if distSq < minDist: # this vertex is nearest so keep a record
          minDist = distSq
          minLoc = (i,j)
        
        # now find the distance between the point and the plane perpendicular to the normal at this vertex
        pDist = Utility.dotproduct((px - self.vertices[p]),(py - self.vertices[p+1]),(pz - self.vertices[p+2]),
                                  -self.normals[p],-self.normals[p+1],-self.normals[p+2])
        # and the position where the normal from point crosses the plane
        xIsect = px - self.normals[p]*pDist
        zIsect = pz - self.normals[p+2]*pDist

        # if the intersection point is in this rectangle then the x,z values will lie between edges
        if xIsect > self.vertices[p1] and xIsect < self.vertices[p] and zIsect > self.vertices[p2+2] and zIsect < self.vertices[p+2]:
          pDistSq = pDist**2
          # finally if the perpendicular distance is less than the nearest so far keep a record
          if pDistSq < minDist:
            minDist = pDistSq
            minLoc = (i,j)
         
        #if minDist < radSq:
        #  minDist = radSq
        
    gLevel = self.calcHeight(-px, -pz) #check it hasn't tunnelled through by going fast
    if gLevel > (py-rad):
      minDist = py - gLevel
      minLoc = (int((x0+x1)/2), int((z0+z1)/2))
    
    if minDist <= radSq: #i.e. near enough to clash so return normal
      p = (minLoc[1]*self.ix + minLoc[0])*3
      if minDist < 0:
        jump = rad - minDist
      else:
        jump = 0
      return(True, -self.normals[p], -self.normals[p+1], -self.normals[p+2],  jump)
    else:
      return (False, 0, 0, 0, 0)

def intersect_triangle(v1, v2, v3, pos):
  #Function calculates the y intersection of a point on a triangle

  #Z order triangle
  if v1[2] > v2[2]:
    v1, v2 = v2, v1

  if v1[2] > v3[2]:
    v1, v3 = v3, v1

  if v2[2] > v3[2]:
    v2, v3 = v3, v2

  if pos[2] > v2[2]:
    #test bottom half of triangle
    if pos[2] > v3[2]:
      #print "z below triangle"
      return -100000  # point completely out

    za = (pos[2] - v1[2]) / (v3[2] - v1[2])
    dxa = v1[0] + (v3[0] - v1[0]) * za
    dya = v1[1] + (v3[1] - v1[1]) * za

    zb = (v3[2] - pos[2]) / (v3[2] - v2[2])
    dxb = v3[0] - (v3[0] - v2[0]) * zb
    dyb = v3[1] - (v3[1] - v2[1]) * zb
    if (pos[0] < dxa and pos[0] < dxb) or (pos[0] > dxa and pos[0] > dxb):
      #print "outside of bottom triangle range"
      return -100000
  else:
    #test top half of triangle
    if pos[2] < v1[2]:
        #print "z above triangle",pos[2],v1[2]
        return -100000  # point completely out
    za = (pos[2] - v1[2]) / (v3[2] - v1[2])
    dxa = v1[0] + (v3[0] - v1[0]) * za
    dya = v1[1] + (v3[1] - v1[1]) * za

    zb = (v2[2] - pos[2]) / ((v2[2] + 0.00001) - v1[2])  #get rid of FP error!
    dxb = v2[0] - (v2[0] - v1[0]) * zb
    dyb = v2[1] - (v2[1] - v1[1]) * zb
    if (pos[0] < dxa and pos[0] < dxb) or (pos[0] > dxa and pos[0] > dxb):
      #print "outside of top triangle range"
      return -100000

  #return resultant intersecting height
  return dya + (dyb - dya) * ((pos[0] - dxa)/(dxb - dxa))
