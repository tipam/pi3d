import re, os
from pi3d import *
from pi3d.parse_mtl import parse_mtl
from pi3d.shape.Shape import Shape

#########################################################################################
#
# this block added by paddy gaunt 22 August 2012
# Copyright (c) Paddy Gaunt, 2012
# Chunks of this code are based on https://github.com/mrdoob/three.js/ by
# AlteredQualia http://alteredqualia.com
#
#########################################################################################


#########################################################################################
def parse_vertex(text):
  """Parse text chunk specifying single vertex.

  Possible formats:
    vertex index
    vertex index / texture index
    vertex index / texture index / normal index
    vertex index / / normal index
  """

  v = 0
  t = 0
  n = 0

  chunks = text.split("/")

  v = int(chunks[0])
  if len(chunks) > 1:
    if chunks[1]:
      t = int(chunks[1])
  if len(chunks) > 2:
    if chunks[2]:
      n = int(chunks[2])

  return { 'v':v, 't':t, 'n':n }

#########################################################################################
def loadFileOBJ(model,fileName,texs):

  model.coordinateSystem = "Y-up"
  model.parent = None
  model.childModel = [] # don't really need parent and child pointers but will speed up traversing tree
  model.vNormal = False
  model.vGroup = {} # holds the information for each vertex group
  model.texs = texs

  if ("__clone__" in fileName): return #used for cloning this loadModel, i.e. don't need to parse egg file
  # read in the file and parse into some arrays

  filePath = os.path.split(os.path.abspath(fileName))[0]
  print filePath
  f = open(fileName, 'r')

  vertices = []
  normals = []
  uvs = []

  faces = {}

  materials = {}
  material = ""
  mcounter = 0
  mcurrent = 0
  numv = [] #number of vertices for each material (nb each vertex will have three coords)
  numi = [] #number of indices (triangle corners) for each material

  mtllib = ""

  # current face state
  group = 0
  object = 0
  smooth = 0

  for l in f:
    chunks = l.split()
    if len(chunks) > 0:

      # Vertices as (x,y,z) coordinates
      # v 0.123 0.234 0.345
      if chunks[0] == "v" and len(chunks) == 4:
        x = float(chunks[1])
        y = float(chunks[2])
        z = float(chunks[3])
        vertices.append([x,y,z])

      # Normals in (x,y,z) form; normals might not be unit
      # vn 0.707 0.000 0.707
      if chunks[0] == "vn" and len(chunks) == 4:
        x = float(chunks[1])
        y = float(chunks[2])
        z = float(chunks[3])
        normals.append([x,y,z])

      # Texture coordinates in (u,v)
      # vt 0.500 -1.352
      if chunks[0] == "vt" and len(chunks) >= 3:
        u = float(chunks[1])
        v = float(chunks[2])
        uvs.append([u,v])

      # Face
      if chunks[0] == "f" and len(chunks) >= 4:
        vertex_index = []
        uv_index = []
        normal_index = []


        # Precompute vert / normal / uv lists
        # for negative index lookup
        vertlen = len(vertices) + 1
        normlen = len(normals) + 1
        uvlen = len(uvs) + 1

        if len(numv) < (mcurrent+1): numv.append(0)
        if len(numi) < (mcurrent+1): numi.append(0)

        for v in chunks[1:]:
          numv[mcurrent] += 1
          numi[mcurrent] += 3
          vertex = parse_vertex(v)
          if vertex['v']:
            if vertex['v'] < 0:
              vertex['v'] += vertlen
            vertex_index.append(vertex['v'])
          if vertex['t']:
            if vertex['t'] < 0:
              vertex['t'] += uvlen
            uv_index.append(vertex['t'])
          if vertex['n']:
            if vertex['n'] < 0:
              vertex['n'] += normlen
            normal_index.append(vertex['n'])
        numi[mcurrent] -= 6 # number of corners of triangle = (n-2)*3 where n is the number of corners of face
        if not mcurrent in faces: faces[mcurrent] = []

        faces[mcurrent].append({
          'vertex':vertex_index,
          'uv':uv_index,
          'normal':normal_index,

          'group':group,
          'object':object,
          'smooth':smooth,
          })

      # Group
      if chunks[0] == "g" and len(chunks) == 2:
        group = chunks[1]

      # Object
      if chunks[0] == "o" and len(chunks) == 2:
        object = chunks[1]

      # Materials definition
      if chunks[0] == "mtllib" and len(chunks) == 2:
        mtllib = chunks[1]

      # Material
      if chunks[0] == "usemtl":
        if len(chunks) > 1:
          material = chunks[1]
        else:
          material = ""
        if not material in materials:
          mcurrent = mcounter
          materials[material] = mcounter
          mcounter += 1
        else:
          mcurrent = materials[material]

      # Smooth shading
      if chunks[0] == "s" and len(chunks) == 2:
        smooth = chunks[1]

  print "materials:  ", materials
  print "numv: ", numv

  for g in faces:
    numv[g] -= 1
    numi[g] -= 1
    model.vGroup[g] = Shape("", model.x, model.y, model.z, model.rotx,model.roty,model.rotz, model.sx,model.sy,model.sz, model.cx,model.cy,model.cz)
    ctype_array1 = c_float*(numv[g] * 3 + 3)
    model.vGroup[g].vertices = ctype_array1()
    model.vGroup[g].normals = ctype_array1()
    ctype_array2 = c_float*(numv[g] * 2 + 2)
    model.vGroup[g].tex_coords = ctype_array2()
    ctype_array3 = c_short*(numi[g] + 1)
    model.vGroup[g].indices = ctype_array3()
    i = 0 # vertex counter in this material
    j = 0 # triangle vertex count in this material
    print "len uv=",len(vertices)
    for f in faces[g]:
      iStart = i
      for v in range(len(f['vertex'])):
        for k in range(0,3):
          model.vGroup[g].vertices[i*3+k] = c_float(vertices[f['vertex'][v]-1][k])
          model.vGroup[g].normals[i*3+k] = c_float(normals[f['normal'][v]-1][k])
        if (len(f['uv']) > 0 and len(uvs[f['uv'][v]-1]) == 2):
          for k in range(0,2):
            model.vGroup[g].tex_coords[i*2+k] = c_float(uvs[f['uv'][v]-1][k])
        i += 1
      n = i - iStart - 1
      for t in range(1,n):
        model.vGroup[g].indices[j*3] = c_short(iStart)
        model.vGroup[g].indices[j*3+1] = c_short(iStart + t)
        model.vGroup[g].indices[j*3+2] = c_short(iStart + t +1)
        j += 1
    model.vGroup[g].indicesLen = len(model.vGroup[g].indices)
    model.vGroup[g].material = None
    model.vGroup[g].ttype = GL_TRIANGLES


    #for i in range(len(model.vGroup[g].normals)):
    #  print model.vGroup[g].normals[i],
    print
    print "indices=",len(model.vGroup[g].indices)
    print "vertices=",len(model.vGroup[g].vertices)
    print "normals=",len(model.vGroup[g].normals)
    print "tex_coords=",len(model.vGroup[g].tex_coords)

  material_lib = parse_mtl(open(os.path.join(filePath, mtllib), 'r'))
  for m in materials:
    print m
    if 'mapDiffuse' in material_lib[m]:
      tfileName = material_lib[m]['mapDiffuse']
      model.vGroup[materials[m]].texFile = tfileName
      model.vGroup[materials[m]].texID = model.texs.loadTexture(os.path.join(filePath, tfileName), False, True) # load from file
    else:
      model.vGroup[materials[m]].texFile = None
      model.vGroup[materials[m]].texID = None
    if 'colorDiffuse' in material_lib[m]:#TODO maybe don't create this array if texture being used though not exclusive.
    #TODO used by pi3d if light set
      ctype_array4 = c_byte*((numi[materials[m]] + 1)*4)
      model.vGroup[materials[m]].material = ctype_array4()
      redVal = int(material_lib[m]['colorDiffuse'][0] * 255.0)
      grnVal = int(material_lib[m]['colorDiffuse'][1] * 255.0)
      bluVal = int(material_lib[m]['colorDiffuse'][2] * 255.0)
      for i in xrange(0, (numi[materials[m]] + 1)*4, 4):
        model.vGroup[materials[m]].material[i] = c_byte(redVal)
        model.vGroup[materials[m]].material[i + 1] = c_byte(grnVal)
        model.vGroup[materials[m]].material[i + 2] = c_byte(bluVal)
        model.vGroup[materials[m]].material[i + 3] = c_byte(255)


