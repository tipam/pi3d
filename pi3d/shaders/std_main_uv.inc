// ----- boiler-plate code for fragment shaders with uv textures

// NB previous define: tex0, texcoordout, unib, unif, dist

  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  if (unif[5][0] < 0.0) {
    if (dist > abs(unif[5][0]) || dist <= fract(fog_start) * 100.0) discard; // don't draw
  }
  texc.rgb += unib[1] - vec3(0.5);
  float ffact = smoothstep(fog_start, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
