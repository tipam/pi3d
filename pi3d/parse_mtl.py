def parse_mtl(lines):
  """Parse lines from an MTL model file.
  """

  materials = {}

  for line in lines:
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
