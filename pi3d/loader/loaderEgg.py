from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import re, os

from pi3d import *
from random import randint
from six_mod.moves import xrange
from six_mod import advance_iterator

from pi3d.Texture import Texture
from pi3d.Buffer import Buffer

#########################################################################################
#
# this block added by paddy gaunt 15 June 2012
# Copyright (c) Paddy Gaunt, 2012
#
#########################################################################################
#######################################################################
class vertex():
  def __init__(self, coords_in, UVcoords_in, normal_in):
    self.coords = coords_in
    self.UVcoords = UVcoords_in
    # self.UVtangent = UVtangent_in
    # self.UVbinormal = UVbinormal_in
    self.normal = normal_in

########################################################################
class polygon():
  def __init__(self, normal_in, rgba_in, MRef_in, TRef_in, vertexRef_in, vpkey_in):
    self.normal = [] #should always be three
    for nVal in normal_in:
      self.normal.append(nVal)

    self.rgba = [] #should always be four
    for rgbVal in rgba_in:
      self.rgba.append(rgbVal)

    self.MRef = MRef_in

    self.TRef = TRef_in

    self.vref = [] # variable number of indices
    for v in vertexRef_in:
      self.vref.append(v)

    self.vpKey = vpkey_in

########################################################################


def loadFileEGG(model, fileName):
  """Loads an panda3d egg file to produce Buffer object
  as part of a Shape.

  Arguments:
    *model*
      Model object to add to.
    *fileName*
      Path and name of egg file relative to program file.

  """
  model.coordinateSystem = "Y-up"
  model.materialList = {}
  model.textureList = {}
  model.vertexGroupList = {}
  model.vertexList = []
  model.polygonList = []
  model.childModelList = []
  model.parentModel = None
  model.childModel = [] # don't really need parent and child pointers but will speed up traversing tree
  model.vNormal = False
  model.vGroup = {} # holds the information for each vertex group

  # read in the file and parse into some arrays

  if fileName[0] != '/':
    import os
    for p in sys.path:
      if os.path.isfile(p + '/' + fileName): # this could theoretically get different files with same name
        fileName = p + '/' + fileName
        break
  filePath = os.path.split(os.path.abspath(fileName))[0]
  if VERBOSE:
    print(filePath)
  f = open(fileName, 'r')
  l = f.read() # whole thing as a string in memory this will only work for reasonably small files!!!

  ############### function to parse file as one off process to avoid re-traversing string #########
  # convertes the '<a> b { c <d> e {f} <g> h {i} }' structure
  # into nested arrays ['a', 'b', 'c',[['d','e','',['','','f',[]]],['g','h','',['','','i',[]]]]]
  def pRec(x, bReg, l, i):
    while 1:
      try:
        nxtFind = advance_iterator(bReg)
        j = nxtFind.start()
      except:
        return i+1
      c = l[j]
      if c == "<": # add entry to array at this level
        if len(x[3]) == 0: x[2] = l[i:j].strip() # text after "{" and before "<Tabxyz>"
        i = j+1 # save marker for start of descriptor
        x[3].append(["", "", "", []])

      elif c == "{":
        xn = x[3][len(x[3])-1]
        tx = l[i-1:j].strip().split()
        xn[0] = tx[0] #x[0] & x[1] is the "<Tabxyz>" & "123" prior to "{"
        xn[1] = tx[1] if len(tx) > 1 else ""
        i = pRec(xn, bReg, l, j+1)
      else: #i.e. c="}" # go up one level of recursion
        if len(x[3]) == 0: x[2] = l[i:j].strip()
        return j+1
  ################### end of pRec #################

  ####### go through all the nested <Groups> ####################
  def groupDrill(gp, np):
    structVList = {}
    offsetVList = {}
    structPList = []
    offset = 0
    #numv = 0
    #numi = 0
    for x in gp:
      if len(x) == 0: continue
      if ("<Group>" in x[0]):
        if len(x[1]) > 0:
          nextnp = np+x[1]
        else:
          nextnp = np+str(randint(10000, 99999))
        groupDrill(x[3], nextnp)
      else:
        #build vertex, polygon, normal, triangles, UVs etc etc
        if "<VertexPool>" in x[0]:
          vp = x[1]
          structVList[vp] = []
          offsetVList[vp] = offset
          for v in x[3]:
            #if "<Vertex>" in v[0]: #try with this test first!
            coords = [float(n) for n in v[2].strip().split()] # before first < error if no coords!
            # texture mapping
            UVcoords = []
            normal = []
            for u in v[3]:
              if "<UV>" in u[0]: UVcoords = [float(n) for n in u[2].strip().split()]
              #TODO get UVtangent and UVbinormal out of UVset (and use them!)
              # if ("<Tangent>" in vList[v]): UVtangent = [float(n) for n in (extBracket("<Tangent>", vList[v]))[0].split()] # not sure how to use this at this stage
              #else: UVtangent = []
              # if ("<Binormal>" in vList[v]): UVbinormal = [float(n) for n in (extBracket("<Binormal>", vList[v]))[0].split()] # not sure how to use this at this stage
              #else: UVbinormal = []
              # normals, used in 'smoothing' edges between polygons
              if "<Normal>" in u[0]: normal = [float(n) for n in u[2].strip().split()]
            vInt = int(v[1])
            while (len(structVList[vp]) < (vInt+1)): structVList[vp].append("")
            structVList[vp][vInt] = (vertex(coords, UVcoords, normal))
            offset += 1
    #
      # now go through splitting out the Polygons from this Group same level as vertexGroup
      if "<Polygon>" in x[0]:
        normal = []
        rgba = []
        MRef = ""
        TRef = ""
        for p in x[3]:
          if ("<Normal>" in p[0]): normal = [float(n) for n in p[2].strip().split()]
          if ("<RGBA>" in p[0]): rgba = [float(n) for n in p[2].strip().split()]
          if ("<MRef>" in p[0]): MRef = p[2].strip()
          if ("<TRef>" in p[0]): TRef = p[2].strip()
          if ("<VertexRef>" in p[0]):
            vref = []
            for n in p[2].strip().split():
              vref.append(int(n))
              #numv += 1
              #numi += 3
            #numi -= 6 # number of corners of triangle = (n-2)*3 where n is the number of corners of face
            vpKey = p[3][0][2].strip() # ought to do a for r in p[3]; if "Ref in...
        # add to list
        #while (len(structPList) < (p+1)): structPList.append("")
        #
        structPList.append(polygon(normal, rgba, MRef, TRef, vref, vpKey))

    # now go through the polygons in order of vertexPool+id, trying to ensure that the polygon arrays in each group are built in the order of vertexPool names
    # only cope with one material and one texture per group
    #numv -= 1
    #numi -= 1
    g_vertices = []
    g_normals = []
    g_tex_coords = []
    g_indices = []
    nv = 0 # vertex counter in this material
    #ni = 0 # triangle vertex count in this material

    gMRef = ""
    gTRef = ""
    nP = len(structPList)
    for p in xrange(nP):
      if (len(structPList[p].MRef) > 0): gMRef = structPList[p].MRef
      else: gMRef = ""
      if (len(structPList[p].TRef) > 0): gTRef = structPList[p].TRef
      else: gTRef = ""

      vpKey = structPList[p].vpKey
      vref = structPList[p].vref
      startV = nv
      for j in vref:

        if (len(structVList[vpKey][j].normal) > 0): model.vNormal = True
        else: model.vNormal = False
        if model.coordinateSystem == "z-up":
          thisV = [structVList[vpKey][j].coords[1], structVList[vpKey][j].coords[2], -structVList[vpKey][j].coords[0]]
          if model.vNormal:
            thisN = [structVList[vpKey][j].normal[1], structVList[vpKey][j].normal[2], -structVList[vpKey][j].normal[0]]
        else:
          thisV = [structVList[vpKey][j].coords[0], structVList[vpKey][j].coords[1], -structVList[vpKey][j].coords[2]]
          if model.vNormal:
            thisN = [structVList[vpKey][j].normal[0], structVList[vpKey][j].normal[1], -structVList[vpKey][j].normal[2]]
        g_vertices.append(thisV)
        if model.vNormal: nml = thisN
        else: nml = structPList[p].normal
        g_normals.append(nml)
        uvc = structVList[vpKey][j].UVcoords
        if (len(uvc) == 2):
          g_tex_coords.append(uvc)
        else:
          g_tex_coords.append([0.0, 0.0])
        nv += 1
      n = nv - startV - 1
      for j in range(1, n):
        g_indices.append((startV, startV + j + 1, startV + j))

    ilen = len(g_vertices)
    if ilen > 0:
      if len(g_normals) != len(g_vertices):
        g_normals = None # force Buffer.__init__() to generate normals
      model.buf.append(Buffer(model, g_vertices, g_tex_coords, g_indices, g_normals))
      n = len(model.buf) - 1
      model.vGroup[np] = n

      model.buf[n].indicesLen = ilen
      model.buf[n].material = (0.0, 0.0, 0.0, 0.0)
      model.buf[n].ttype = GL_TRIANGLES

      # load the texture file TODO check if same as previously loaded files (for other loadModel()s)
      if (gTRef in model.textureList):
        model.buf[model.vGroup[np]].textures = [model.textureList[gTRef]["texID"]]
        model.buf[model.vGroup[np]].texFile = model.textureList[gTRef]["filename"]
      else:
        model.buf[model.vGroup[np]].textures = []
        model.buf[model.vGroup[np]].texFile = None
        #TODO  don't create this array if texture being used but should be able to combine
        if (gMRef in model.materialList):
          redVal = float(model.materialList[gMRef]["diffr"])
          grnVal = float(model.materialList[gMRef]["diffg"])
          bluVal = float(model.materialList[gMRef]["diffb"])
          model.buf[model.vGroup[np]].material = (redVal, grnVal, bluVal, 1.0)
          model.buf[model.vGroup[np]].unib[3:6] = [redVal, grnVal, bluVal]

        else: model.buf[model.vGroup[np]].material = (0.0, 0.0, 0.0, 0.0)
    ####### end of groupDrill function #####################

  bReg = re.finditer('[{}<]', l)
  xx = ["", "", "", []]
  pRec(xx, bReg, l, 0)
  l = None #in case it's running out of memory?
  f.close()

  for x in xx[3]:
    if "<Texture>" in x[0]:
      model.textureList[x[1]] = {}
      for i in xrange(len(x[3])): model.textureList[x[1]][x[3][i][1]] = x[3][i][2]
      model.textureList[x[1]]["filename"] = x[2].strip("\"")
      if VERBOSE:
        print(filePath, model.textureList[x[1]]["filename"])
      model.textureList[x[1]]["texID"] = Texture(os.path.join(filePath, model.textureList[x[1]]["filename"]), False, True) # load from file
    if "<CoordinateSystem>" in x[0]:
      model.coordinateSystem = x[2].lower()
    if "<Material>" in x[0]:
      model.materialList[x[1]] = {}
      for i in xrange(len(x[3])): model.materialList[x[1]][x[3][i][1]] = x[3][i][2]
    if "<Group>" in x[0]:
      groupDrill(x[3], x[1])
