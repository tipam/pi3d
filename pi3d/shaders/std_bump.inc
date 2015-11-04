// ----- boiler-plate code for fragment shader to get lighting with additional normal mapping
//       look up normal map value as a vector where each colour goes from -100% to +100% over its range so
//       0xFF7F7F is pointing right and 0X007F7F is pointing left. This vector is then rotated relative to the rotation
//       of the normal at that vertex.

// NB previous define: bump, dist, lightVector, lightFactor, texc, unif, unib

  bump.y *= -1.0;
  // unib[3][2] ([11] in python) is used to adjust the strength of normal map textures
  float bfact = unib[3][2] * (1.0 - smoothstep(100.0, 600.0, dist)); // ------ attenuate smoothly between 100 and 600 units
  float intensity = clamp(dot(lightVector, normalize(vec3(0.0, 0.0, 1.0) + bump * bfact)) * lightFactor, 0.0, 1.0); // ------ adjustment of colour according to combined normal
  texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol
