// ----- boiler-plate code for fragment shader to get lighting

// NB previous define: lightVector, lightFactor, texc, unif

  float intensity = clamp(dot(lightVector, vec3(0.0, 0.0, 1.0)) * lightFactor, 0.0, 1.0); // ------ adjustment of colour according to combined normal
  texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol
