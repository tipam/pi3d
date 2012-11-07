import math
import Image
import PIL.ImageOps

from pi3d import *
from pi3d.shape.Shape import Shape

class ElevationMap(Shape):
  def __init__(self, mapfile, width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
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
    tx = ntiles / ix
    ty = ntiles / iy

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
        norms.append(0.0)
        norms.append(1.0)
        norms.append(0.0)
        tex_coords.append((ix - x) * tx)
        tex_coords.append((iy - y) * ty)

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
    #print px,pz,x,z
    #x = wh-math.floor(x+0.5)/ws
    #z = hh-math.floor(z+0.5)/hs

    ih = intersect_triangle((x, self.pixels[x, z] * ht, z),
                            (x + 1, self.pixels[x + 1, z] * ht, z),
                            (x, self.pixels[x, z + 1] * ht, z + 1),
                            (px, 0, pz))
    if ih == -100000:  # TODO: magic number
      ih = intersect_triangle((x + 1, self.pixels[x + 1, z + 1] * ht, z + 1),
                              (x + 1, self.pixels[x + 1, z] * ht, z),
                              (x, self.pixels[x, z + 1] * ht, z + 1),
                              (px, 0, pz))
    if ih == -100000:  # TODO: magic number
      ih = 0

    return ih

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
