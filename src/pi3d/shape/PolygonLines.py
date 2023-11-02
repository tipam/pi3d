from __future__ import absolute_import, division, print_function, unicode_literals

from pi3d.Buffer import Buffer
from pi3d.Shape import Shape
import logging

LOGGER = logging.getLogger(__name__)

class Segment(object):
    # use class for tidiness, r,s,t,u are corners of polygon representing a line segment
    r = []
    s = []
    t = []
    u = []
    a = 0.0 # line equation gradient (for calc intersections of corners)
    cr = 0.0 # right side line equation const (i.e. in eq of line y = ax + c)
    cs = 0.0 # left side const

class PolygonLines(Shape):
  """ 3d model inherits from Shape"""
  def __init__(self,  camera=None, light=None, vertices=[], material=(1.0,1.0,1.0),
               line_width=1, closed=False, name="", x=0.0, y=0.0, z=0.0,
               sx=1.0, sy=1.0, sz=1.0, rx=0.0, ry=0.0, rz=0.0,
               cx=0.0, cy=0.0, cz=0.0, strip=True):
    """uses standard constructor for Shape extra Keyword arguments:

      *vertices*
        array of tuples [(x0,y0,z0),(x1,y1,z1)..]
      *material*
        tuple (r,g,b)
      *line_width*
        set to 1 if absent or set to a value less than 1
      *closed*
        joins up last leg i.e. for polygons - only used for strip
      *strip*
        use GL_LINE_STRIP otherwise GL_LINES - needs pairs for line ends
    """
    super(PolygonLines, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                sx, sy, sz, cx, cy, cz)

    LOGGER.debug("Creating PolygonLines ...")

    segs = []
    hw = line_width * 0.5 # half width
    step = 1 if strip else 2
    n_v = len(vertices) if closed else len(vertices) - 1
    for i in range(0, n_v, step): #TODO non strip version
        i_next = (i + 1) % len(vertices) # i.e. wrap to first if closed
        ((x0, y0, z0), (x1, y1, z1)) = (vertices[i], vertices[i_next])
        (dx, dy) = (x1 - x0, y1 - y0)
        dlen = (dx ** 2 + dy ** 2) ** 0.5
        (dx, dy) = (dx / dlen, dy / dlen) # normalised vec along segment
        seg = Segment() # for convenient notation
        seg.r = [x0 + dy * hw, y0 - dx * hw, z0] # points to either side of line ends
        seg.s = [x0 - dy * hw, y0 + dx * hw, z0]
        seg.t = [x1 + dy * hw, y1 - dx * hw, z1]
        seg.u = [x1 - dy * hw, y1 + dx * hw, z1]
        seg.a = dy / dx if dx != 0 else 1000000.0
        seg.cr = seg.r[1] - seg.r[0] * seg.a
        seg.cs = seg.s[1] - seg.s[0] * seg.a
        segs.append(seg)
    if strip:
        new_verts = [segs[0].r[:], segs[0].s[:]] # first pair vertex
        n_s = len(segs) if closed else len(segs) - 1
        for i in range(n_s): # calculate intersection points for extension
            i_next = (i + 1) % len(segs) # i.e. wrap for closed
            da = segs[i].a - segs[i_next].a
            if abs(da) < 0.0001: # either straight or doubling back
                new_verts.extend([segs[i].t, segs[i].u])
            else:
                dc = segs[i_next].cr - segs[i].cr # far end right
                new_verts.append([dc / da, segs[i].a * dc / da + segs[i].cr, segs[i].t[2]])
                dc = segs[i_next].cs - segs[i].cs # far end left
                new_verts.append([dc / da, segs[i].a * dc / da + segs[i].cs, segs[i].u[2]])
        if not closed:
            new_verts.extend([segs[-1].t, segs[-1].u]) # last pair vertex
        else:
            new_verts[1] = new_verts[-1][:]
            new_verts[0] = new_verts[-2][:]
        n = len(new_verts) - 2
        indices = [[i+u, i+v, i+w] for i in range(0, n, 2)
                                    for (u, v, w) in [(0, 1, 3), (3, 2, 0)]]
    else: # simpler for non-strip
        new_verts = []
        for seg in segs:
            new_verts.extend([seg.r, seg.s, seg.t, seg.u])
        indices = [[i+u, i+v, i+w] for i in range(0, len(new_verts), 4)
                                     for (u, v, w) in [(0,1,3), (3,2,0)]]

    # UV mapped to vertex locations
    min_x = min((i[0] for i in new_verts))
    max_x = max((i[0] for i in new_verts))
    min_y = min((i[1] for i in new_verts))
    max_y = max((i[1] for i in new_verts))
    x_range = max_x - min_x
    y_range = max_y - min_y
    texcoords = [[(i[0] - min_x) / x_range, 1.0 - (i[1] - min_y) / y_range] for i in new_verts]
    # need normals if using texcoords
    normals = [[0.0, 0.0, -1.0] for i in range(len(new_verts))]

    self.buf = [Buffer(self, new_verts, texcoords, indices, normals, smooth=False)]
    self.set_material(material)