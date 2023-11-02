from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Extrude(Shape):
  """ 3d model inherits from Shape
  NB this shape has an array of three Buffers representing each end face
  and the sides of the prism. Each can be textured seperately for drawing.
  """
  def __init__(self, camera=None, light=None, path=None, height=1.0, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0,
               cx=0.0, cy=0.0, cz=0.0):
    """uses standard constructor for Shape extra Keyword arguments:

      *path*
        Coordinates defining crossection of prism [(x0,z0),(x1,z1)..]
      *height*
        Distance between end faces in the y direction.
    """
    super(Extrude, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                  sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating Extrude ...")

    s = len(path) if path != None else 0
    ht = height * 0.5

    verts = []
    norms = []
    botface = []
    topface = []
    sidefaces = []
    tex_coords = []

    minx = path[0][0]
    maxx = path[0][0]
    minz = path[0][1]
    maxz = path[0][1]

    #find min/max values for texture coords
    for p in range(0, s):
      px = path[p][0]
      pz = path[p][1]
      minx = min(minx, px)
      minz = min(minz, pz)
      maxx = max(maxx, px)
      maxz = max(maxz, pz)

    tx = 1.0 / (maxx - minx)
    tz = 1.0 / (maxz - minz)

    #vertices for sides
    for p in range(s):
      px = path[p][0]
      pz = path[p][1]
      dx = path[(p+1)%s][0] - px
      dz = path[(p+1)%s][1] - pz
      #TODO normalize these vector components, not needed for shadows = 0:2s
      for i in (-1, 1):
        verts.append((px, i*ht, pz))
        norms.append((-dz, 0.0, dx))
        tex_coords.append((1.0*p/s, i*0.5))

    #vertices for edges of top and bottom, bottom first (n=2s to 3s-1) 2s:3s then top (3s+1 to 4s) 3s+1:4s+1
    for i in (-1, 1):
      for p in range(s):
        px = path[p][0]
        pz = path[p][1]
        verts.append((px, i*ht, pz))
        norms.append((0.0, i, 0.0))
        tex_coords.append(((px - minx) * tx, (pz - minz) * tz))
      #top and bottom face mid points verts number 3*s and 4*s+1 (bottom and top respectively)
      verts.append(((minx+maxx)/2, i*ht, (minz+maxz)/2))
      norms.append((0, i, 0))
      tex_coords.append((0.5, 0.5))


    for p in range(s):    #sides - triangle strip
      v0, v1, v2, v3 = 2*p, 2*p+1, (2*p+2)%(2*s), (2*p+3)%(2*s)
      sidefaces.append((v0, v2, v1))
      sidefaces.append((v1, v2, v3))

    for p in range(s):    #bottom face indices - triangle fan
      botface.append((s, (p+1)%s, p))

    for p in range(s):    #top face indices - triangle fan
      topface.append((s, p, (p+1)%s))


    # sides, top, bottom
    self.buf = [Buffer(self, verts[0:(2*s)], tex_coords[0:(2*s)], sidefaces, norms[0:(2*s)]),
          Buffer(self, verts[(2*s):(3*s+1)], tex_coords[(2*s):(3*s+1)], botface, norms[(2*s):(3*s+1)]),
          Buffer(self, verts[(3*s+1):(4*s+2)], tex_coords[(3*s+1):(4*s+2)], topface, norms[(3*s+1):(4*s+2)])]

