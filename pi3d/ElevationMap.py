from pi3d.pi3dCommon import *
from pi3d import Constants
from pi3d.Shape import Shape

class ElevationMap(Shape):
  def __init__(self, mapfile, width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0):
    super(ElevationMap,self).__init__(name, x, y, z, rx, ry, rz,
                                      sx, sy, sz, cx, cy, cz)
    if Constants.VERBOSE:
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

    if Constants.VERBOSE:
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

    self.vertices = eglfloats(verts)
    self.normals = eglfloats(norms)
    self.indices = eglshorts(idx)
    self.tex_coords = eglfloats(tex_coords)
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

    ih = intersectTriangle((x, self.pixels[x, z] * ht, z),
                           (x + 1, self.pixels[x + 1, z] * ht, z),
                           (x, self.pixels[x, z + 1] * ht, z + 1),
                           (px, 0, pz))
    if ih == -100000:
      ih = intersectTriangle((x + 1, self.pixels[x + 1, z + 1] * ht, z + 1),
                             (x + 1, self.pixels[x + 1, z] * ht, z),
                             (x, self.pixels[x, z + 1] * ht, z + 1),
                             (px,0,pz))
    if ih == -100000:
      ih = 0

    return ih

  def draw(self,tex=None):
    shape_draw(self,tex)
