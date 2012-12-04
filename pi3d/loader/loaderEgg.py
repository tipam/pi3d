import re, os
from pi3d import *
import ctypes

from pi3d.Texture import Texture
from pi3d.shape.Shape import Shape

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

  if ("__clone__" in fileName): return #used for cloning this loadModel, i.e. don't need to parse egg file
  # read in the file and parse into some arrays

  filePath = os.path.split(os.path.abspath(fileName))[0]
  print filePath
  f = open(fileName, 'r')
  l = f.read() # whole thing as a string in memory this will only work for reasonably small files!!!

  ############### function to parse file as one off process to avoid re-traversing string #########
  # convertes the '<a> b { c <d> e {f} <g> h {i} }' structure
  # into nested arrays ['a', 'b', 'c',[['d','e','',['','','f',[]]],['g','h','',['','','i',[]]]]]
  def pRec(x, bReg, l, i):
    while 1:
      try: j = bReg.next().start()
      except: return i+1
      c = l[j]
      if c=="<": # add entry to array at this level
        if len(x[3]) == 0: x[2] = l[i:j].strip() # text after "{" and before "<Tabxyz>"
        i = j+1 # save marker for start of descriptor
        x[3].append(["","","",[]])

      elif c=="{":
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
    numv = 0
    numi = 0
    for x in gp:
      if len(x) == 0: continue
      if ("<Group>" in x[0]): groupDrill(x[3], np+x[1])
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
              numv += 1
              numi += 3
            numi -= 6 # number of corners of triangle = (n-2)*3 where n is the number of corners of face
            vpKey = p[3][0][2].strip() # ought to do a for r in p[3]; if "Ref in...
        # add to list
        #while (len(structPList) < (p+1)): structPList.append("")
        #
        structPList.append(polygon(normal, rgba, MRef, TRef, vref, vpKey))

    # now go through the polygons in order of vertexPool+id, trying to ensure that the polygon arrays in each group are built in the order of vertexPool names
    # only cope with one material and one texture per group
    numv -= 1
    numi -= 1
    model.vGroup[np] = Shape("", model.x, model.y, model.z, model.rotx,model.roty,model.rotz, model.sx,model.sy,model.sz, model.cx,model.cy,model.cz)
    ctype_array1 = c_float * (numv * 3 + 3)
    model.vGroup[np].vertices = ctype_array1()
    model.vGroup[np].normals = ctype_array1()
    ctype_array2 = c_float * (numv * 2 + 2)
    model.vGroup[np].tex_coords = ctype_array2()
    ctype_array3 = c_short * (numi + 1)
    model.vGroup[np].indices = ctype_array3()
    nv = 0 # vertex counter in this material
    ni = 0 # triangle vertex count in this material

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
        for k in range(3):
          model.vGroup[np].vertices[nv*3+k] = c_float(structVList[vpKey][j].coords[k])
          if model.vNormal: nml = structVList[vpKey][j].normal[k]
          else: nml = structPList[p].normal[k]
          model.vGroup[np].normals[nv*3+k] = c_float(nml)
        if (len(structVList[vpKey][j].UVcoords) == 2):
          for k in range(2):
            model.vGroup[np].tex_coords[nv*2+k] = c_float(structVList[vpKey][j].UVcoords[k])
        nv += 1

      n = nv - startV - 1
      for j in range(1,n):
        model.vGroup[np].indices[ni*3] = c_short(startV)
        model.vGroup[np].indices[ni*3+1] = c_short(startV + j)
        model.vGroup[np].indices[ni*3+2] = c_short(startV + j +1)
        ni += 1

    model.vGroup[np].indicesLen = len(model.vGroup[np].indices)
    model.vGroup[np].ttype = GL_TRIANGLES

    # load the texture file TODO check if same as previously loaded files (for other loadModel()s)
    if (gTRef in model.textureList):
      model.vGroup[np].texID = model.textureList[gTRef]["texID"]
      model.vGroup[np].texFile = model.textureList[gTRef]["filename"]
    else:
      model.vGroup[np].texID = None
      model.vGroup[np].texFile = None

    # load materials TODO something more sophisticated
    #TODO maybe don't create this array if texture being used?
    if (gMRef in model.materialList):
      ctype_array4 = c_byte * ((numi + 1)*4)
      model.vGroup[np].material = ctype_array4()
      redVal = int(float(model.materialList[gMRef]["diffr"]) * 255.0)
      grnVal = int(float(model.materialList[gMRef]["diffg"]) * 255.0)
      bluVal = int(float(model.materialList[gMRef]["diffb"]) * 255.0)
      for i in xrange(0, (numi + 1)*4, 4):
        model.vGroup[np].material[i] = c_byte(redVal)
        model.vGroup[np].material[i + 1] = c_byte(grnVal)
        model.vGroup[np].material[i + 2] = c_byte(bluVal)
        model.vGroup[np].material[i + 3] = c_byte(255)
    else: model.vGroup[np].material = None
    ####### end of groupDrill function #####################

  bReg = re.finditer("[{}<]",l)
  xx = ["","","",[]]
  pRec(xx, bReg, l, 0)

  for x in xx[3]:
    if "<Texture>" in x[0]:
      model.textureList[x[1]] = {}
      for i in xrange(len(x[3])): model.textureList[x[1]][x[3][i][1]] = x[3][i][2]
      model.textureList[x[1]]["filename"] = x[2].strip("\"")
      #print filePath, model.textureList[x[1]]["filename"]
      model.textureList[x[1]]["texID"] = Texture(os.path.join(filePath, model.textureList[x[1]]["filename"]),False,True) # load from file
    if "<CoordinateSystem>" in x[0]:
      model.coordinateSystem = x[2]
    if "<Material>" in x[0]:
      model.materialList[x[1]] = {}
      for i in xrange(len(x[3])): model.materialList[x[1]][x[3][i][1]] = x[3][i][2]
    if "<Group>" in x[0]:
      groupDrill(x[3], x[1])


# groupDrill(l, "") # recursively break down groups - TODO this doesn't actually work properly because of split() on <Group>

def texSwap(self, texID, fileName):
  texToUse = None
  texToSwap = None
  for t in self.textureList:
    if fileName in self.textureList[t]["filename"]: # NB this is a bit slacker than using == but easier to use
      texToSwap = self.textureList[t]["texID"]
      break
  for g in self.vGroup:
     if self.vGroup[g]["texID"] == texToSwap: self.vGroup[g]["texID"] = texID
  return texToSwap # this texture is returned so it can be used or held by the calling code and reinserted if need be


#########################################################################################
#
#########################################################################################

