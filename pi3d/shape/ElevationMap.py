from __future__ import absolute_import, division, print_function, unicode_literals

import math
import sys, os

import math
import numpy as np

from pi3d import PIL_OK
from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

if PIL_OK:
  from PIL import Image

def file_pathify(file_path):
  if file_path[0] != '/':
    for p in sys.path:
      if os.path.isfile(p + '/' + file_path): # this could theoretically get different files with same name
        file_path = p + '/' + file_path
        break
  return file_path

# a rectangular surface where elevation is defined by a greyscal image
class ElevationMap(Shape):
  """ 3d model inherits from Shape
  """
  def __init__(self, mapfile, camera=None, light=None,
               width=100.0, depth=100.0, height=10.0,
               divx=0, divy=0, ntiles=1.0, name="",
               x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0,
               sx=1.0, sy=1.0, sz=1.0, cx=0.0, cy=0.0, cz=0.0, smooth=True, 
               cubic=False, texmap=None):
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
      *texmap*
        Image file path or PIL.Image to be used to represent each of four
        textures and normals using the uv_elev_map shader. The image is
        converted to greyscale and apportioned between darkest (first and
        second entries in Buffer.textures list) and lightest (seventh and
        eighth entries). The resulting 0.0, 1.0, 2.0 or 3.0 is added to the
        uv texture coordinate i.e. Buffer.array_buffer[:,6:8]
    """
    super(ElevationMap, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                       sx, sy, sz, cx, cy, cz)
    divx += 1 # one more vertex in each direction than number of divisions
    divy += 1
    if divx > 200 or divy > 200:
      LOGGER.warning("... Map size can't be bigger than 199x199 divisions")
      divx = 200
      divy = 200
    #print(type(mapfile), type(""))

    if PIL_OK:
      try:
        if '' + mapfile == mapfile: #HORRIBLE. Only way to cope with python2v3
          mapfile = file_pathify(mapfile)
          LOGGER.info("Loading height map ...%s", mapfile)

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
      im = im.convert('L')
      im = im.transpose(Image.FLIP_TOP_BOTTOM)
      im = im.transpose(Image.FLIP_LEFT_RIGHT)
      self.pixels = im.load()
      if texmap is not None:
        try:
          texmap = file_pathify(texmap)
          tm = Image.open(texmap)
        except:
          tm = texmap
        tm = tm.convert('L')
        tm = tm.resize((ix, iy))
        tm = np.array(tm)
        tm = np.floor(tm * 3.99 / (tm.max() - tm.min())) # set to 0.0, 1.0, 2.0, 3.0
        tm = tm[::-1,::-1].T # effectively reflect and rotate to match mapping of elevation

    else: 
      ''' images saved as compressed numpy npz file. No resizing so needs 
      to be right size.'''
      mapfile = file_pathify(mapfile)
      self.pixels = np.load(mapfile)['arr_0'][::-1,::-1] # has to be saved with default key
      ix, iy = self.pixels.shape[:2]
    
    self.width = width
    self.depth = depth
    self.height = height
    self.ix = ix
    self.iy = iy
    self.ht_y = 0.0
    self.ht_n = np.array([0.0, 1.0, 0.0])

    LOGGER.info("Creating Elevation Map ...%d x %d", ix, iy)

    self.wh = width * 0.5
    self.hh = depth * 0.5
    self.ws = width / (ix - 1.0)
    self.hs = depth / (iy - 1.0)
    self.ht = height / 255.0
    tx = 1.0 * ntiles / ix
    ty = 1.0 * ntiles / iy

    verts = []
    tex_coords = []
    idx = []

    for y in range(iy):
      for x in range(ix):
        hgt = self.pixels[x, y] * self.ht
        verts.append((-self.wh + x * self.ws, 
                      hgt, 
                      -self.hh + y * self.hs))
        if texmap is not None:
          tex_n = tm[x, y]
        else:
          tex_n = 0.0
        tex_coords.append((tex_n + (ix - x) * tx, (iy - y) * ty))

    s = 0
    #create one long triangle_strip by alternating X directions
    for y in range(0, iy-1):
      for x in range(0, ix-1):
        i = (y * ix)+x
        idx.append((i, i+ix, i+ix+1))
        idx.append((i+ix+1, i+1, i))
        s += 2

    self.buf = [Buffer(self, verts, tex_coords, idx, None, smooth)]

  def dropOn(self, px, pz):
    """determines approximately how high an object is when dropped on the map
     (providing it's inside the map area)
    """
    #adjust for map not set at origin
    px -= self.unif[0]
    pz -= self.unif[2]
    '''
    wh = self.width * 0.5
    hh = self.depth * 0.5
    ws = self.width / (self.ix - 1.0)
    hs = self.depth / (self.iy - 1.0)
    ht = self.height / 255.0
    '''
    if px > -self.wh and px < self.wh and pz > -self.hh and pz < self.hh:
      pixht = self.pixels[int((self.wh + px) / self.ws),
                          int((self.hh + pz) / self.hs)] * self.ht
    else:
      pixht = 0.0
    return pixht + self.unif[1]


  def calcHeight(self, px, pz, inc_normal=False, regular_map=True):
    """accurately return the height of the map at the point specified

    Arguments:
      *px, pz*
        Location of the point in world coordinates to calculate height.
      *inc_normal*
        optionall return a tuple with height and normal vector (h, (nx,ny,nz))
      *regular_map*
        setting this to False allows the method to be used with maps constructed
        with irregular vertex locations - i.e. increased vertex density
        around areas of detail. TODO implement functionality to generate
        this type of map.
    """
    px -= self.unif[0] # adjust p for locatoin of map
    pz -= self.unif[2]
    f = self.buf[0].element_array_buffer # alias to faces array for readability!
    v = self.buf[0].array_buffer # alias to vertices array for readability!
    if regular_map: # for regular arrays of vertices this is quicker
      if px > -self.wh and px < self.wh and pz > -self.hh and pz < self.hh:
        ipx, ipz = int((self.wh + px) / self.ws), int((self.hh + pz) / self.hs)
        ix = (ipx + ipz * (self.iy - 1)) * 2
        if (pz - ipz * self.hs) < (px - ipx * self.ws):
          ix += 1
      else:
        ix = 0
    else: # but this is pretty quick
      x0, z0 = v[f[:,0],0], v[f[:,0],2] # two 1D arrays of x,z coords of 1st corners of faces
      x1, z1 = v[f[:,1],0], v[f[:,1],2] # ditto 2nd corner
      x2, z2 = v[f[:,2],0], v[f[:,2],2] # ditto 3rd corner
      # ix should be a tuple containing a list of face indexes where px,pz is
      # a point inside the triangle formed by the three corners listed above
      ix = np.where(((z1 - z0)*(px - x0) + (-x1 + x0)*(pz - z0) >= 0.0) &
                    ((z2 - z1)*(px - x1) + (-x2 + x1)*(pz - z1) >= 0.0) &
                    ((z0 - z2)*(px - x2) + (-x0 + x2)*(pz - z2) >= 0.0))
      if len(ix[0]) > 0: # at least one face found
        ix = ix[0][0] # should only have one but return the first anyway
      else:
         ix = 0
    self.ht_y, self.ht_n = self._intersect_face(ix, (px, 0.0, pz))
    if inc_normal:
      self.ht_n /= np.linalg.norm(self.ht_n) # normalise to unit len
      return (self.unif[1] + self.ht_y, self.ht_n)
    return self.unif[1] + self.ht_y


  def clashTest(self, px, py, pz, rad, span=None):
    """Works out if an object at a given location and radius will overlap
    with the map surface. NB it is possible for tunnel through the mesh.
    Returns four values:

    * boolean whether there is a clash
    * x, y, z components of the normal vector
    * the amount of overlap at the x,z location

    Arguments:
      *px, py, pz*
        Location of object to test in world coordinates.
      *rad*
        Radius of object to test.
      *span*
        size of the square around the point to select faces from - defaults
        to 2 x rad
    """
    f = self.buf[0].element_array_buffer # alias to faces array for readability!
    v = self.buf[0].array_buffer # alias to vertices array for readability!
    p = [[px, py, pz] - v[f[:,i],:3] - self.unif[0:3] for i in range(3)]  # vector from each corner to point
    # reduce scope by only considering reasonably near vertices
    span = 2.0 * rad if span is None else span / 2.0
    ix = np.where((np.abs(p[0][:,0]) < span) | (np.abs(p[0][:,2]) < span) |
                  (np.abs(p[0][:,0]) < span) | (np.abs(p[0][:,2]) < span) |
                  (np.abs(p[0][:,0]) < span) | (np.abs(p[0][:,2]) < span))[0]
    f = f[ix] # now only work with subset of faces
    p = [p[i][ix] for i in range(3)] # reduce p list to mach subse
    nVec = self.buf[0].element_normals[ix] # alias to normals for subse of faces
    # cross product of each edge with normal is vector in plane of face
    # at rt angle to edge pointing inwards, then dot product of these with
    # vectors from corners to point.
    a = [np.einsum('...j,...j', p[i], np.cross(nVec, v[f[:,i],:3] - v[f[:,(i-1)%3],:3])) for i in range(3)]
    # if all are >= 0 then normal from plane to point passes through triangle
    ix = np.where((a[0] >= 0.0) &
                  (a[1] >= 0.0) &
                  (a[2] >= 0.0))
    if len(ix[0]) > 0: # at least one face found, but could be several in convex area
      ix = ix[0]
      dists = np.einsum('...j,...j', nVec[ix], [px, py, pz] - v[f[ix,0],:3])
      dix = np.argmin(np.abs(dists))
      if np.abs(dists[dix]) < rad: # TODO is there a more efficient way rather than doing abs() twice?
        n = nVec[ix][dix] # alias for brevity
        return True, n[0], n[1], n[2], rad - dists[dix]
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
    _, n = self.calcHeight(px, pz, True)
    sidev = np.array([n[1], -n[0], 0.0])
    sidev /= np.linalg.norm(sidev)
    #forwd = np.cross(sidev, normp)
    forwd = np.array([-n[2]*n[0], -n[2]*n[1], n[0]*n[0] + n[1]*n[1]])
    forwd /= np.linalg.norm(forwd)
    return (math.degrees(math.asin(-forwd[1])), math.degrees(math.atan2(sidev[1], n[1])))

  def _intersect_face(self, ix, pos):
    '''calculates the y intersection of a point on a face and returns the y
    value of the intersection of the line defined by x,z of pos through the
    triange.

    **NB** it relies on Buffer.calc_normals() being called when the Buffer was
    created as that writes values into the element_normals array. This will
    be faster than working out the cross product of two sides of the face.

    Arguments:
      *ix*
        is the index of a record in element_array_buffer and element_normals
      *pos*
        tuple (x, y, z) of point

    Returns:
      tuple of y value, normal vector (xn, yn, zn)
    '''
    face = self.buf[0].element_array_buffer[ix]
    nVec = self.buf[0].element_normals[ix]
    v = self.buf[0].array_buffer[face[0], 0:3]
    kVal = np.dot(nVec, v)
    return (kVal - nVec[0]*pos[0] - nVec[2]*pos[2]) / nVec[1], nVec

  def __getstate__(self): # to allow pickling
    self.childModel = None
    state = super(ElevationMap, self).__getstate__()
    state['width'] = self.width
    state['height'] = self.height
    state['depth'] = self.depth
    state['ix'] = self.ix
    state['iy'] = self.iy
    state['wh'] = self.wh
    state['hh'] = self.hh
    state['ws'] = self.ws
    state['hs'] = self.hs
    return state

  def __setstate__(self, state):
    super(ElevationMap, self).__setstate__(state)
    self.width = state['width']
    self.height = state['height']
    self.depth = state['depth']
    self.ix = state['ix']
    self.iy = state['iy']
    self.wh = state['wh']
    self.hh = state['hh']
    self.ws = state['ws']
    self.hs = state['hs']

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
  nVec = np.cross((v2 - v1), (v3 - v1))
  #equation of plane: Ax + By + Cz = kVal where A,B,C are components of normal. x,y,z for point v1 to find kVal
  kVal = np.dot(nVec, v1)
  #return y val i.e. y = (kVal - Ax - Cz)/B also the normal vector seeing as this has been calculated
  return (kVal - nVec[0]*pos[0] - nVec[2]*pos[2]) / nVec[1], nVec

