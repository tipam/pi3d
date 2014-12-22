// ----- boiler-plate code for fragment shader to get mapping for use
//       with reflected image

// NB previous define: inray, normout, bfact, bump

  vec3 refl = reflect(inray, normout + 0.2 * bfact * bump); // ----- reflection direction from this vertex
  vec3 horiz = cross(inray, vec3(0.0, 1.0, 0.0)); // ----- a 'horizontal' unit vector normal to the inray
  vec3 vert = cross(inray, vec3(1.0, 0.0, 0.0)); // ----- a 'vertical' unit vector normal to the inray
  float hval = dot(refl, horiz); // ----- component of the reflected ray along horizonal
  float vval = dot(refl, vert); // -----  componet of reflected ray along vertical
  float zval = dot(refl, -1.0 * inray); // ----- component of reflected ray in direction back to camera
  // ----- now work out the horizonal and vertical angles relative to inray and map them to range 0 to 1
  vec2 shinecoord = vec2(0.5 - atan(hval , zval)/6.283185307, 0.5 - atan(vval , zval)/6.283185307); // ------ potentially need to clamp with bump included in normal
  vec4 shinec = vec4(0.0, 0.0, 0.0, 0.0);
