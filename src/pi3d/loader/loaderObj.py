from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os

from pi3d.constants import GL_TRIANGLES
from pi3d.loader.parse_mtl import parse_mtl
from pi3d.Texture import Texture
from pi3d.Buffer import Buffer
import logging

LOGGER = logging.getLogger(__name__)

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
  *  vertex index
  *  vertex index / texture index
  *  vertex index / texture index / normal index
  *  vertex index / / normal index
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
def loadFileOBJ(model, fileName):
  """Loads an obj file with associated mtl file to produce Buffer object
  as part of a Shape. Arguments:
    *model*
      Model object to add to.
    *fileName*
      Path and name of obj file relative to program file.
  """
  model.coordinateSystem = "Y-up"
  model.parent = None
  #model.childModel = [] # don't really need parent and child pointers but will speed up traversing tree
  model.vNormal = False
  model.vGroup = {} # holds the information for each vertex group

  # read in the file and parse into some arrays, name='teapot', z=4

  #import os
  if fileName[0] != '/':
    for p in sys.path:
      if os.path.isfile(p + '/' + fileName): # this could theoretically get different files with same name
        fileName = p + '/' + fileName
        break
  filePath = os.path.split(os.path.abspath(fileName))[0]
  LOGGER.debug(filePath)
  f = open(fileName, 'r')

  vertices = []
  normals = []
  uvs = []

  faces = {}

  materials = {}
  material = ""
  mcounter = 0
  mcurrent = 0
  mtllib = ""

  # current face state
  group = 0
  objct = 0
  smooth = 0

  for l in f:
    chunks = l.split()
    if len(chunks) > 0:

      # Vertices as (x,y,z) coordinates
      # v 0.123 0.234 0.345
      if chunks[0] == "v" and len(chunks) >= 4:
        x = float(chunks[1])
        y = float(chunks[2])
        z = -float(chunks[3]) # z direction away in gl es 2.0 shaders
        vertices.append((x, y, z))

      # Normals in (x, y, z) form; normals might not be unit
      # vn 0.707 0.000 0.707
      if chunks[0] == "vn" and len(chunks) >= 4:
        x = float(chunks[1])
        y = float(chunks[2])
        z = -float(chunks[3]) # z direction away in gl es 2.0 shaders
        normals.append((x, y, z))

      # Texture coordinates in (u,v)
      # vt 0.500 -1.352
      if chunks[0] == "vt" and len(chunks) >= 3:
        u = float(chunks[1])
        v = float(chunks[2])
        uvs.append((u, v))

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

        for v in chunks[1:]:
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
        if not mcurrent in faces:
          faces[mcurrent] = []

        faces[mcurrent].append({
          'vertex':vertex_index,
          'uv':uv_index,
          'normal':normal_index,

          'group':group,
          'object':objct,
          'smooth':smooth,
          })

      # Group
      if chunks[0] == "g" and len(chunks) == 2:
        group = chunks[1]

      # Object
      if chunks[0] == "o" and len(chunks) == 2:
        objct = chunks[1]

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
    
  for g in faces: # make each of these into an array_buffer with its own material
    g_vertices = []
    g_normals = []
    g_tex_coords = []
    g_indices = []
    i = 0 # vertex counter in this material
    LOGGER.debug("len uv={}".format(len(vertices)))
    vec_dict = {} # hold unique combinations of v/u/n
    for f in faces[g]:
      vec_list = [] # hold index vals for each array_buffer entry for this face
      length = len(f['vertex'])
      length_n = len(f['normal'])
      length_uv = len(f['uv'])
      for v in range(length):
        vec_tuple = (f['vertex'][v],
                    f['uv'][v] if length_uv > 0 else -1,
                    f['normal'][v] if length_n == length else -1)
        if vec_tuple in vec_dict: #already exists don't duplicate
          vec_list.append(vec_dict[vec_tuple])
        else:
          g_vertices.append(vertices[vec_tuple[0] - 1])
          if length_n == length: #only use normals if there is one for each vertex
            g_normals.append(normals[vec_tuple[2] - 1])
          if (length_uv > 0 and len(uvs[vec_tuple[1] - 1]) == 2):
            g_tex_coords.append(uvs[vec_tuple[1] - 1])
          vec_dict[vec_tuple] = i
          vec_list.append(i)
          i += 1
      for t in range(len(vec_list) - 2):
        g_indices.append((vec_list[0], vec_list[t + 2], vec_list[t + 1]))
    if len(g_normals) != len(g_vertices):
      g_normals = None # force Buffer.__init__() to generate normals
    model.buf.append(Buffer(model, g_vertices, g_tex_coords, g_indices, g_normals))
    n = len(model.buf) - 1
    model.vGroup[g] = n

    model.buf[n].indicesLen = len(model.buf[n].element_array_buffer)
    model.buf[n].material = (0.0, 0.0, 0.0, 0.0)
    model.buf[n].draw_method = GL_TRIANGLES

    LOGGER.debug("indices=%s\nvertices=%s", len(model.buf[n].element_array_buffer), 
                                       len(model.buf[n].array_buffer))

  try:
    material_lib = parse_mtl(open(os.path.join(filePath, mtllib), 'r'))
    for m in materials:
      LOGGER.debug(m)
      if 'mapDiffuse' in material_lib[m]:
        tfileName = material_lib[m]['mapDiffuse']
        model.buf[model.vGroup[materials[m]]].texFile = tfileName
        model.buf[model.vGroup[materials[m]]].textures = [Texture(filePath + '/' + tfileName, blend=False, flip=True)] # load from file
      else:
        model.buf[model.vGroup[materials[m]]].texFile = None
        model.buf[model.vGroup[materials[m]]].textures = []
        if 'colorDiffuse' in material_lib[m]:#TODO don't create this array if texture being used though not exclusive.
        #TODO check this works with appropriate mtl file
          redVal = material_lib[m]['colorDiffuse'][0]
          grnVal = material_lib[m]['colorDiffuse'][1]
          bluVal = material_lib[m]['colorDiffuse'][2]
          model.buf[model.vGroup[materials[m]]].material = (redVal, grnVal, bluVal, 1.0)
          model.buf[model.vGroup[materials[m]]].unib[3:6] = [redVal, grnVal, bluVal]
  except:
    LOGGER.warning('no material specified')