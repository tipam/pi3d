import re, os
from pi3dCommon import *

#########################################################################################
#
# this block added by paddy gaunt 22 August 2012
# Copyright (c) Paddy Gaunt, 2012
# Chunks of this code are based on https://github.com/mrdoob/three.js/ by
# AlteredQualia http://alteredqualia.com
#
#########################################################################################

def parse_mtl(fname):
    """Parse MTL file.
    """

    materials = {}

    f = open(fname, 'r')
    for line in f:
        chunks = line.split()
        if len(chunks) > 0:

            # Material start
            # newmtl identifier
            if chunks[0] == "newmtl":
                if len(chunks) > 1:
                    identifier = chunks[1]
                else:
                    identifier = ""
                if not identifier in materials:
                    materials[identifier] = {}

            # Diffuse color
            # Kd 1.000 1.000 1.000
            if chunks[0] == "Kd" and len(chunks) == 4:
                materials[identifier]["colorDiffuse"] = [float(chunks[1]), float(chunks[2]), float(chunks[3])]

            # Ambient color
            # Ka 1.000 1.000 1.000
            if chunks[0] == "Ka" and len(chunks) == 4:
                materials[identifier]["colorAmbient"] = [float(chunks[1]), float(chunks[2]), float(chunks[3])]

            # Specular color
            # Ks 1.000 1.000 1.000
            if chunks[0] == "Ks" and len(chunks) == 4:
                materials[identifier]["colorSpecular"] = [float(chunks[1]), float(chunks[2]), float(chunks[3])]

            # Specular coefficient
            # Ns 154.000
            if chunks[0] == "Ns" and len(chunks) == 2:
                materials[identifier]["specularCoef"] = float(chunks[1])

            # Transparency
            # Tr 0.9 or d 0.9
            if (chunks[0] == "Tr" or chunks[0] == "d") and len(chunks) == 2:
                materials[identifier]["transparency"] = float(chunks[1])

            # Optical density
            # Ni 1.0
            if chunks[0] == "Ni" and len(chunks) == 2:
                materials[identifier]["opticalDensity"] = float(chunks[1])

            # Diffuse texture
            # map_Kd texture_diffuse.jpg
            if chunks[0] == "map_Kd" and len(chunks) == 2:
                materials[identifier]["mapDiffuse"] = chunks[1]

            # Ambient texture
            # map_Ka texture_ambient.jpg
            if chunks[0] == "map_Ka" and len(chunks) == 2:
                materials[identifier]["mapAmbient"] = chunks[1]

            # Specular texture
            # map_Ks texture_specular.jpg
            if chunks[0] == "map_Ks" and len(chunks) == 2:
                materials[identifier]["mapSpecular"] = chunks[1]

            # Alpha texture
            # map_d texture_alpha.png
            if chunks[0] == "map_d" and len(chunks) == 2:
                materials[identifier]["mapAlpha"] = chunks[1]

            # Bump texture
            # map_bump texture_bump.jpg or bump texture_bump.jpg
            if (chunks[0] == "map_bump" or chunks[0] == "bump") and len(chunks) == 2:
                materials[identifier]["mapBump"] = chunks[1]

            # Illumination
            # illum 2
            #
            # 0. Color on and Ambient off
            # 1. Color on and Ambient on
            # 2. Highlight on
            # 3. Reflection on and Ray trace on
            # 4. Transparency: Glass on, Reflection: Ray trace on
            # 5. Reflection: Fresnel on and Ray trace on
            # 6. Transparency: Refraction on, Reflection: Fresnel off and Ray trace on
            # 7. Transparency: Refraction on, Reflection: Fresnel on and Ray trace on
            # 8. Reflection on and Ray trace off
            # 9. Transparency: Glass on, Reflection: Ray trace off
            # 10. Casts shadows onto invisible surfaces
            if chunks[0] == "illum" and len(chunks) == 2:
                materials[identifier]["illumination"] = int(chunks[1])

    return materials

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
def loadFileOBJ(self,fileName,texs):
        
    self.coordinateSystem = "Y-up"
    self.materialList = {}
    self.textureList = {}
    self.vertexGroupList = {}
    self.vertexList = []
    self.polygonList = []
    self.childModelList = []
    self.parentModel = None
    self.childModel = [] # don't really need parent and child pointers but will speed up traversing tree
    self.vNormal = False
    self.vGroup = {} # holds the information for each vertex group
    self.texs = texs
    
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
        self.vGroup[g] = create_shape("", self.x, self.y, self.z, self.rotx,self.roty,self.rotz, self.sx,self.sy,self.sz, self.cx,self.cy,self.cz)
        ctype_array1 = eglfloat * (numv[g] * 3 + 3)
        self.vGroup[g].vertices = ctype_array1()
        self.vGroup[g].normals = ctype_array1()
        ctype_array2 = eglfloat * (numv[g] * 2 + 2)
        self.vGroup[g].tex_coords = ctype_array2()
        ctype_array3 = eglshort * (numi[g] + 1)
        self.vGroup[g].indices = ctype_array3()
        i = 0 # vertex counter in this material
        j = 0 # triangle vertex count in this material
        print "len uv=",len(vertices)
        for f in faces[g]:
            iStart = i
            for v in range(len(f['vertex'])):
                #print f['vertex'][v],f['normal'][v],"|"
                for k in range(0,3):
                    self.vGroup[g].vertices[i*3+k] = c_float(vertices[f['vertex'][v]-1][k])
                    self.vGroup[g].normals[i*3+k] = c_float(normals[f['normal'][v]-1][k])
                for k in range(0,2):
                    self.vGroup[g].tex_coords[i*2+k] = c_float(uvs[f['uv'][v]-1][k])
                i += 1
            n = i - iStart - 1
            for t in range(1,n):
                self.vGroup[g].indices[j*3] = c_short(iStart)
                self.vGroup[g].indices[j*3+1] = c_short(iStart + t)
                self.vGroup[g].indices[j*3+2] = c_short(iStart + t +1)
                j += 1
        self.vGroup[g].indicesLen = len(self.vGroup[g].indices)
        self.vGroup[g].material = None
        #TODO add non texture materials here
        self.vGroup[g].ttype = GL_TRIANGLES

        
        #for i in range(len(self.vGroup[g].normals)):
        #    print self.vGroup[g].normals[i],
        print
        print "indices=",len(self.vGroup[g].indices)
        print "vertices=",len(self.vGroup[g].vertices)
        print "normals=",len(self.vGroup[g].normals)
        print "tex_coords=",len(self.vGroup[g].tex_coords)
        
    material_lib = parse_mtl(os.path.join(filePath, mtllib))
    for m in materials:
        print m
        tfileName = material_lib[m]['mapDiffuse']
        self.vGroup[materials[m]].texFile = tfileName
        self.vGroup[materials[m]].texID = self.texs.loadTexture(os.path.join(filePath, tfileName), False, True) # load from file
    
