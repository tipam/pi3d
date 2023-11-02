// ----- boiler-plate code for fragment shader to get mapping for use
//       with reflected image

// NB previous define: inray, normout, bfact, bump

  vec3 refl = normalize(reflect(inray, normout - 0.1 * bfact * bump)); // ----- reflection direction from this vertex
  vec2 shinecoord = vec2(atan(-refl.x, -refl.z)/ 6.2831854 + 0.5,
                          acos(refl.y) / 3.1415927); // ------ potentially need to clamp with bump included in normal
  vec4 shinec = vec4(0.0, 0.0, 0.0, 0.0);
