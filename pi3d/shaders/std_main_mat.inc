// ----- boiler-plate code for fragment shaders with material textures

// NB previous define: unib, unif, dist

  vec4 texc = vec4(unib[1], 1.0); // ------ basic colour from material vector
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
